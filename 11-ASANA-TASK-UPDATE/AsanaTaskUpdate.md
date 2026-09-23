# AsanaTaskUpdate — Unified Meeting Notes to Asana Sync

**Status:** ✅ **v1.0 PRODUCTION READY** (UAT Complete: 25/25 tests passed, 100% pass rate)

**Purpose:** Transform meeting notes into Asana task updates automatically — parse items with optional explicit references, fuzzy-match or direct task specification, execute actions (comments, due dates, assignments, completion), and post with team-wide deduplication.

---

## v1.0 Release Summary

### ✅ Validated Capabilities (UAT Completed 2026-09-16)

**Core Functionality (6/6 PASSED):**
- Natural language parsing ✅
- Explicit GID reference ✅
- Task name matching ✅
- Fuzzy search ✅
- Multiple items → single task (grouping) ✅
- Batch sync (multiple tasks) ✅

**Extended Actions (5/5 PASSED):**
- Set due date (explicit syntax) ✅
- Set due date (natural language) ✅
- Assign task (natural language) ✅
- Mark complete ✅
- Multiple actions per task ✅

**Safety & Preview (3/3 PASSED):**
- Dry-run mode (no changes) ✅
- Error handling (no match) ✅
- Ambiguous match (picker) ✅

**Error Handling & Configuration (6/6 PASSED):**
- Missing .env handling ✅
- GID override support ✅
- User-friendly error messages ✅
- Configuration validation ✅
- Multi-project support ✅
- Deduplication & file processing ✅

**Advanced Features (5/5 PASSED):**
- Custom field updates ✅
- Cross-project references ✅
- Recursive grouping ✅
- Advanced filtering ✅
- Stress test (1000+ items) ✅

**Test Results:** `Project-Nemesis/TEST-EXECUTION-LOG.md`  
**Findings & Roadmap:** `Project-Nemesis/TEST-FINDINGS-ENHANCEMENTS.md`

### v1.0 Critical Features

**Flexible Date Format Support:**
- Asana API accepts multiple date formats natively
- Supported: ISO 8601, US (MM/DD/YYYY), EU (DD/MM/YYYY), prose, abbreviated
- No custom parsing needed — pass to Asana, let API handle validation

**User-Friendly Error Messages:**
- When no tasks match: "No tasks match, nothing to update. If you feel this is a mistake, please use GID or task name to make perfectly clear."
- Guides users to explicit solutions (GID or exact task name)
- Reduces friction in error scenarios

### v1.1 Planned Enhancements (Weeks 3-4)

**Enhancement 1: Task Search on Error**
- When task not found, offer [SEARCH AGAIN] option
- Users enter partial task name/keyword (e.g., "US-1", "Code Review")
- System performs fuzzy search on refined query

**Enhancement 2: Search Narrowing in Picker**
- When multiple tasks match (10+ results), offer [NARROW] option
- Users enter partial task name to filter results
- Reduces 10 results → 2 results, then user picks

### Implementation

**Master Script Location:** `C:\Repo\Project\Skills\asana-sync-enhanced.py`

**How It Works (Simplified v1.0):**
1. Reads `.env` from project folder
2. Scans meeting notes files for `@task` references
3. Resolves task names to Asana task GIDs (fuzzy search or exact match)
4. Executes actions: comments, due dates, assignments, completion
5. Posts to Asana with team deduplication
6. Updates `.processed-notes.log`

---

**Use When:**
- You're capturing meeting notes and need to sync action items to Asana
- You want to link discussion points to existing tasks without manual re-entry
- You need one-click workflow: write notes → confirm matches → done
- You want extended Asana actions (set due dates, assign, mark complete)
- Your projects live in `C:\Repo\Projects\Project-{Name}` structure
- You're using Asana for task management with MCP or Python execution
- You need team coordination (prevent duplicate posts across users)

**Scope:** Meeting notes (natural language + optional syntax) → Asana task sync (parse, search, confirm, execute actions, post)

---

## Core Capabilities

### 1. **Hybrid Input Format**
- Natural language meeting notes (no special syntax required)
- Optional explicit syntax for precision: `GID:`, `Task:`, or `@task search:` / `@task name:"`
- System auto-detects and prioritizes explicit references

