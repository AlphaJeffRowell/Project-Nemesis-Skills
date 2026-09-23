# Implementation Guide: Asana Bulk User Story Task Creation

**Document Version:** 1.0  
**Last Updated:** 2026-09-16  
**Created For:** Project Chimera / Project Nemesis

---

## Executive Summary

This guide documents the end-to-end process for converting user stories and acceptance criteria into a hierarchical Asana task structure. The workflow extracts stories from a spreadsheet, creates parent tasks in one section, creates acceptance criteria as child tasks in another section, and maintains consistent naming, assignment, and structure.

**Expected Output:** 9 parent tasks + 44 subtasks, all properly linked and assigned.

---

## Detailed Workflow

### Phase 1: Preparation & Validation

#### 1.1 Gather Requirements
- [ ] User stories spreadsheet (Excel format)
- [ ] Column structure: Story ID | Title | Description | Acceptance Criteria
- [ ] Asana project name (e.g., "Project Nemesis")
- [ ] Target assignee (e.g., "Jeff Rowell")
- [ ] Existing parent task GIDs to delete (if restructuring)

**Example structure:**
```
| Story ID | Title | Description | Acceptance Criteria |
|----------|-------|-------------|-------------------|
| US-1 | Estimate Creation | As a PM, I want... | - Accept Requirements Spreadsheet |
|      |        |             | - Analyze Complexity & Effort |
|      |        |             | - Provide Effort Estimates |
```

#### 1.2 Verify Asana Project
```bash
# Confirm project exists and sections are named correctly
asana_typeahead_search(resource_type="project", query="Project Nemesis")
# Expected: returns project GID (e.g., 1218362790344978)

# List all sections
asana_get_project_sections(project_id="1218362790344978")
# Expected: Find "Development & QA" and "User Acceptance Testing" sections
```

#### 1.3 Confirm Assignee GID
```bash
asana_typeahead_search(resource_type="user", query="Jeff Rowell")
# Expected: returns user GID (e.g., 1211068656393609)
```

**Critical:** Store these GIDs — they are required for all subsequent task creation calls.

---

### Phase 2: Parse & Plan

#### 2.1 Extract User Stories
Read the source spreadsheet and build a task plan:

| Story | Title | AC Count | Notes |
|-------|-------|----------|-------|
| US-1 | Estimate Creation | 7 | Full 7 acceptance criteria |
| US-2 | SOW Creation | 5 | Well-scoped 5 criteria |
| US-8 | Teams Comm Tracking | 5 | Expanded from sparse description |
| US-9 | Outlook Integration | 5 | Expanded from sparse description |

**Rule:** If a story has <3 ACs or >8 ACs, review with stakeholder. Flag unusual breakdowns before creating.

#### 2.2 Create Planning Spreadsheet
Generate an `Asana_Task_Restructure_Plan.xlsx` with columns:
- Action (DELETE / CREATE)
- Section (Development & QA / User Acceptance Testing / etc.)
- Task Type (Parent Task / Subtask)
- Task ID (US-N / US-N-ACM)
- Task Name (full formatted name)
- Description
- Assignee
- Asana GID (current or NEW)

**Example row:**
```
DELETE | Untitled section | Parent Task | - | US-1: Estimate Creation | ... | N/A | 1218549503930191
CREATE | Development & QA | Parent Task | US-1 | US-1: Estimate Creation | ... | Jeff Rowell | NEW
CREATE | User Acceptance Testing | Subtask | US-1-AC1 | US-1-AC1: Accept Requirements Spreadsheet | ... | Jeff Rowell | NEW
```

#### 2.3 Review & Confirm
- [ ] Display planning spreadsheet to stakeholder
- [ ] Confirm task count matches expectation (9 parents + AC subtasks)
- [ ] Confirm section mapping (parents→Dev, ACs→UAT)
- [ ] Confirm assignee (Jeff Rowell for all)
- [ ] **Get explicit approval before proceeding**

---

### Phase 3: Deletion (If Restructuring)

#### 3.1 Delete Old Parent Tasks
If replacing existing tasks, delete old parent tasks first (subtasks auto-delete if not in other projects):

```bash
asana_delete_task(task_id="1218549503872670")  # Old US-4
asana_delete_task(task_id="1218549504228880")  # Old US-5
# ... etc for all 7 old tasks
```

**Why before:** Prevents duplicate task names in the project.

#### 3.2 Verify Deletion
```bash
asana_search_tasks(projects_any="1218362790344978", text="US-1")
# Expect: Only NEW US-1 task exists (if already created)
```

---

### Phase 4: Create Parent Tasks (User Stories)

#### 4.1 Batch Create Parents
For each user story, call:

