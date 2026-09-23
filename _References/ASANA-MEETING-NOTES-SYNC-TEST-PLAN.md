# Asana Meeting Notes Sync — Test Plan

**Skill:** `asana-meeting-notes-sync.md`  
**Component Under Test:** Meeting notes parser + task synchronizer  
**Scope:** All 4 operating modes, task resolution, actions, and error handling  
**Duration:** ~45 minutes for full suite

---

## Pre-Test Setup

### Step 1: Create Test Project in Asana

1. Open **asana.com** → your workspace
2. Create a new test project: **"[TEST] Claude Sync"**
3. Create 3 sections:
   - `Backlog`
   - `In Progress`
   - `Completed`
4. Add 5 test tasks in `Backlog` section:
   - **TS-1:** "API Authentication Layer"
   - **TS-2:** "Database Schema Migration"
   - **TS-3:** "Frontend Redesign Review"
   - **TS-4:** "Performance Optimization"
   - **TS-5:** "Client Feedback Integration"

5. Get your **Project GID** from the URL:
   - URL: `https://app.asana.com/0/WORKSPACE_GID/PROJECT_GID/list`
   - Copy the `PROJECT_GID`

### Step 2: Create Test Project Directory

```bash
mkdir -p C:\Repo\Project\test-asana-sync
cd C:\Repo\Project\test-asana-sync

mkdir -p scripts
mkdir -p "08 - Meeting Notes"
```

### Step 3: Copy Script & Create Config

```bash
# Copy from TWG or create asana-sync-enhanced.py (see template below if needed)
cp ../Project-TWG/scripts/asana-sync-enhanced.py ./scripts/

# Create .env with your test project GID
cat > .env << 'EOF'
ASANA_PAT=your-personal-access-token
ASANA_PROJECT_GID=your-test-project-gid
EOF

# Add to .gitignore
echo ".env" >> .gitignore
```

### Step 4: Verify Setup

```bash
python scripts/asana-sync-enhanced.py --help
# Should show all available flags

python scripts/asana-sync-enhanced.py --dry-run
# Should output: "No @task references found" (no notes yet)
```

---

## Test Cases

### TEST 1: Basic Dry-Run (No Changes)

**Purpose:** Verify script runs without side effects

**Steps:**
1. Create test file: `08 - Meeting Notes/2026-09-16-test-basic.md`
   ```markdown
   # Test Meeting - Basic Dry-Run

   @task name:"API Authentication Layer"

   We discussed the authentication approach. Standard OAuth 2.0 flow.
   ```

2. Run:
   ```bash
   python scripts/asana-sync-enhanced.py --dry-run
   ```

**Expected Output:**
```
Found 1 @task reference(s)
---
Proposal 1:
  Task: API Authentication Layer (TS-1)
  Action: Add comment
  Comment: "We discussed the authentication approach. Standard OAuth 2.0 flow."

Dry-run mode — no changes made.
```

**Verification:**
- ✅ Task found in Asana
- ✅ Comment content extracted correctly
- ✅ No API calls (dry-run)
- ✅ Log file created at `scripts/asana-sync.log`

---

### TEST 2: Manual Mode with Approval

**Purpose:** Verify interactive approval workflow

**Steps:**
1. Create test file: `08 - Meeting Notes/2026-09-16-test-manual.md`
   ```markdown
   # Sprint Planning - Manual Approval Test

   @task name:"Database Schema Migration"

   Schema finalized. Ready for implementation.
   ```

2. Run:
   ```bash
   python scripts/asana-sync-enhanced.py
   ```

3. At prompt `Proceed? (yes/no)`, answer: **`yes`**

**Expected Output:**
```
Found 1 @task reference(s)
---
Proposal 1:
  Task: Database Schema Migration (TS-2)
  Action: Add comment
  Comment: "Schema finalized. Ready for implementation."

Proceed? (yes/no): yes
✓ Synced: Database Schema Migration
Execution complete: 1 task synced.
```

**Verification:**
- ✅ Proposals shown before execution
- ✅ User approval gate works
- ✅ Task updated in Asana (check UI)
- ✅ Comment appears on TS-2

---

### TEST 3: Auto-Approve Mode (No Prompt)