### 2. **Intelligent Line Parsing**
- Extracts bullet points (- item), numbered items (1. item)
- Identifies action items, discussion points, decisions
- Detects embedded GIDs, task names, and action directives
- Creates indexed list of {text, gid?, task_name?, actions?}

### 3. **Smart Task Matching**
- If GID provided → use directly (no search needed)
- If task name provided → search and use match
- If natural language → fuzzy search with confidence scoring
- Handles typos, partial names, abbreviations

### 4. **Per-Item Confirmation UI**
- Single match with high confidence → YES/NO/Manual GID
- Multiple matches or low confidence → numbered picker [1] [2] [3]...
- No match → SKIP / Manual GID / Create New / Rephrase
- User explicitly controls all actions

### 5. **Extended Asana Actions**
- **Default:** Add comment to task
- **Set due date:** `@action: set_due_date` → `@due_date: 2026-10-01`
- **Assign task:** `@action: assign` → `@assignee: user@domain.com`
- **Mark complete:** `@action: complete`
- **Custom fields:** `@action: set_custom_field` → `@field: Status` → `@value: In Progress`

### 6. **Duplicate Prevention & Grouping**
- Team-wide deduplication via `.processed-notes.log`
- Groups responses by task GID
- One comment per task (multiple items → one grouped comment)
- Prevents duplicate posts across all users

### 7. **Dual-Source Meeting Notes**
- **SharePoint:** Scans `{SHAREPOINT_SITE}/Client/Active Projects/` for Meeting Notes folders
- **Local Repo:** Scans `{LOCAL_NOTES_PATH}`
- Processes both sources, deduplicates across sources

### 8. **Execution Flexibility**
- **MCP Skill:** Native Claude Code integration (primary)
- **Python Script:** CLI execution option (secondary)
- Both support dry-run preview mode

---

## How It Works: 7-Phase Workflow

### Phase 1: Setup & Configuration Loading
```
User trigger: "sync meeting notes"
↓
System reads .env from project Phase folder
Loads: PROJECT_NAME, PROJECT_CODE, PHASE_NUMBER
Loads: SHAREPOINT_SITE, SHAREPOINT_PATH, LOCAL_NOTES_PATH
Loads: ASANA_PROJECT_GID (optional)
Loads: .processed-notes.log (deduplication tracking)
```

### Phase 1.5: Source Scanning & Deduplication
```
Scan SharePoint:
  Path: {SHAREPOINT_BASE_URL}{SHAREPOINT_SITE}/{SHAREPOINT_PATH}
  Look for: folders matching "*Meeting Notes*"
  Find: all .md files
  Check: against .processed-notes.log
  Keep: unprocessed files only

Scan Local Repo:
  Path: {LOCAL_NOTES_PATH}
  Find: all .md files
  Check: against .processed-notes.log
  Keep: unprocessed files only

Result: List of new meeting notes files to process
```

### Phase 2: Parse Line Items
```
Input: "- Q4 timeline confirmed
        - Technical requirements approved
        - Update project plan"
↓
Output: [{index: 1, text: "Q4 timeline confirmed"},
         {index: 2, text: "Technical requirements approved"},
         {index: 3, text: "Update project plan"}]
```

### Phase 3: Batch Asana Search
```
For each line item:
  Call: asana_search_tasks(item_text)
  Store: {item_text, matches[], selected_task_id}
```

### Phase 4: Build Interactive Confirmation UI
Shows all items at once with:
- **No match** → [SKIP] [Manual GID] [Create new] [Rephrase]
- **Single match** → [YES] [NO] [Create new] [Manual GID]
- **Multiple matches** → [Task 1] [Task 2] [Task 3] [SKIP] [Manual GID]

### Phase 5: Collect User Responses
User clicks through AskUserQuestion interface, selects option for each item, submits all at once.

### Phase 6: Process Responses
- SKIP → discard
- Selected match → use task GID
- Manual GID → use provided GID
- Task name → search and use matching task
- Create new → generate new Asana task with provided name

### Phase 7: Group & Post
```
Collect accepted items
Group by task GID
For each task:
  Combine multiple items into one comment
  Post via asana_create_task_story
Update .processed-notes.log with file metadata
```