```bash
asana_create_task(
  name="US-{N}: {Title}",
  project_id="1218362790344978",           # Project Nemesis GID
  section_id="1218377628302949",           # Development & QA section GID
  notes="{Full story description}",
  assignee="1211068656393609",             # Jeff Rowell GID
)
```

**All 9 calls in parallel** (batch them together to speed up):

| Story | Name | Expected GID Return |
|-------|------|-------------------|
| US-1 | US-1: Estimate Creation | NEW GID → store as `parent_us1_gid` |
| US-2 | US-2: SOW Creation | NEW GID → store as `parent_us2_gid` |
| ... | ... | ... |
| US-9 | US-9: Outlook Email Integration | NEW GID → store as `parent_us9_gid` |

**Critical:** Store each returned GID — required for subtask creation in Phase 5.

#### 4.2 Verify Parent Creation
```bash
asana_search_tasks(
  projects_any="1218362790344978",
  resource_subtype="default_task"  # Get parent tasks only
)
# Expected: 9 tasks with names US-1 through US-9
```

---

### Phase 5: Create Subtasks (Acceptance Criteria)

#### 5.1 Batch Create Subtasks by Parent
For each parent task, create all its acceptance criteria subtasks:

```bash
# For US-1 (7 AC subtasks)
asana_create_task(
  name="US-1-AC1: Accept Requirements Spreadsheet",
  project_id="1218362790344978",
  section_id="1218377721415199",           # User Acceptance Testing section GID
  notes="Accept uploaded spreadsheet with client requirements",
  parent="1218551918761316",               # Returned parent GID from Phase 4
  assignee="1211068656393609",             # Jeff Rowell GID
)

# ... repeat AC2 through AC7
```

**Execution pattern:**
1. Create all AC subtasks for US-1 (7 tasks)
2. Create all AC subtasks for US-2 (5 tasks)
3. ... and so on through US-9

**Batch optimization:** Group 10-15 calls per batch, execute in parallel, wait for completion, then next batch.

#### 5.2 Verify Subtask Creation
```bash
asana_get_task(task_id="{parent_us1_gid}", opt_fields="subtasks")
# Expected: 7 subtasks listed under US-1

# Or search for AC subtasks
asana_search_tasks(
  projects_any="1218362790344978",
  text="AC1",
  limit=50
)
# Expected: All AC1 tasks across US-1 through US-9 (9 tasks total)
```

---

### Phase 6: Verification & Reporting

#### 6.1 Task Count Validation
```
Expected: 9 parent tasks + 44 subtasks = 53 total tasks

Breakdown:
- US-1 parent + 7 AC subtasks = 8 tasks
- US-2 parent + 5 AC subtasks = 6 tasks
- US-3 parent + 6 AC subtasks = 7 tasks
- US-4 parent + 6 AC subtasks = 7 tasks
- US-5 parent + 6 AC subtasks = 7 tasks
- US-6 parent + 7 AC subtasks = 8 tasks
- US-7 parent + 6 AC subtasks = 7 tasks
- US-8 parent + 5 AC subtasks = 6 tasks
- US-9 parent + 5 AC subtasks = 6 tasks
```

#### 6.2 Section Placement Validation
- [ ] All 9 parent tasks in "Development & QA" section
- [ ] All 44 AC subtasks in "User Acceptance Testing" section
- [ ] No tasks in wrong section

#### 6.3 Assignment Validation
- [ ] All 53 tasks assigned to Jeff Rowell
- [ ] No unassigned tasks
- [ ] Verify in Asana UI: Jeff's task count increases by 53

#### 6.4 Hierarchy Validation
- [ ] Each AC subtask has correct parent (US-1, US-2, etc.)
- [ ] No orphaned subtasks
- [ ] Parent-child relationships visualize correctly in Asana

**Sample check:**
```bash
asana_get_task(task_id="{us1_parent_gid}")
# Expected: subtasks array contains all 7 AC1-AC7 task GIDs
```

---

## Decision Rationale

### Why Separate Sections?

| Section | Purpose | Why This Choice |
|---------|---------|-----------------|
| Development & QA | Parent user stories represent features to build | Consolidates scope; visible to dev team at board level |
| User Acceptance Testing | Acceptance criteria define test coverage | Isolates validation work; UAT team can focus on this section; easy to track test progress independently |

### Why This Naming Convention?

| Element | Format | Why |
|---------|--------|-----|
| Parent | `US-{N}: {Title}` | Matches user story numbering in SOW; stakeholders reference by this number |
| Subtask | `US-{N}-AC{M}: {Title}` | Links AC back to parent; sequential; parseable in reports and searches |

### Why Assign All to One User?

**Current:** All assigned to Jeff Rowell (PM)
**Reason:** Single orchestrator; Jeff routes work to developers/QA team via subtask reassignment or comments

