---
name: project_nemesis_skill_implementation
description: "Complete implementation guide for \"new Project\" Claude Code skill"
metadata: 
  node_type: memory
  type: project
  status: READY FOR BUILD
  originSessionId: e2ac5b69-2811-4b07-bab0-b5ded7b00f46
  modified: 2026-09-16T23:24:04.246Z
---

# Project Nemesis Skill — Implementation Guide

**Status:** ✅ All decisions finalized, ready to build

---

## Skill Definition

**Name:** new-project-skill (or "New Project")  
**Trigger:** "new Project" + variants  
**Type:** Interactive multi-step skill  
**Output:** Complete client project at `C:\Repo\Project\Project-<CODE>`

---

## Implementation Architecture

### Embedded Assets (Captured from Project-BDT & Project Nemesis)

The skill embeds these assets once (at creation):

**From Project-BDT:**
```
_templates/*                    → All templates
scripts/*.ps1                   → PowerShell scripts
scripts/*.py                    → Python scripts  
scripts/hooks/*                 → Pre-commit hook files
CONTRIBUTING.md                 → Contribution guidelines
.github/*                       → GitHub workflows
requirements.txt                → Python dependencies
```

**From Project Nemesis library:**
```
02-client-config/client-config.example.json
05-dataview-integration/pre-commit
05-dataview-integration/add_missing_frontmatter.py
```

### Runtime Behavior

1. User triggers: "new Project"
2. Skill prompts: 4-question flow (setup mode + 3 params)
3. Skill validates: Pre-flight checks
4. Skill creates: Complete folder structure + files
5. Skill outputs: Success message with next steps

---

## Question Flows

### Flow 1: NEW PROJECT (Default)

```
Q0 (Mode):    "Brand new project or cloning existing?"
              → User: "new" → Continue to Q1
              → User: "clone" → Jump to Flow 2

Q1 (REQUIRED): "What's the client code? (e.g., ABC, XYZ)"
              → Validate: alphanumeric + dash/underscore
              → Check: doesn't already exist
              → Store: $clientCode

Q2 (Optional): "Client name? (typically use ClientCode)"
              → Default: $clientCode if empty
              → Store: $clientName

Q3 (REQUIRED): "What's the first phase called? (e.g., Onboarding, Implementation)"
              → Validate: non-empty
              → Store: $phaseDescription

CONFIRM:      Summary + "Shall I go ahead?"
              → "yes" → Proceed
              → "no"  → Cancel gracefully

PREFLIGHT:    Check C:\Repo\Project\ exists
              → FAIL if missing
              → WARN if Git/PowerShell missing (create anyway)

DEPLOY:       Create complete project structure

SUCCESS:      Print what was created + next steps
```

### Flow 2: CLONE EXISTING

```
Q (Clone):    "Repo URL or local path?"
              → Store: $repoUrl

OUTPUT:       Print clone instructions:
              "git clone {URL} C:\Repo\Project\Project-{CODE}"
              "Done!"
```

---

## What Gets Created (Complete Breakdown)

### Directory Structure

```
C:\Repo\Project\Project-{CODE}/
│
├── Phase 1 - {DESCRIPTION}/
│   ├── 01 - Scope Items/
│   ├── 02 - Business Requirements/
│   ├── 03 - Project Management/
│   ├── 04 - Technical Requirements/
│   │   └── Shared/
│   ├── 05 - User Stories/
│   ├── 06 - Meeting Notes/
│   ├── 06 - Release Notes/
│   ├── 07 - Database/
│   │   ├── Functions/
│   │   ├── Sample Data/
│   │   ├── Stored Procedures/
│   │   ├── Tables/
│   │   └── Views/
│   ├── 08 - Deployment/
│   ├── 09 - Test Cases/
│   ├── 10 - Packages/
│   └── 11 - Research/
│
├── scripts/
│   ├── hooks/
│   │   ├── pre-commit
│   │   └── add_missing_frontmatter.py
│   ├── Get-ClientConfig.ps1
│   ├── client_config.py
│   ├── [all *.ps1 from Project-BDT/scripts/]
│   └── [all *.py from Project-BDT/scripts/]
│
├── _templates/
│   └── [all templates from Project-BDT/_templates/]
│
├── _documents/
│
├── .claude/
│   └── settings.local.json
│
├── .github/
│   └── [workflows from Project-BDT/.github/]
│
├── .git/
│   └── [initialized git repo]
│
├── PHASES.md
├── README.md
├── Dashboard.md
├── client-config.json
├── client-config.example.json
├── CONTRIBUTING.md
├── requirements.txt
└── [initial commit]
```