**Output:**
```
✓ Processed 5 line items from 2026-09-16-Meeting-Notes.md
✓ Posted to 3 Asana tasks
✓ File marked as processed in .processed-notes.log
✓ Deduplication prevents re-processing by any user
```

---

## Quick Start

### Prerequisites
- Claude Code with Asana MCP connector access
- Claude Code with SharePoint/Microsoft 365 MCP connector access (for SharePoint notes)
- Project folder exists: `C:\Repo\Projects\Project-{Name}\Phase {N}`
- `.env` file configured in project Phase folder
- Asana workspace configured

### Step 1: Configure Project .env
Create `.env` in `C:\Repo\Projects\Project-{Name}\Phase {N}\.env`:

```env
# Project Configuration
PROJECT_NAME=TWG
PROJECT_CODE=TWG
PHASE_NUMBER=1

# SharePoint Meeting Notes Source
SHAREPOINT_SITE=ALTS-TWG
SHAREPOINT_BASE_URL=https://alphafmc183.sharepoint.com/sites/
SHAREPOINT_PATH=Client/Active Projects

# Local Repo Meeting Notes Source
LOCAL_NOTES_PATH=C:\Repo\Projects\Project-TWG\Phase 1\08 - Meeting Notes

# Asana Configuration
ASANA_PROJECT_GID=123456789
```

### Step 2: Trigger in Claude Code
```
sync meeting notes
```

Or explicitly specify source:
```
asana task update from sharepoint
asana task update from local
```

### Step 3: System Processes
1. Reads `.env` from project Phase folder
2. Scans both SharePoint and local sources for meeting notes files
3. Deduplicates (skips already-processed files)
4. Parses line items from unprocessed notes
5. Shows confirmation UI

### Step 4: Confirm Matches
System shows confirmation UI:
```
[File: 2026-09-16-Meeting-Notes.md from SharePoint]

[1] "Q4 implementation timeline confirmed"
    Detected: "Q4 Implementation" (GID: 123456)
    → [YES] [NO] [Manual GID]

[2] "Technical architecture approved"
    Detected: "Tech Architecture Review" (GID: 234567)
    → [YES] [NO] [Manual GID]

... (more items)
```

### Step 5: Submit & Done
- Click option for each item
- Click Submit
- System posts to Asana
- Marks file as processed
- Done!

---

## Approval Modes

AsanaTaskUpdate supports two modes for different workflows:

### Mode 1: Normal (Interactive) — DEFAULT
```
sync meeting notes
```

**Flow:**
1. Scans sources for unprocessed notes
2. Parses all line items
3. Searches Asana for matches
4. Shows confirmation UI:
   - Single matches → YES/NO/Manual GID
   - Multiple/uncertain matches → numbered picker
5. Waits for user confirmation
6. Executes actions after approval
7. Updates `.processed-notes.log`

**Use case:** Standard workflow with user oversight

---

### Mode 2: Dry-Run (Preview) — NO EXECUTION
```
sync meeting notes --preview
asana task update --dry-run
```

**Flow:**
1. Same as Normal mode (steps 1-4)
2. Shows all proposed actions (what WOULD be posted)
3. **No API calls to Asana**
4. **No updates to `.processed-notes.log`**
5. Returns to prompt (file remains unprocessed)

**Use case:** Verify matches before committing, debug task resolution

---

## Configuration

### .env Location (User-Configurable)

AsanaTaskUpdate auto-detects `.env` location or allow explicit specification:

**Default (Auto-Detect):**
```
sync meeting notes
```
Checks: Phase folder first → Project root → Error if not found

**Explicit Phase Folder:**
```
sync meeting notes --config phase
```
Looks only at: `C:\Repo\Projects\Project-{Name}\Phase {N}\.env`

**Explicit Project Root:**
```
sync meeting notes --config project
```
Looks only at: `C:\Repo\Projects\Project-{Name}\.env`

### .env Setup

Place `.env` in either Phase folder or Project root (not both):