**Purpose:** Verify `--no-prompt` flag for automation

**Steps:**
1. Create test file: `08 - Meeting Notes/2026-09-16-test-autoprompt.md`
   ```markdown
   # Standup - Auto Approval Test

   @task name:"Frontend Redesign Review"

   Mockups approved by design team. Ready for dev discussion.
   ```

2. Run:
   ```bash
   python scripts/asana-sync-enhanced.py --no-prompt
   ```

**Expected Output:**
```
Found 1 @task reference(s)
---
Proposal 1:
  Task: Frontend Redesign Review (TS-3)
  Action: Add comment
  Comment: "Mockups approved by design team. Ready for dev discussion."

Executing (auto-approve mode)...
✓ Synced: Frontend Redesign Review
Execution complete: 1 task synced.
```

**Verification:**
- ✅ No approval prompt
- ✅ Auto-executes immediately
- ✅ Suitable for Claude Code hooks
- ✅ Comment appears on TS-3

---

### TEST 4: Set Due Date Action

**Purpose:** Verify `@action: set_due_date` functionality

**Steps:**
1. Create test file: `08 - Meeting Notes/2026-09-16-test-due-date.md`
   ```markdown
   # Project Review - Due Date Test

   @task name:"Performance Optimization"
   @action: set_due_date
   @due_date: 2026-09-30

   Performance benchmarks need to be met by end of Q3.
   ```

2. Run:
   ```bash
   python scripts/asana-sync-enhanced.py
   ```

3. Answer `yes` at prompt

**Expected Output:**
```
Found 1 @task reference(s)
---
Proposal 1:
  Task: Performance Optimization (TS-4)
  Action: Set due date
  Due date: 2026-09-30
  Comment: "Performance benchmarks need to be met by end of Q3."

Proceed? (yes/no): yes
✓ Synced: Performance Optimization
Execution complete: 1 task synced.
```

**Verification:**
- ✅ Due date set on TS-4 (check Asana UI)
- ✅ Comment also added
- ✅ Format validation (ISO 8601)
- ✅ Log entry shows both action and comment

---

### TEST 5: Mark Complete Action

**Purpose:** Verify `@action: complete` functionality

**Steps:**
1. Create test file: `08 - Meeting Notes/2026-09-16-test-complete.md`
   ```markdown
   # Completion Check - Complete Action Test

   @task name:"Client Feedback Integration"
   @action: complete

   All feedback items addressed. UAT sign-off received.
   ```

2. Before running, verify TS-5 is in `Backlog` (not completed)

3. Run:
   ```bash
   python scripts/asana-sync-enhanced.py --no-prompt
   ```

**Expected Output:**
```
Found 1 @task reference(s)
---
Proposal 1:
  Task: Client Feedback Integration (TS-5)
  Action: Mark complete
  Comment: "All feedback items addressed. UAT sign-off received."

Executing (auto-approve mode)...
✓ Synced: Client Feedback Integration
Execution complete: 1 task synced.
```

**Verification:**
- ✅ TS-5 marked complete in Asana
- ✅ Comment appears on task
- ✅ Task moves to `Completed` section (or similar)

---

### TEST 6: Multiple Tasks in One Meeting

**Purpose:** Verify batch sync of multiple tasks

**Steps:**
1. Create test file: `08 - Meeting Notes/2026-09-16-test-batch.md`
   ```markdown
   # Weekly Standup - Multi-Task Test

   @task name:"API Authentication Layer"

   Authentication flow approved. Moving to dev.

   @task name:"Database Schema Migration"
   @action: set_due_date
   @due_date: 2026-10-01

   Schema review complete. Timeline confirmed.

   @task name:"Frontend Redesign Review"
   @action: complete

   Design approved. Ready for implementation.
   ```

2. Reset TS-3 to `Backlog` if it was completed

3. Run:
   ```bash
   python scripts/asana-sync-enhanced.py --dry-run
   ```

**Expected Output:**
```
Found 3 @task reference(s)
---
Proposal 1:
  Task: API Authentication Layer (TS-1)
  Action: Add comment
  ...

Proposal 2:
  Task: Database Schema Migration (TS-2)
  Action: Set due date
  Due date: 2026-10-01
  ...

Proposal 3:
  Task: Frontend Redesign Review (TS-3)
  Action: Mark complete
  ...

Dry-run mode — no changes made.
```