**Alternative:** Could assign by role:
- Parent tasks → Jeff (PM)
- Dev-related ACs → Dev lead
- QA-related ACs → QA lead
- Requires custom role mapping in source data

---

## Common Variations

### Variation 1: Multiple Assignees per AC
**Use when:** You want different team members owning different ACs

**Change:** Extend source spreadsheet to include AC-level assignee column
```
| Story | AC | Title | Assignee |
| US-1 | AC1 | Accept Requirements | Jeff Rowell |
| US-1 | AC2 | Analyze Complexity | Alice (Dev Lead) |
```

**Implementation:** Check assignee per AC in Phase 5; use different GID per task

### Variation 2: Add Due Dates
**Use when:** SOW or estimation spreadsheet specifies delivery dates

**Change:** Add `due_on` parameter to task creation
```bash
asana_create_task(
  ...,
  due_on="2026-10-15",  # From SOW timeline
)
```

### Variation 3: Set Initial Status
**Use when:** You want all new tasks to start in a specific status (e.g., "Not Started")

**Change:** Populate custom Status field during creation
```bash
asana_create_task(
  ...,
  custom_fields='{"1218377804698249": "1218377804698250"}',  # Status = "Not Started"
)
```

### Variation 4: Auto-organize by Rollout Sequence
**Use when:** User stories have a defined rollout order (Phase 1, Phase 2, etc.)

**Change:** Add custom field or tags to group related stories
```bash
asana_create_task(
  ...,
  custom_fields='{"rollout_phase": "Phase 1"}',
)
```

---

## Troubleshooting

### Problem: "Section not found" error

**Cause:** Section name mismatch or wrong project
**Fix:**
1. List all sections: `asana_get_project_sections(project_id="...")`
2. Verify section names match exactly (case-sensitive)
3. Confirm you're using correct project GID

### Problem: Parent task GID not returned

**Cause:** API response didn't include GID field
**Fix:**
1. Use `asana_search_tasks` to find task by name
2. Add `opt_fields="gid"` to task creation call if available
3. Check Asana API response format

### Problem: Subtasks appear in wrong parent

**Cause:** Parent GID typo or ID reused
**Fix:**
1. Verify parent GID stored correctly in Phase 4
2. Use unique variable per parent (e.g., `parent_us1_gid`, `parent_us2_gid`)
3. Double-check task creation logs

### Problem: Duplicate tasks created

**Cause:** Parallel calls executed twice or rerun of Phase 4/5
**Fix:**
1. Check Asana search before re-running
2. For reruns, search for existing tasks and skip creation
3. Add idempotency check: search by name, create only if not found

### Problem: Assignee not recognized

**Cause:** Incorrect GID or user not in workspace
**Fix:**
1. Use `asana_typeahead_search(resource_type="user", query="Jeff Rowell")`
2. Verify user is active in workspace
3. Confirm GID format (should be numeric string, e.g., "1211068656393609")

---

## Post-Implementation Checklist

- [ ] All 53 tasks created in Asana
- [ ] Task count verified by project search
- [ ] Parent-child relationships confirmed (all ACs linked to correct parents)
- [ ] All tasks assigned to Jeff Rowell
- [ ] Development & QA section contains 9 parent tasks only
- [ ] User Acceptance Testing section contains 44 AC subtasks only
- [ ] Task names follow `US-{N}` and `US-{N}-AC{M}` format
- [ ] Stakeholder confirmed structure in Asana UI
- [ ] Planning spreadsheet archived as reference
- [ ] Source spreadsheet backed up (if modifications were made)

---

## Next Steps

Once tasks are created, typical workflows include:

1. **Subtask Assignment:** Jeff reassigns AC subtasks to developers/QA team members
2. **Dependency Linking:** Create blocking relationships between parent stories using `asana_set_task_dependencies`
3. **Status Tracking:** Move tasks through workflow (Not Started → In Progress → Complete)
4. **Reporting:** Generate progress reports by parent story (how many AC subtasks complete per story)

---

## References

- **Asana Connector Tools:**
  - `asana_create_task` — Create single task
  - `asana_get_project_sections` — List project sections
  - `asana_typeahead_search` — Find projects, users, tasks
  - `asana_search_tasks` — Search by criteria
  - `asana_delete_task` — Delete task
  - `asana_get_task` — Get task details including subtasks

- **Project Chimera Artifacts:**
  - `Chimera_User_Stories.xlsx` — Source data (9 user stories)
  - `Asana_Task_Restructure_Plan.xlsx` — Planning spreadsheet (53 tasks planned)
  - Project Nemesis Asana board — Live task board (53 tasks created)

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-09-16 | Claude Haiku 4.5 | Initial guide; documented end-to-end workflow for Project Chimera |