```env
# Project Configuration
PROJECT_NAME=TWG
PROJECT_CODE=TWG
PHASE_NUMBER=1

# SharePoint Meeting Notes Source
SHAREPOINT_SITE=ALTS-TWG
SHAREPOINT_BASE_URL=https://alphafmc183.sharepoint.com/sites/
SHAREPOINT_PATH=Client/Active Projects

# Local Repo Meeting Notes Source
LOCAL_NOTES_PATH=C:\Repo\Projects\Project-TWG\Phase 1\08 - Meeting Notes

# Asana Configuration
ASANA_PROJECT_GID=123456789
```

**Required variables:**

| Variable | Purpose | Example |
|----------|---------|---------|
| `PROJECT_NAME` | Project identifier | TWG |
| `PROJECT_CODE` | Short code for SharePoint mapping | TWG |
| `PHASE_NUMBER` | Phase number (if Phase-level .env) | 1 |
| `SHAREPOINT_SITE` | SharePoint site name | ALTS-TWG |
| `SHAREPOINT_BASE_URL` | SharePoint domain | https://alphafmc183.sharepoint.com/sites/ |
| `SHAREPOINT_PATH` | Path within site | Client/Active Projects |
| `LOCAL_NOTES_PATH` | Local repo meeting notes folder | C:\Repo\Projects\Project-TWG\Phase 1\08 - Meeting Notes |
| `ASANA_PROJECT_GID` | Asana project ID (optional) | 123456789 |

### Meeting Notes Sources
System scans **both** sources in parallel:

1. **SharePoint:** `{SHAREPOINT_BASE_URL}{SHAREPOINT_SITE}/{SHAREPOINT_PATH}/**/Meeting Notes/*`
2. **Local Repo:** `{LOCAL_NOTES_PATH}/*`

### Deduplication
To prevent multiple users from posting the same notes:
- System maintains `.processed-notes.log` in each Phase folder
- Tracks: filename, source, hash, processed timestamp
- Skips files already in log (prevents duplicate Asana posts)

### Project Structure
```
C:\Repo\Projects\
├── Project-TWG/
│   ├── Phase 1/
│   │   ├── .env                           ← Configuration (required)
│   │   ├── .processed-notes.log           ← Deduplication log (auto-created)
│   │   ├── 00 - Project Overview/
│   │   ├── ...
│   │   └── 08 - Meeting Notes/            ← Local meeting notes
│   ├── Phase 2/
│   │   ├── .env
│   │   └── ...
│   └── ...
├── Project-BDT/
│   └── ...
└── Project-{Name}/
    └── ...
```

### Asana Integration
- Uses Asana MCP connector (built-in)
- Searches tasks in ASANA_PROJECT_GID (if set) or workspace-wide

### SharePoint Integration
- Uses SharePoint/Microsoft 365 MCP connector
- Searches for folders matching `*Meeting Notes*` pattern
- No additional authentication needed (uses existing MCP credentials)

---

## Handling Edge Cases

### No Match Found
User sees:
```
[1] SKIP this item
[2] Enter TASK ID
[3] Create new task: "Item name here"
[Other] Rephrase and search again
```

### Multiple Matches
User sees:
```
[1] "Q4 Planning" (GID: 123456)
[2] "Q4 Timeline" (GID: 789012)
[3] "Q4 Review" (GID: 345678)
[4] SKIP this item
[Other] Manual GID or rephrase
```

### User Provides Manual GID
System uses GID directly without further search (e.g., `1215428532115696`)

### Create New Task
System prompts for task name, creates in Asana, uses new task GID for posting

### Multiple Items → Same Task
Items grouped into one comment:
```
Task "Q4 Planning" (GID: 123456)
Updated with:
  - Q4 implementation timeline confirmed
  - Timeline schedule finalized
  (Posted as one comment, not two)
```

---

## System Implementation

### Required Asana Tools
- `asana_search_tasks` — find tasks by text
- `asana_create_task_story` — post comment to task
- `asana_create_task` — create new task on demand

### File Operations
- Read: user input from chat/markdown
- Write: meeting notes file to `08 - Meeting Notes/`

### UI Components
- `AskUserQuestion` — per-item confirmation picker
- Text feedback for each phase

### Workflow Entry Points
Recognized patterns:
- "New session meeting notes {PROJECT}"
- "meeting notes for {PROJECT}"
- "{PROJECT} meeting notes"
- "notes: {PROJECT}"
- Any text with "meeting notes" + project name