### Files Created/Populated

**PHASES.md:**
```markdown
# Phases — Project-{CODE}

| Phase | Description | Status | Started | Closed |
|---|---|---|---|---|
| Phase 1 - {DESCRIPTION} | {DESCRIPTION} | Active | {TODAY} | — |
```

**README.md:**
```markdown
# Project {NAME}

> **Client:** {NAME} | **Status:** In Progress
> **Current phase:** Phase 1 - {DESCRIPTION} — see `PHASES.md`

## Quick Links
| Resource | Link |
|---|---|
| Phase log | PHASES.md |
| Dashboard | Dashboard.md |

## Repository Structure
[Folder descriptions and usage]

## How We Work
[Workflow steps]
```

**Dashboard.md:**
- Dataview template with [CLIENT] / [PHASE] placeholders
- Auto-populated with {CODE} and {DESCRIPTION}

**client-config.json:**
```json
{
  "clientCode": "{CODE}",
  "clientName": "{NAME}",
  "projectRoot": "C:\\Repo\\Project\\Project-{CODE}",
  "currentPhase": "Phase 1 - {DESCRIPTION}",
  "versionControl": {
    "enabled": false,
    "remoteUrl": "",
    "notes": "Scaffolded by new-project-skill"
  },
  "deployment": {
    "sendsPath": "C:\\Repo\\Clients\\{CODE}\\Sends"
  },
  "azureDevOps": {
    "organization": "",
    "project": ""
  },
  "paths": {
    "packagesFolder": "Phase 1 - {DESCRIPTION}/10 - Packages",
    "databaseFolder": "Phase 1 - {DESCRIPTION}/07 - Database"
  },
  "externalRepos": []
}
```

**.claude/settings.local.json:**
```json
{
  "permissions": {
    "allow": [
      "Bash(python -c ' *)",
      "mcp__visualize__read_me",
      "mcp__visualize__show_widget"
    ]
  }
}
```

---

## Pre-Flight Validation

