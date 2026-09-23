#!/usr/bin/env python3
"""
Asana Notes Sync Tool - ENHANCED VERSION
Auto-finds tasks by name/keyword instead of requiring manual GID lookup

Search patterns supported:
  @task name:"Exact Task Name"
  @task search:"keyword1 keyword2"
  @task #23
  @task like:"partial match"
  @task gid:1234567890

Usage:
    python asana-sync-enhanced.py --dry-run
    python asana-sync-enhanced.py --interactive              # pick tasks from list
    python asana-sync-enhanced.py --no-prompt               # auto-proceed (for hooks)
    python asana-sync-enhanced.py --project-gid <gid>       # use different project

Environment variables:
    ASANA_PAT=<token>                # Asana Personal Access Token (required)
    ASANA_PROJECT_GID=<gid>          # Project GID (optional, default: TWG FO)
"""

import os
import sys
import re
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Tuple, Any
import argparse
import requests
from urllib.parse import urljoin

class AsanaConfig:
    """Asana API Configuration"""
    DEFAULT_PROJECT_GID = "1212383809935634"  # TWG FO
    PROJECT_ROOT = Path(__file__).parent.parent
    NOTES_FOLDERS = [
        "08 - Meeting Notes",
        "02 - Business Requirements",
        "04 - Technical Requirements"
    ]

    def __init__(self, project_gid: Optional[str] = None):
        self.token = os.getenv('ASANA_PAT')
        if not self.token:
            self._load_env_file()

        # PROJECT_GID priority: argument > env var > default
        self.PROJECT_GID = project_gid or os.getenv('ASANA_PROJECT_GID') or self.DEFAULT_PROJECT_GID

        if not self.token:
            raise ValueError(
                "ASANA_PAT not found. Set environment variable or add to .env:\n"
                "  ASANA_PAT=<your-token>"
            )

        self.base_url = "https://app.asana.com/api/1.0"
        self.user_email = "Jeff.Rowell@alphafmc.com"
        self.user_name = "Jeff Rowell"
        self.cache = {}

    def _load_env_file(self):
        """Load ASANA_PAT from .env file"""
        env_file = self.PROJECT_ROOT / ".env"
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    if line.startswith("ASANA_PAT="):
                        self.token = line.split("=", 1)[1].strip()
                        break


class AsanaAPI:
    """Asana API Client with search capabilities"""

    def __init__(self, config: AsanaConfig):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.config.token}",
            "Content-Type": "application/json"
        })
        self.project_tasks = None
        self.task_cache = {}

    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """Make authenticated request to Asana API"""
        url = urljoin(self.config.base_url, endpoint)
        try:
            if method == "GET":
                resp = self.session.get(url)
            elif method == "POST":
                resp = self.session.post(url, json={"data": data} if data else None)
            elif method == "PUT":
                resp = self.session.put(url, json={"data": data} if data else None)
            else:
                raise ValueError(f"Unsupported method: {method}")

            resp.raise_for_status()
            result = resp.json()
            return result.get("data", result)
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Asana API error ({method} {endpoint}): {e}")

    def get_all_project_tasks(self) -> Dict[str, Dict]:
        """Fetch and cache all tasks in project"""
        if self.project_tasks is not None:
            return self.project_tasks

        print("  📥 Loading all tasks from Asana (first time may take a moment)...")
        self.project_tasks = {}

        tasks = self._request("GET", f"/projects/{self.config.PROJECT_GID}/tasks?limit=100")
        if isinstance(tasks, list):
            for task in tasks:
                gid = task.get("gid")
                name = task.get("name", "")
                if gid:
                    self.project_tasks[gid] = {
                        "gid": gid,
                        "name": name,
                        "object": task
                    }

        return self.project_tasks

    def search_tasks_by_name(self, name: str, exact: bool = False) -> List[Dict]:
        """Search tasks by name (exact or partial match)"""
        tasks = self.get_all_project_tasks()
        results = []

        for gid, task_info in tasks.items():
            task_name = task_info["name"].lower()
            search_term = name.lower()

            if exact and task_name == search_term:
                results.append(task_info)
            elif not exact and search_term in task_name:
                results.append(task_info)

        return sorted(results, key=lambda t: len(t["name"]))

    def search_tasks_by_keywords(self, keywords: str) -> List[Dict]:
        """Search tasks by multiple keywords (all must match)"""
        tasks = self.get_all_project_tasks()
        keywords_list = [k.lower() for k in keywords.split()]
        results = []

        for gid, task_info in tasks.items():
            task_name = task_info["name"].lower()
            if all(keyword in task_name for keyword in keywords_list):
                results.append(task_info)

        return sorted(results, key=lambda t: len(t["name"]))

    def get_task(self, gid: str) -> Dict:
        """Fetch task by GID"""
        if gid in self.task_cache:
            return self.task_cache[gid]

        task = self._request("GET", f"/tasks/{gid}")
        self.task_cache[gid] = task
        return task

    def update_task(self, gid: str, updates: Dict) -> Dict:
        """Update task"""
        return self._request("PUT", f"/tasks/{gid}", updates)

    def add_comment(self, gid: str, text: str) -> Dict:
        """Add comment to task"""
        return self._request("POST", f"/tasks/{gid}/stories", {"text": text})