---

## Best Practices

### Writing Effective Meeting Notes

1. **Be Descriptive in Line Items**
   - ❌ "Discussed timeline"
   - ✅ "Q4 implementation timeline confirmed"
   - ✅ "Database schema migration approved — ready for Phase 2"
   - Helps fuzzy matching and creates meaningful comments

2. **Use Explicit References When Certain**
   - ❌ "We talked about the API"
   - ✅ "1234567890: API design finalized"
   - ✅ "Task: Database Migration - schema approved"
   - Direct references bypass search and execute faster

3. **Group Related Items Logically**
   - Keep items for same task together
   - Improves readability and deduplication
   - System will group them in comments anyway, but logical grouping helps review

4. **One Action Per Item (or Related Actions)**
   - ✅ One item = one primary note
   - ✅ Multiple actions = same item with multiple `@action:` directives
   - ❌ Mixing unrelated actions in one item causes ambiguity

5. **Review Matches Before Confirming**
   - Read the detected task name carefully
   - When picker shows multiple matches, select the MOST SPECIFIC one
   - Use "Manual GID" if you know the exact task
   - Use "SKIP" if unsure — don't post to wrong task

6. **Use Dry-Run Before Automating**
   - First sync: run with `--preview` (dry-run mode)
   - Review proposed matches and actions
   - Then run without preview once confident
   - Especially important before setting up hooks

7. **Validate Task Names Exist**
   - Check that task explicitly referenced exists in Asana
   - System searches but may not find partial/informal names
   - Better to use GID if you know it

8. **Keep Meeting Notes Focused Per Project**
   - One meeting notes file per project (or per section if cross-project)
   - If multi-project meeting: create separate sections
   - Prevents accidental posts to wrong project tasks

### Execution & Team Coordination

9. **Leverage Deduplication**
   - Deduplication prevents duplicate posts across team
   - Multiple users can run sync on same file (second user sees "already processed")
   - Don't manually re-run or clear `.processed-notes.log` unless necessary

10. **Monitor Audit Logs**
   - Check logs after first few syncs to verify correct behavior
   - Look for: correct tasks found, correct actions executed, correct assignees
   - Verify due dates are in ISO format (`YYYY-MM-DD`)

11. **Use Hooks for Consistent Automation**
   - Set up Claude Code hook for auto-preview on file save
   - Reduces manual sync calls
   - Start with dry-run hook, graduate to auto-execute when confident

12. **Action Syntax Should Match Task Context**
   - `@action: set_due_date` for timeline-sensitive tasks
   - `@action: assign` for ownership transfer
   - `@action: complete` only for truly finished work
   - `@action: set_custom_field` for status tracking

### Troubleshooting & Support

13. **When Matches Are Wrong**
   - Use picker to select correct task from list
   - Or provide manual GID if you know it
   - Or rephrase and re-search
   - Never skip if wrong — the meeting note data will be lost

14. **When No Matches Found**
   - Check task name spelling in Asana
   - Try broader term: "Q4" instead of "Q4 Planning"
   - Check that task exists in the right workspace
   - If none work, provide manual GID or create new task

15. **Clear `.processed-notes.log` Carefully**
   - Only delete if reprocessing old file intentionally
   - Clearing allows duplicate Asana posts (defeating deduplication)
   - Use case: correcting wrong posts from previous run

---

## Extended Asana Actions

Beyond comments, AsanaTaskUpdate can execute additional Asana actions on matched tasks.

### Action: Add Comment (DEFAULT)
Implicit — all meeting note text becomes a comment unless other actions specified.

```markdown
- Q4 timeline confirmed

(No @action specified → posted as comment to matched task)
```

**Result:** Note text added as comment to task in Asana.

---

### Action: Set Due Date

```markdown
- Database migration approved
  @action: set_due_date
  @due_date: 2026-10-15
```

**Format:** ISO 8601 (`YYYY-MM-DD`)

**Result:** Task due date updated to October 15, 2026.

---

### Action: Assign Task

```markdown
1234567890: API Documentation
  @action: assign
  @assignee: jane.doe@company.com
```

**Format:** Email address of Asana workspace member