**Verification:**
- ✅ All 3 tasks recognized
- ✅ Different actions per task understood
- ✅ Order preserved
- ✅ No changes (dry-run)

---

### TEST 7: Task Resolution - Exact Name Match

**Purpose:** Verify `@task name:"exact"` behavior

**Steps:**
1. Create test file: `08 - Meeting Notes/2026-09-16-test-exact-match.md`
   ```markdown
   # Exact Match Test

   @task name:"API Authentication Layer"

   Using exact task name.
   ```

2. Run:
   ```bash
   python scripts/asana-sync-enhanced.py --dry-run
   ```

**Expected Output:**
```
Found 1 @task reference(s)
...
Proposal 1:
  Task: API Authentication Layer (TS-1)
  Action: Add comment
  Comment: "Using exact task name."
...
```

**Verification:**
- ✅ Task found on first try
- ✅ Exact name match successful
- ✅ No ambiguity

---

### TEST 8: Task Resolution - Fuzzy Search Match

**Purpose:** Verify `@task search:"keyword"` behavior

**Steps:**
1. Create test file: `08 - Meeting Notes/2026-09-16-test-fuzzy.md`
   ```markdown
   # Fuzzy Search Test

   @task search:"Authentication"

   Using fuzzy search for authentication task.
   ```

2. Run:
   ```bash
   python scripts/asana-sync-enhanced.py --dry-run
   ```

**Expected Output:**
```
Found 1 @task reference(s)
...
Proposal 1:
  Task: API Authentication Layer (TS-1) [FUZZY MATCH]
  Action: Add comment
  Comment: "Using fuzzy search for authentication task."
...
```

**Verification:**
- ✅ Fuzzy search finds task
- ✅ Contains keyword "Authentication"
- ✅ Marked as `FUZZY MATCH` (helps distinguish from exact)

---

### TEST 9: Interactive Mode - Ambiguous Match

**Purpose:** Verify `--interactive` mode when multiple tasks match

**Steps:**
1. Create test file: `08 - Meeting Notes/2026-09-16-test-ambiguous.md`
   ```markdown
   # Ambiguous Search Test

   @task search:"Review"

   Using a generic keyword that matches multiple tasks.
   ```

2. Run:
   ```bash
   python scripts/asana-sync-enhanced.py --interactive
   ```

**Expected Output:**
```
Found 1 @task reference(s)
...
Ambiguous match for "Review": 2 tasks found
  1. Frontend Redesign Review (TS-3)
  2. Client Feedback Integration (TS-5) [contains "review"]

Select task (1-2): 
```

3. Enter `1`

**Expected Continuation:**
```
Select task (1-2): 1
Selected: Frontend Redesign Review (TS-3)

Proceed? (yes/no): yes
✓ Synced: Frontend Redesign Review
```

**Verification:**
- ✅ Multiple matches detected
- ✅ User presented with choices
- ✅ User can select correct task
- ✅ Sync proceeds with selected task

---

### TEST 10: Task Not Found - Error Handling

**Purpose:** Verify graceful error when task doesn't exist

**Steps:**
1. Create test file: `08 - Meeting Notes/2026-09-16-test-not-found.md`
   ```markdown
   # Not Found Test

   @task name:"This Task Does Not Exist"

   This should trigger an error.
   ```

2. Run:
   ```bash
   python scripts/asana-sync-enhanced.py --dry-run
   ```

**Expected Output:**
```
Found 1 @task reference(s)
...
Proposal 1:
  Task: [NOT FOUND] "This Task Does Not Exist"
  Status: ERROR — Task not found in project

Dry-run mode — no changes made.
```