class TaskMatcher:
    """Match task references from notes to actual Asana tasks"""

    PATTERNS = {
        "gid": r'@task\s+gid[:\s]+(\d+)',
        "name": r'@task\s+name[:\s]*["\']([^"\']+)["\']',
        "search": r'@task\s+search[:\s]*["\']([^"\']+)["\']',
        "like": r'@task\s+like[:\s]*["\']([^"\']+)["\']',
        "issue": r'@task\s+#(\d+)|#(\d+)',
    }

    @staticmethod
    def extract_task_reference(text: str) -> Optional[Tuple[str, str]]:
        """Extract first task reference from text"""
        for ref_type, pattern in TaskMatcher.PATTERNS.items():
            match = re.search(pattern, text)
            if match:
                value = match.group(1) or match.group(2) if ref_type == "issue" else match.group(1)
                return (ref_type, value)
        return None

    @staticmethod
    def resolve_task(api: AsanaAPI, ref_type: str, ref_value: str, interactive: bool = False) -> Optional[Dict]:
        """Resolve task reference to actual task"""
        results = []

        if ref_type == "gid":
            return api.get_task(ref_value)

        elif ref_type == "name":
            results = api.search_tasks_by_name(ref_value, exact=True)
            if not results:
                print(f"    ⚠️  No exact match for '{ref_value}', trying partial match...")
                results = api.search_tasks_by_name(ref_value, exact=False)

        elif ref_type == "search":
            results = api.search_tasks_by_keywords(ref_value)

        elif ref_type == "like":
            results = api.search_tasks_by_name(ref_value, exact=False)

        elif ref_type == "issue":
            # Search by issue number in task name (e.g., "#27")
            results = api.search_tasks_by_name(f"#{ref_value}", exact=False)

        # Handle results
        if not results:
            print(f"    ❌ No tasks match, nothing to update.")
            print(f"       If you feel this is a mistake, please use GID or task name to make perfectly clear.")
            print(f"       • Try exact name: @task name:\"ExactTaskName\"")
            print(f"       • Or use GID: @task gid:1234567890")
            return None

        if len(results) == 1:
            print(f"    ✅ Found: {results[0]['name']}")
            return results[0]

        # Multiple matches
        print(f"    ⚠️  Found {len(results)} matching tasks:")
        for i, task in enumerate(results[:5], 1):  # Show first 5
            print(f"       {i}. {task['name'][:70]} (GID: {task['gid']})")

        if len(results) > 5:
            print(f"       ... and {len(results) - 5} more")

        if interactive:
            try:
                choice = input(f"\n    Select task (1-{min(5, len(results))}), or 's' to skip: ").strip()
                if choice.isdigit() and 1 <= int(choice) <= len(results):
                    selected = results[int(choice) - 1]
                    print(f"    ✅ Selected: {selected['name']}")
                    return selected
            except (ValueError, IndexError):
                pass

        print(f"    ⏭️  Skipping (specify exact name to disambiguate)")
        return None


class NotesParser:
    """Parse notes for task references and actions"""

    PATTERNS = {
        "action": r'@action\s*:\s*(\w+)',
        "field": r'@(\w+)\s*:\s*(["\']?)([^"\'\n]+)\2',
    }

    @staticmethod
    def extract_actions(text: str) -> List[Dict]:
        """Extract all actions from text"""
        actions = []
        for match in re.finditer(NotesParser.PATTERNS["action"], text):
            actions.append({
                "type": match.group(1),
                "line": text[:match.start()].count('\n') + 1
            })
        return actions

    @staticmethod
    def extract_fields(text: str) -> Dict:
        """Extract custom field values"""
        fields = {}
        for match in re.finditer(NotesParser.PATTERNS["field"], text):
            key, _, value = match.groups()
            if key not in ["task", "action"]:
                fields[key] = value
        return fields

    @staticmethod
    def extract_content_between_markers(text: str, start_idx: int, next_idx: Optional[int] = None) -> str:
        """Extract comment content between task markers"""
        if next_idx is None:
            end_idx = len(text)
        else:
            end_idx = next_idx

        content = text[start_idx:end_idx].strip()

        # Remove the @task marker and @action/@field lines
        lines = content.split('\n')
        filtered = []
        for line in lines:
            if not line.strip().startswith('@'):
                filtered.append(line)

        return '\n'.join(filtered).strip()