**Result:** Task assigned to Jane Doe (must have project access).

---

### Action: Mark Complete

```markdown
- Performance testing completed
  @action: complete
```

**Result:** Task marked as complete in Asana.

---

### Action: Set Custom Field

```markdown
- Sprint review ready
  @action: set_custom_field
  @field: Status
  @value: In Progress
```

**Parameters:**
- `@field:` — Custom field name (must exist in project)
- `@value:` — Value to set (must match field type: text, dropdown, number, etc.)

**Result:** Custom field updated on task.

---

### Combining Actions

Multiple actions on same item:

```markdown
Task: Q4 Planning
  @action: set_due_date
  @due_date: 2026-10-01
  @action: assign
  @assignee: bob.smith@company.com
  Q4 timeline finalized, Bob taking ownership.
```

**Result:**
- Comment added: "Q4 timeline finalized, Bob taking ownership."
- Due date set to 2026-10-01
- Task assigned to Bob Smith

---

## Claude Code Hook Integration

Automate task sync when meeting notes are saved.

### Setup

Add to `.claude/settings.json` in project root:

```json
{
  "hooks": [
    {
      "on": "file_write",
      "match": "**/08 - Meeting Notes/**/*.md",
      "run": "sync meeting notes --preview"
    }
  ]
}
```

**Behavior:**
- Each time you save a markdown file in `08 - Meeting Notes/`
- Hook runs `sync meeting notes --preview` (dry-run mode by default)
- Shows what would be posted in console
- User can then manually trigger `sync meeting notes` to execute

### Variant: Auto-Execute (Advanced)

```json
{
  "on": "file_write",
  "match": "**/08 - Meeting Notes/**/*.md",
  "run": "sync meeting notes --auto"
}
```

**Behavior:**
- Auto-executes sync (no preview, no confirmation)
- Best for trusted, well-tested workflows
- **Use with caution** — can post without review

---

## Logging & Audit Trail

Every sync operation is logged with full details for accountability.

### Log Location
- **MCP Skill:** Console output + Claude Code session transcript
- **Python Script:** `scripts/asana-sync.log`

### Log Format
```
[2026-09-16 14:32:15] SYNC START
[2026-09-16 14:32:15] Source: SharePoint + Local
[2026-09-16 14:32:16] User: jeff.rowell@alphafmc.com
[2026-09-16 14:32:16] File: 2026-09-16-Meeting-Notes.md (SharePoint)
[2026-09-16 14:32:17] Parsed: 5 line items
[2026-09-16 14:32:18] Searched: 5 Asana tasks
[2026-09-16 14:32:22] Confirmed: 4 items (1 skipped)
[2026-09-16 14:32:23] ACTION: Comment → Task 123456 (Q4 Planning)
[2026-09-16 14:32:24] ACTION: Set Due Date → Task 123456 (2026-10-01)
[2026-09-16 14:32:25] ACTION: Comment → Task 234567 (Tech Review)
[2026-09-16 14:32:26] ACTION: Assign → Task 234567 (jane.doe@company.com)
[2026-09-16 14:32:27] RESULT: Posted to 2 tasks
[2026-09-16 14:32:28] File marked processed: 2026-09-16-Meeting-Notes.md
[2026-09-16 14:32:28] SYNC COMPLETE
```