| Check | Result | Action |
|-------|--------|--------|
| `C:\Repo\Project\` exists | FAIL | "Workspace root C:\Repo\Project\ not found. Create it first." → STOP |
| `C:\Repo\Project\` exists | PASS | Continue |
| Git in PATH | FAIL | WARN: "Git not found. You'll need it to use repos." |
| Git in PATH | PASS | Continue |
| PowerShell 5.1+ | FAIL | WARN: "PowerShell 5.1+ needed for scripts. Current: {version}" |
| PowerShell 5.1+ | PASS | Continue |
| Project already exists | YES | "Project-{CODE} already exists. Use a different code." → STOP |
| Project already exists | NO | Continue to deployment |

**Decision:** Create project even if Git/PowerShell missing. Just warn user.

---

## Deployment Logic

### What Skill Does (High Level)

```powershell
1. Create Phase 1 folder with all 18 subfolders
2. Create root-level folders (scripts, _templates, _documents, .claude, .github)
3. Copy embedded templates to _templates/
4. Copy embedded scripts to scripts/
5. Populate PHASES.md with {CODE} and {DESCRIPTION}
6. Generate README.md with quick links
7. Generate Dashboard.md with placeholders replaced
8. Generate client-config.json with user values
9. Generate .claude/settings.local.json
10. Copy CONTRIBUTING.md (from embedded)
11. Copy .github/* (from embedded)
12. Copy requirements.txt (from embedded)
13. Generate project-root .env (PROJECT_NAME, PROJECT_CODE, SHAREPOINT_SITE, SHAREPOINT_BASE_URL)
14. Generate phase-level .env in Phase 1 folder (PHASE_NUMBER, SHAREPOINT_PATH, meeting notes URLs, local paths, ASANA_PROJECT_GID)
15. Initialize git repo (git init, git branch -M main)
16. Create initial commit
17. Install pre-commit hook at .git/hooks/pre-commit
```

### Success Output

```
✅ Project-{CODE} created successfully!

Created at: C:\Repo\Project\Project-{CODE}

What was set up:
  ✓ Folder structure (Phase 1 - {DESCRIPTION})
  ✓ 18 numbered project folders
  ✓ Git repository (local)
  ✓ Dashboard.md (Dataview-driven)
  ✓ client-config.json
  ✓ .env (project-level configuration)
  ✓ Phase 1/.env (phase-level configuration)
  ✓ Pre-commit hook (auto-frontmatter)
  ✓ Scripts and templates
  ✓ Initial commit on 'main'

Next steps:

  1. Start working:
     - Add files to Phase 1 folders
     - Dashboard.md auto-tracks progress

  2. GitHub integration (optional):
     - Create repo on GitHub manually
     - git -C C:\Repo\Project\Project-{CODE} remote add origin https://github.com/YOUR-ORG/project-{code}
     - git -C C:\Repo\Project\Project-{CODE} push -u origin main

  3. External repo configuration (optional):
     - Edit: C:\Repo\Project\Project-{CODE}\client-config.json
     - Set: externalRepos.localPath to actual path/URL
```

---

## Error Scenarios

| Scenario | Message | Action |
|----------|---------|--------|
| C:\Repo\Project\ missing | "Workspace root C:\Repo\Project\ not found. Create it first or adjust path." | STOP |
| Project already exists | "Project-{CODE} already exists at C:\Repo\Project\Project-{CODE}. Use a different code." | STOP |
| Invalid code (special chars) | "Client code '{CODE}' contains invalid characters. Use alphanumeric + dash/underscore." | Re-ask Q1 |
| Empty code | "Client code is required." | Re-ask Q1 |
| Empty phase | "Phase description is required." | Re-ask Q3 |
| User cancels | "Cancelled. Just say 'new Project' again when ready." | STOP (no changes) |
| Git missing | WARN only | Create project anyway, warn user |
| PowerShell < 5.1 | WARN only | Create project anyway, warn user |

---

## Implementation Checklist

### Phase A: Skill File Creation
- [ ] Create skill definition file (Markdown or skill format)
- [ ] Define trigger patterns ("new Project" + variants)
- [ ] Set up interactive prompt flow

### Phase B: New Project Flow
- [ ] Implement setup mode detection (new vs clone)
- [ ] Implement Q1: Client code (validation + duplicate check)
- [ ] Implement Q2: Client name (optional with default)
- [ ] Implement Q3: Phase description (required)
- [ ] Implement confirmation (summary + "go ahead?")
- [ ] Implement pre-flight checks (C:\Repo\Project\, Git, PowerShell)

### Phase C: Project Creation
- [ ] Create Phase 1 folder with all 18 subfolders
- [ ] Create root folders (scripts, _templates, _documents, .claude, .github)
- [ ] Populate PHASES.md
- [ ] Populate README.md
- [ ] Populate Dashboard.md
- [ ] Populate client-config.json
- [ ] Populate .claude/settings.local.json
- [ ] Copy embedded templates to _templates/
- [ ] Copy embedded scripts to scripts/
- [ ] Copy CONTRIBUTING.md, requirements.txt, .github/

### Phase D: Git & Success
- [ ] Initialize git repo
- [ ] Install pre-commit hook
- [ ] Create initial commit
- [ ] Print success message + next steps

### Phase E: Clone Flow
- [ ] Ask for repo URL
- [ ] Print clone instructions

### Phase F: Error Handling
- [ ] All error scenarios from table above
- [ ] Graceful failure messages
- [ ] Cancel handling

### Phase G: Testing
- [ ] Test new project flow (3 questions)
- [ ] Test clone flow
- [ ] Verify all 18 folders created
- [ ] Verify all files present
- [ ] Verify git repo initialized
- [ ] Test error scenarios

---

## Key Implementation Notes

1. **Embedded Assets:** All templates/scripts must be embedded in skill at creation time
2. **No External Dependencies:** Skill works standalone (no Project-BDT lookup at runtime)
3. **Placeholder Substitution:** {CODE}, {NAME}, {DESCRIPTION} substituted in all templates
4. **Git Initialization:** Local repo only, no remote creation
5. **Pre-commit Hook:** Must be installed and functional
6. **Idempotent Checks:** Project-already-exists check before creation
7. **Graceful Warnings:** Git/PowerShell missing = warn, not fail
8. **Complete Output:** User gets fully functional project, day 1 ready

---

## Success Criteria

✅ Trigger detected ("new Project" variants)  
✅ User sees 4-question flow (mode + 3 params)  
✅ Project-{CODE} folder created at C:\Repo\Project\  
✅ All 18 Phase 1 subfolders present  
✅ All files present (config, README, Dashboard, scripts, templates)  
✅ Git repo initialized with initial commit  
✅ Pre-commit hook installed and working  
✅ Success message shown with next steps  
✅ Clone flow works (URL + instructions)  
✅ Error handling functional  
✅ No external dependencies required

---

## Ready to Build ✅

All specifications locked in. Implementation can begin immediately.