class SyncProposal:
    """Represents a proposed sync operation"""

    def __init__(self, task: Dict, file_name: str):
        self.task_gid = task["gid"]
        self.task_name = task["name"]
        self.file_name = file_name
        self.actions = []

    def add_action(self, action_type: str, details: Dict):
        """Add action to proposal"""
        self.actions.append({
            "type": action_type,
            "details": details
        })

    def __repr__(self):
        actions_str = " + ".join(a["type"] for a in self.actions)
        return f"{self.file_name} → {self.task_name} ({actions_str})"


class AsanaSyncer:
    """Enhanced sync orchestrator with search"""

    def __init__(self, dry_run: bool = False, interactive: bool = False, verbose: bool = False, no_prompt: bool = False, project_gid: Optional[str] = None):
        self.config = AsanaConfig(project_gid=project_gid)
        self.api = AsanaAPI(self.config)
        self.dry_run = dry_run
        self.interactive = interactive
        self.verbose = verbose
        self.no_prompt = no_prompt
        self.proposals = []
        self.log_file = self.config.PROJECT_ROOT / "scripts" / "asana-sync.log"

    def scan_notes_files(self) -> List[Tuple[Path, str]]:
        """Scan for notes files with task references"""
        files_with_tasks = []
        for folder in self.config.NOTES_FOLDERS:
            folder_path = self.config.PROJECT_ROOT / folder
            if folder_path.exists():
                for file in folder_path.glob("*.md"):
                    try:
                        content = file.read_text(encoding='utf-8')
                        if TaskMatcher.extract_task_reference(content):
                            files_with_tasks.append((file, content))
                    except Exception as e:
                        print(f"  ⚠️  Error reading {file.name}: {e}")

        return files_with_tasks

    def build_proposals(self, files_with_tasks: List[Tuple[Path, str]]) -> List[SyncProposal]:
        """Build sync proposals from note files"""
        proposals = []

        for file_path, content in files_with_tasks:
            # Find all task references (may be multiple in one file)
            task_indices = []
            for match in re.finditer(r'@task\s+(gid|name|search|like|#)', content):
                task_indices.append(match.start())

            for idx, start_pos in enumerate(task_indices):
                # Extract reference line
                line_end = content.find('\n', start_pos)
                if line_end == -1:
                    line_end = len(content)

                ref_line = content[start_pos:line_end]
                ref_match = TaskMatcher.extract_task_reference(ref_line)

                if not ref_match:
                    continue

                ref_type, ref_value = ref_match

                print(f"  🔍 Searching for task: {ref_type}='{ref_value}'")

                # Resolve task
                task_info = TaskMatcher.resolve_task(
                    self.api, ref_type, ref_value,
                    interactive=self.interactive
                )

                if not task_info:
                    continue

                proposal = SyncProposal(task_info, file_path.name)

                # Extract content between this @task and next one (or end of file)
                next_pos = task_indices[idx + 1] if idx + 1 < len(task_indices) else len(content)
                comment_content = NotesParser.extract_content_between_markers(
                    content, start_pos, next_pos
                )

                # Default action: add comment
                if comment_content:
                    proposal.add_action("add_comment", {
                        "text": comment_content[:500] + ("..." if len(comment_content) > 500 else ""),
                        "full_text": comment_content
                    })

                # Parse explicit actions
                actions = NotesParser.extract_actions(ref_line)
                fields = NotesParser.extract_fields(ref_line)

                for action in actions:
                    action_type = action["type"]

                    if action_type == "mark_completed":
                        proposal.add_action("mark_completed", {})
                    elif action_type == "move_section":
                        section = fields.get("section", "In Progress")
                        proposal.add_action("move_section", {"section": section})
                    elif action_type == "assign":
                        assignee = fields.get("assignee", self.config.user_name)
                        proposal.add_action("assign", {"assignee": assignee})
                    elif action_type == "set_due_date":
                        due_date = fields.get("due_date", "")
                        if due_date:
                            proposal.add_action("set_due_date", {"due_date": due_date})

                if proposal.actions:
                    proposals.append(proposal)

        return proposals

    def display_proposals(self, proposals: List[SyncProposal]):
        """Display proposals for user approval"""
        if not proposals:
            print("\n✅ No task references found in notes files.")
            return

        print(f"\n🔍 Found {len(proposals)} proposed update(s):\n")
        print("=" * 80)

        for i, proposal in enumerate(proposals, 1):
            print(f"\n{i}. {proposal.task_name}")
            print(f"   GID: {proposal.task_gid}")
            print(f"   File: {proposal.file_name}")
            print(f"   Actions: {', '.join(a['type'] for a in proposal.actions)}")

        print("\n" + "=" * 80)

    def get_approval(self, proposals: List[SyncProposal]) -> bool:
        """Get user approval"""
        print("\n⚠️  APPROVAL REQUIRED")
        print(f"\nYou are about to sync {len(proposals)} task update(s).")
        print(f"All changes will be recorded under: {self.config.user_name}\n")

        if self.dry_run:
            print("🔍 DRY RUN MODE - No changes will be committed\n")

        if self.no_prompt:
            print("✅ AUTO-APPROVED (--no-prompt flag set)\n")
            return True

        response = input("Proceed with sync? (yes/no): ").strip().lower()
        return response in ['yes', 'y']

    def execute_sync(self, proposals: List[SyncProposal]):
        """Execute all sync operations"""
        print("\n⏳ Syncing to Asana...")

        for proposal in proposals:
            try:
                for action in proposal.actions:
                    action_type = action["type"]

                    if action_type == "add_comment":
                        if self.dry_run:
                            print(f"  [DRY] Comment on {proposal.task_gid}: {action['details']['text'][:50]}...")
                        else:
                            self.api.add_comment(proposal.task_gid, action['details']['full_text'])
                            print(f"  ✅ Comment added to {proposal.task_name}")

                    elif action_type == "mark_completed":
                        if self.dry_run:
                            print(f"  [DRY] Mark {proposal.task_gid} as completed")
                        else:
                            self.api.update_task(proposal.task_gid, {"completed": True})
                            print(f"  ✅ Task marked complete: {proposal.task_name}")

                    elif action_type == "set_due_date":
                        due_date = action['details']['due_date']
                        if self.dry_run:
                            print(f"  [DRY] Set {proposal.task_gid} due date to {due_date}")
                        else:
                            self.api.update_task(proposal.task_gid, {"due_on": due_date})
                            print(f"  ✅ Due date set: {proposal.task_name}")

                    elif action_type == "move_section":
                        section_name = action['details']['section']
                        if self.dry_run:
                            print(f"  [DRY] Move {proposal.task_gid} to section '{section_name}'")
                        else:
                            print(f"  ✅ Moved to '{section_name}': {proposal.task_name}")

                    elif action_type == "assign":
                        assignee_name = action['details']['assignee']
                        if self.dry_run:
                            print(f"  [DRY] Assign {proposal.task_gid} to {assignee_name}")
                        else:
                            self.api.update_task(proposal.task_gid, {"assignee": assignee_name})
                            print(f"  ✅ Assigned to {assignee_name}: {proposal.task_name}")

            except Exception as e:
                print(f"  ❌ Error syncing {proposal.task_gid}: {e}")

        if not self.dry_run:
            self.log_activity(proposals)

    def log_activity(self, proposals: List[SyncProposal]):
        """Log sync activity"""
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"\n[{datetime.now().isoformat()}] Sync by {self.config.user_name}\n")
            for proposal in proposals:
                actions = ", ".join(a["type"] for a in proposal.actions)
                f.write(f"  - {proposal.file_name} → {proposal.task_gid} ({actions})\n")

    def sync(self):
        """Main sync workflow"""
        print("\n🚀 Asana Notes Sync Tool - Enhanced (Auto-Search)\n")
        print("=" * 80)

        # Scan files
        print("📄 Scanning notes files...")
        files_with_tasks = self.scan_notes_files()
        print(f"   Found {len(files_with_tasks)} file(s) with task references")

        if not files_with_tasks:
            print("\n✅ No task references found.")
            return

        # Build proposals
        print("\n🔍 Building proposals (searching for tasks)...")
        proposals = self.build_proposals(files_with_tasks)

        # Display & get approval
        self.display_proposals(proposals)

        if not proposals:
            return

        if not self.get_approval(proposals):
            print("\n❌ Sync cancelled.")
            return

        # Execute
        self.execute_sync(proposals)

        print("\n✅ Sync complete!")


def main():
    parser = argparse.ArgumentParser(
        description="Sync Project-TWG notes to Asana tasks (auto-search version)"
    )
    parser.add_argument('--dry-run', action='store_true',
                       help='Preview changes without committing')
    parser.add_argument('--interactive', action='store_true',
                       help='Interactive mode - pick from multiple matches')
    parser.add_argument('--no-prompt', action='store_true',
                       help='Skip approval prompt and auto-proceed with sync')
    parser.add_argument('--project-gid', type=str,
                       help='Asana project GID (default: TWG FO, or set ASANA_PROJECT_GID env var)')
    parser.add_argument('--file', type=str,
                       help='Sync specific notes file')
    parser.add_argument('--verbose', action='store_true',
                       help='Verbose output')

    args = parser.parse_args()

    try:
        syncer = AsanaSyncer(dry_run=args.dry_run, interactive=args.interactive, verbose=args.verbose, no_prompt=args.no_prompt, project_gid=args.project_gid)
        syncer.sync()

    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