### Audit Fields
- **Timestamp** — When operation ran
- **User** — Who executed sync
- **Source** — Which source(s) scanned
- **File** — Which meeting notes file processed
- **Items Parsed** — Line count
- **Items Confirmed** — User approvals
- **Actions Executed** — Each action with task ID + details
- **Status** — Success / Partial / Failed
- **Hash** — File fingerprint for deduplication verification

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **No .env found** | Create `.env` in `C:\Repo\Projects\Project-{Name}\Phase {N}\` with all required variables |
| **SharePoint path not found** | Verify SHAREPOINT_SITE and SHAREPOINT_PATH are correct; use SharePoint MCP connector to verify access |
| **Local notes path not found** | Verify LOCAL_NOTES_PATH exists and contains meeting notes files |
| **No meeting notes found** | Check both SharePoint and local folders; verify files have `.md` extension |
| **File already processed** | File is in `.processed-notes.log`; this prevents duplicate posting (intentional) |
| **Clear processed log** | Delete `.processed-notes.log` to reprocess files (use with caution) |
| **No Asana matches** | Try "Manual GID" if you know the task ID; verify ASANA_PROJECT_GID is set correctly |
| **Wrong task matched** | Select [NO], try "Manual GID" with correct task GID |
| **Asana won't connect** | Verify Asana MCP connector is configured in Claude Code settings |
| **Multiple matches confusing** | Pick the most specific match; if unsure, say [NO] and use [Manual GID] with exact task ID |

---

## Examples

### Example 1: Natural Language Notes (Fuzzy Search)

**SharePoint file: `2026-09-16-Status-Meeting.md`**
```markdown
- Q4 timeline confirmed
- Technical requirements approved
- Update project roadmap
```

**User Command:**
```
sync meeting notes
```

**System Flow:**
1. Parses: 3 items (all natural language)
2. Searches Asana: finds matches
3. Shows confirmation UI:
   - Item 1: Single match → [YES] [NO] [Manual GID]
   - Item 2: Multiple matches → [1] Q4 Planning [2] Q4 Review [3] SKIP...
   - Item 3: No match → [SKIP] [Manual] [Create New]
4. User confirms selections
5. Posts comments to 3 tasks

**Result:** ✓ 3 items processed, comments posted

---

### Example 2: Mixed Syntax (Explicit + Natural Language)

**SharePoint file: `2026-09-16-Architecture-Review.md`**
```markdown
- Q4 timeline confirmed
  (natural language — will fuzzy search)

- 1234567890: API design finalized
  (GID provided — uses directly, no search)

- Task: Database Schema Migration - approved
  (task name provided — searches for exact match)

- 9876543210: Client feedback integration
  @action: assign
  @assignee: jane.doe@company.com
  (GID + action — assigns task to Jane)
```

**User Command:**
```
sync meeting notes
```

**System Flow:**
1. Item 1: Fuzzy search "Q4 timeline confirmed" → finds Q4 Planning task
2. Item 2: Uses GID 1234567890 directly (no search)
3. Item 3: Searches for "Database Schema Migration" → finds match
4. Item 4: Uses GID 9876543210, detects assign action
5. Shows picker for Item 1 if multiple matches
6. User confirms
7. Posts comments + assignments

**Result:** ✓ 4 items processed, 1 task assigned

---

### Example 3: Extended Actions with Due Dates

**Local file: `2026-09-16-Planning.md`**
```markdown
- Q4 Implementation Timeline
  @action: set_due_date
  @due_date: 2026-10-01
  Timeline finalized, ready for Phase 2.

- 5678901234: Stakeholder Communication
  @action: assign
  @assignee: bob.smith@company.com
  @action: set_due_date
  @due_date: 2026-09-25
  Bob leading outreach to clients.

- Database Migration - Schema Approved
  @action: complete
  All approvals done, ready to implement.
```

**User Command:**
```
sync meeting notes
```

**System Flow:**
1. Item 1: Searches for Q4, finds match, sets due date to 2026-10-01, posts comment
2. Item 2: Uses GID 5678901234, assigns to Bob, sets due date to 2026-09-25, posts comment
3. Item 3: Searches for "Database Migration", marks task complete, posts comment

**Audit Log Result:**
```
[ACTION: Comment] → Task "Q4 Implementation" (GID 1111111111111111)
[ACTION: Set Due Date] → 2026-10-01 on Task "Q4 Implementation"
[ACTION: Comment] → Task "Stakeholder Communication" (GID 5678901234)
[ACTION: Assign] → bob.smith@company.com on Task "Stakeholder Communication"
[ACTION: Set Due Date] → 2026-09-25 on Task "Stakeholder Communication"
[ACTION: Comment] → Task "Database Migration" (GID 2222222222222222)
[ACTION: Complete] → Task "Database Migration"
```

**Result:** ✓ 3 items processed, 3 tasks updated with actions

---

### Example 4: Dry-Run Preview

**User Command:**
```
sync meeting notes --preview
```

**Output (No Changes):**
```
[DRY-RUN MODE - No Asana changes will be made]

File: 2026-09-16-Architecture-Review.md (SharePoint)
Parsed: 7 items

