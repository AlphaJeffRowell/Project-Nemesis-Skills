# Asana Bulk User Story Tasks Skill

**Purpose:** Automate creation of hierarchical Asana task structures from user stories with acceptance criteria as subtasks.

**Use When:** You have user stories with acceptance criteria and need to:
- Create parent tasks (User Stories) in a "Development & QA" section
- Create child tasks (Acceptance Criteria) in a "User Acceptance Testing" section
- Establish parent-child relationships
- Assign all to a single user
- Maintain consistent numbering (US-1, US-1-AC1, etc.)

---

## Workflow Overview

### Inputs Required
1. **User stories spreadsheet** (Excel, CSV) with columns:
   - Story ID (e.g., US-1)
   - Story Title
   - Story Description
   - Acceptance Criteria (bulleted or comma-separated)

2. **Asana context:**
   - Project name or GID
   - Assignee name or GID
   - Development & QA section GID (for parent tasks)
   - User Acceptance Testing section GID (for subtasks)

### Process Steps

#### Step 1: Parse User Stories
Read the source spreadsheet and extract:
- Parent task name and description
- List of acceptance criteria per story
- Maintain sequential numbering

#### Step 2: Create Parent Tasks
For each user story:
- Name: `US-{N}: {Story Title}`
- Description: Full story description
- Section: Development & QA
- Assignee: Specified user (e.g., Jeff Rowell)
- Store returned GID for use in subtask creation

#### Step 3: Create Subtasks
For each acceptance criterion:
- Name: `US-{N}-AC{M}: {Criterion Title}`
- Description: Acceptance criterion text
- Section: User Acceptance Testing
- Parent: Link to parent task GID
- Assignee: Same user as parent

#### Step 4: Confirm Completion
- Verify all parent tasks created (9 tasks)
- Verify all subtasks created (44 tasks in this example)
- Report count by parent story

---

## Implementation Example

This was successfully executed on **2026-09-16** for Project Nemesis:

**Input:** 9 user stories with 44 acceptance criteria total
**Output:**
- 9 parent tasks (US-1 through US-9) in Development & QA
- 44 subtasks (AC1-AC7 for each) in User Acceptance Testing
- All assigned to Jeff Rowell

**Breakdown:**
- US-1: 7 AC subtasks
- US-2: 5 AC subtasks
- US-3: 6 AC subtasks
- US-4: 6 AC subtasks
- US-5: 6 AC subtasks
- US-6: 7 AC subtasks
- US-7: 6 AC subtasks
- US-8: 5 AC subtasks
- US-9: 5 AC subtasks

---

## Key Decisions

### Parent Task Placement
- **Section:** Development & QA (captures the implementation scope)
- **Why:** Parent stories represent the full feature to be developed

### Subtask Placement
- **Section:** User Acceptance Testing (isolates validation work)
- **Why:** Acceptance criteria define what testers validate; separate section enables focused UAT tracking

### Naming Convention
- **Format:** `US-{N}-AC{M}: {Short Title}`
- **Why:** Sequential numbering maintains auditability and matches stakeholder references

### Assignment Strategy
- **All to single user:** Jeff Rowell (PM/orchestrator role)
- **Alternative:** Could vary by skill type (dev vs. QA) if needed

---

## When NOT to Use

- Individual task creation (use Asana UI)
- Stories without clear acceptance criteria
- Mixed-scope bulk operations (combine this with other workflows separately)
- Real-time backlog grooming (batch this with planning cycles)

---

## Variations & Extensions

### Variant 1: Custom Field Population
Can add Status field initialization (e.g., "Not Started" for all new tasks):
```
custom_fields: {
  "Status": "1218377804698250"  // "Not Started" enum option GID
}
```

### Variant 2: Multiple Assignees
Modify to support role-based assignment:
- Parent tasks → PM (e.g., Jeff Rowell)
- Dev-related ACs → Dev lead
- QA-related ACs → QA lead

### Variant 3: Due Date Injection
Add due dates from estimation spreadsheet:
```
due_on: "2026-10-15"  // Derived from SOW timeline
```

### Variant 4: Custom Descriptions
Expand AC descriptions to include:
- Acceptance Criteria definition
- Testing approach
- Related acceptance criteria (dependencies)

---

## API Calls Used

All tasks created via `asana_create_task` connector:

```
Parameters per call:
- name: {Task name}
- project_id: {Project GID}
- section_id: {Section GID}
- notes: {Description}
- parent: {Parent task GID} (subtasks only)
- assignee: {User GID}
```

**Pro tip:** Batch calls in parallel when creating 10+ tasks for faster execution.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Section not found | Use `asana_get_project_sections` to list all sections and verify section names/GIDs |
| Parent task GID not returned | Check Asana response; some API calls don't return GID in first response — use `asana_search_tasks` to locate by name |
| Assignee not recognized | Verify GID format; use `asana_typeahead_search` with resource_type="user" to look up correct GID |
| Duplicate tasks created | Check if parallel calls used same parent GID; add delay between parent creation and subtask batch |

---

## Related Resources

- [Asana Task Restructure Plan](C:\Repo\Project\Project-Chimera\Asana_Task_Restructure_Plan.xlsx) — Example planning spreadsheet
- [Chimera User Stories](C:\Repo\Project\Project-Chimera\Chimera_User_Stories.xlsx) — Example source spreadsheet
- Asana Connector: `asana_create_task`, `asana_get_project_sections`, `asana_typeahead_search`