**Verification:**
- ✅ Error detected gracefully
- ✅ Helpful error message
- ✅ No crashes
- ✅ Script continues (doesn't halt on error)

---

### TEST 11: Verbose Mode - Debug Output

**Purpose:** Verify `--verbose` flag provides debug details

**Steps:**
1. Create test file: `08 - Meeting Notes/2026-09-16-test-verbose.md`
   ```markdown
   # Verbose Test

   @task name:"API Authentication Layer"

   Testing verbose debug output.
   ```

2. Run:
   ```bash
   python scripts/asana-sync-enhanced.py --verbose --dry-run
   ```

**Expected Output (more detailed):**
```
[DEBUG] Scanning folder: 08 - Meeting Notes
[DEBUG] Found 1 markdown file(s)
[DEBUG] Parsing: 2026-09-16-test-verbose.md
[DEBUG] Extracted @task reference: name="API Authentication Layer"
[DEBUG] Searching Asana for task...
[DEBUG] API call: GET /api/1.0/projects/{PROJECT_GID}/tasks?q=API+Authentication+Layer
[DEBUG] Found 1 result(s)
[DEBUG] Task GID: TS-1-GID-123456789
[DEBUG] Action: Add comment
[DEBUG] Comment text: "Testing verbose debug output."

Proposal 1:
  Task: API Authentication Layer (TS-1)
  Action: Add comment
  Comment: "Testing verbose debug output."

Dry-run mode — no changes made.
```

**Verification:**
- ✅ Debug timestamps visible
- ✅ API calls logged
- ✅ Search parameters shown
- ✅ GID resolution shown

---

### TEST 12: Audit Log Verification

**Purpose:** Verify all changes logged correctly

**Steps:**
1. Run any sync operation that makes changes:
   ```bash
   python scripts/asana-sync-enhanced.py --no-prompt
   ```

2. Check log file:
   ```bash
   cat scripts/asana-sync.log
   # Or for live tail:
   tail -f scripts/asana-sync.log
   ```

**Expected Log Format:**
```
2026-09-16T14:32:15 | SYNC_COMPLETE | TS-1-GID-123 | API Authentication Layer | SUCCESS | Added comment: "We discussed..."
2026-09-16T14:32:45 | SYNC_COMPLETE | TS-2-GID-456 | Database Schema Migration | SUCCESS | Set due date to 2026-10-01
2026-09-16T14:33:12 | SYNC_COMPLETE | TS-3-GID-789 | Frontend Redesign Review | SUCCESS | Marked complete
2026-09-16T14:33:45 | SYNC_FAILED | UNKNOWN | This Task Does Not Exist | ERROR | Task not found in project
```

**Verification:**
- ✅ All syncs logged with timestamps
- ✅ Task GID, name, action visible
- ✅ Success/failure status shown
- ✅ Error details captured

---

### TEST 13: Different Project GID (Multi-Project)

**Purpose:** Verify `--project-gid` flag switches to different project

**Steps:**
1. Create second test project in Asana: **"[TEST] Claude Sync #2"**
2. Copy one test task from Project 1, note the new Project 2 GID

3. Create test file: `08 - Meeting Notes/2026-09-16-test-multi-project.md`
   ```markdown
   # Multi-Project Test

   @task name:"API Authentication Layer"

   This note should sync to Project 2.
   ```

4. Run with explicit project GID:
   ```bash
   python scripts/asana-sync-enhanced.py --project-gid YOUR_PROJECT_2_GID --dry-run
   ```

**Expected Output:**
```
Connecting to Asana project: YOUR_PROJECT_2_GID
Found 1 @task reference(s)
...
Proposal 1:
  Task: API Authentication Layer (in project 2)
  Action: Add comment
...
```

**Verification:**
- ✅ Different project GID accepted
- ✅ Task resolved in correct project
- ✅ Dry-run shows correct target
- ✅ Without flag, defaults to `.env` GID

---

### TEST 14: Environment Variable Override

**Purpose:** Verify `ASANA_PROJECT_GID` env var works

**Steps:**
1. Set environment variable:
   ```bash
   export ASANA_PROJECT_GID=your-different-project-gid
   ```

2. Run without `--project-gid` flag:
   ```bash
   python scripts/asana-sync-enhanced.py --dry-run
   ```

**Expected Behavior:**
- Uses env var GID instead of `.env` file

3. Override env var with CLI flag:
   ```bash
   python scripts/asana-sync-enhanced.py --project-gid original-gid --dry-run
   ```

**Expected Behavior:**
- CLI flag takes precedence over env var

**Verification:**
- ✅ Env var read successfully
- ✅ CLI arg overrides env var
- ✅ Priority order correct (CLI > env > .env)

---

### TEST 15: No References Found

**Purpose:** Verify graceful handling when no `@task` in notes

**Steps:**
1. Create test file: `08 - Meeting Notes/2026-09-16-test-empty.md`
   ```markdown
   # Regular Meeting Notes

   We discussed Q4 planning.
   No task references in this note.
   Just regular discussion.
   ```

2. Run:
   ```bash
   python scripts/asana-sync-enhanced.py
   ```

**Expected Output:**
```
Found 0 @task reference(s)
No @task references found in meeting notes.
Execution complete: 0 tasks synced.
```

**Verification:**
- ✅ No error on empty scan
- ✅ Friendly message
- ✅ Log file updated with timestamp

---

## Summary Table

| Test | Purpose | Mode | Expected Result | Status |
|------|---------|------|-----------------|--------|
| **T1** | Dry-run safety | `--dry-run` | No changes, preview shown | ⬜ |
| **T2** | Manual approval | (default) | Proposes, waits for yes/no | ⬜ |
| **T3** | Auto-approve | `--no-prompt` | Executes immediately | ⬜ |
| **T4** | Set due date action | (mixed) | Task due date updated | ⬜ |
| **T5** | Mark complete action | (mixed) | Task status → complete | ⬜ |
| **T6** | Batch sync | (mixed) | Multiple tasks synced | ⬜ |
| **T7** | Exact name match | (mixed) | Task found by exact name | ⬜ |
| **T8** | Fuzzy search match | (mixed) | Task found by keyword | ⬜ |
| **T9** | Ambiguous match | `--interactive` | User selects from choices | ⬜ |
| **T10** | Task not found | (mixed) | Error message, no crash | ⬜ |
| **T11** | Verbose output | `--verbose` | Debug details shown | ⬜ |
| **T12** | Audit log | (any) | All actions logged | ⬜ |
| **T13** | Multi-project | `--project-gid` | Syncs to different project | ⬜ |
| **T14** | Env var override | (env set) | Env var used correctly | ⬜ |
| **T15** | No references | (mixed) | Handles empty gracefully | ⬜ |

---

## Success Criteria

**Core Functionality:**
- ✅ All 15 test cases pass
- ✅ No crashes on any input
- ✅ Audit log complete and accurate
- ✅ Asana tasks updated as expected

**Reliability:**
- ✅ Dry-run never makes changes
- ✅ Approval gate works (manual mode)
- ✅ Auto-mode suitable for hooks
- ✅ Error messages helpful

**Deployment-Ready:**
- ✅ Multi-project support verified
- ✅ Config priority order confirmed
- ✅ Verbose mode for debugging
- ✅ No credentials in logs

---

## Running Full Suite

```bash
cd C:\Repo\Project\test-asana-sync

# Run all tests (manual, answer "yes" at each prompt)
for test in $(ls "08 - Meeting Notes"/2026-09-16-test-*.md | sed 's/.*-\(.*\)\.md/\1/' | sort); do
  echo "Running TEST: $test"
  python scripts/asana-sync-enhanced.py --no-prompt --verbose
  echo "---"
done

# Check results
tail -50 scripts/asana-sync.log
```

---

## Cleanup After Testing

```bash
# Delete test project from Asana (via UI)
# Or keep for re-testing

# Archive test meeting files
mkdir "08 - Meeting Notes/archive"
mv "08 - Meeting Notes"/2026-09-16-test-*.md "08 - Meeting Notes/archive/"

# Delete test directory if needed
rm -rf C:\Repo\Project\test-asana-sync
```

---

## Notes

- **Duration:** Expect 45-60 minutes for full manual run
- **Parallel Testing:** T1-T15 can run independently (no shared state)
- **Re-run Safe:** Reset tasks in Asana UI between runs; script is idempotent
- **Token Limit:** Each test costs ~1-3 API calls; well within Asana rate limits
- **Log Review:** Always check `scripts/asana-sync.log` after each test for detailed execution

---

**Test Plan Created:** 2026-09-16  
**Skill Tested:** Asana Meeting Notes Sync  
**Total Test Cases:** 15  
**Coverage:** All modes, actions, error cases, multi-project