Proposed Actions:
  [Item 1] "API design finalized" 
    → Would post comment to: API Design (GID: 1234567890)
  
  [Item 2] "Database schema approved"
    → Multiple matches:
        [1] Database Migration (GID: 2222222222222222)
        [2] Schema Review (GID: 3333333333333333)
    → Would require user selection

  [Item 3] "Security review completed"
    → No match found
    → Would require: SKIP / Manual GID / Create New

[DRY-RUN COMPLETE - No changes made]
[File remains unprocessed - safe to retry]
```

**Then run normally:**
```
sync meeting notes
```

**Result:** ✓ Shows real confirmation UI with dry-run verified

---

### Example 5: Multi-User Deduplication

**Scenario:**
- Developer A: `sync meeting notes` on 2026-09-16-Architecture-Review.md
- PM B (5 min later): `sync meeting notes` in same Phase folder

**Dev A's Execution:**
```
sync meeting notes
Scanned: SharePoint + Local
Found: 2026-09-16-Architecture-Review.md (SharePoint)
Processed: 7 items → 5 tasks updated
Updated .processed-notes.log with file hash
```

**PM B's Execution:**
```
sync meeting notes
Scanned: SharePoint + Local
Found: 2026-09-16-Architecture-Review.md (SharePoint)
Checked .processed-notes.log
Result: FILE ALREADY PROCESSED
Status: 0 new items (1 file skipped)
No duplicate posts to Asana
```

**Audit Logs:**
```
Dev A: [2026-09-16 14:32:28] SYNC COMPLETE | File processed | 5 tasks updated
PM B:  [2026-09-16 14:37:15] FILE SKIPPED | Already processed by Dev A | 0 tasks updated
```

**Result:** ✓ No duplicate posts, team automatically coordinated

---

## File Output

### Meeting Notes File
**Path:** `Project-{Name}/Phase {N}/08 - Meeting Notes/{YYYY-MM-DD}-Meeting-Notes.md`

**Content:**
```markdown
# Meeting Notes - 2026-09-16

**Project:** TWG  
**Phase:** 1  
**Date:** 2026-09-16  
**Processed via:** Nemesis Project

## Parsed Items

1. Q4 timeline confirmed → Task: Q4 Planning (GID: 123456)
2. Technical requirements approved → Task: Technical Review (GID: 234567)
3. Update project plan → Task: Project Management (GID: 345678)

## Full Notes

Met with team on 2026-09-16.

Discussed:
- Q4 timeline confirmed
- Technical requirements approved
- Ready for Phase 2

Action items:
- Update project plan
- Schedule review meeting

---
*Auto-generated by Nemesis Project*
```

---

## Advanced: Extending Nemesis

Nemesis is designed for extensibility:

### Custom Project Detection
Add patterns to recognize your client names automatically

### Email Integration (Optional)
Route meeting notes via email:
- Send to: `meetingNotes@domain.com`
- Subject: `[TWG] Q4 Meeting Notes`
- System processes like typed notes

### Batch Processing
Process multiple meeting notes files in one run (future enhancement)

### Custom Asana Fields
Extend posting logic to set priority, due date, or other fields

---

## Related Skills

- **[asana-bulk-user-story-tasks](asana-bulk-user-story-tasks.md)** — Batch create new Asana task hierarchies from user stories

## Archived Skills

- **asana-meeting-notes-sync** (archived) — Legacy skill with similar functionality. Kept for historical reference. AsanaTaskUpdate supersedes it with hybrid syntax support, extended actions, and team deduplication.

---

## Support & Documentation

**Full Documentation:** See `C:\Repo\NemesisProject\` for:
- `QUICK_START.txt` — 2-minute beginner guide
- `MEETING-NOTES-WORKFLOW.md` — Complete workflow details
- `SYSTEM-PROMPT-MEETING-NOTES.md` — Technical implementation
- `docs/TROUBLESHOOTING.md` — Common issues & solutions

**Questions?** Check [C:\Repo\NemesisProject\README.md](C:\Repo\NemesisProject\README.md)

---

**Ready to use?** Type naturally in Claude Code: `meeting notes {PROJECT}` and follow the confirmation prompts.
