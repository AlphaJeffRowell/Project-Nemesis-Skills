# Asana Task Update Skill

**Trigger:** "sync to asana", "update asana", "meeting to asana"  
**Purpose:** Unified Meeting Notes to Asana Sync with extended actions  
**Status:** Ready for deployment  
**Tier:** Cross-Project (Automation)

---

## Quick Start

Ask the skill to sync meeting notes to Asana:
- "Sync meeting notes to Asana"
- "Update Asana from notes"
- "Parse items and update tasks"

The skill will:
1. Parse meeting notes (natural language + optional syntax)
2. Search for matching tasks (fuzzy matching + direct ID)
3. Confirm matches with user
4. Execute actions (comment, update fields, assign, complete)
5. Post unified update with team deduplication

---

## What It Does

Answers: "How do I get meeting notes into Asana? Can I parse natural language?"

**Inputs:**
- Meeting notes (markdown/text)
- Optional syntax markers
- Asana workspace/project
- Team for deduplication

**Outputs:**
- Matched Asana tasks
- Executed updates (comments, due dates, assignments)
- Team-deduplicated post
- Execution log
- Confirmation report

---

## How It Works

1. **Parse** — Extract items from notes
2. **Search** — Find matching Asana tasks (fuzzy + direct)
3. **Confirm** — Show matches to user
4. **Execute** — Update tasks (comments, assignments, completion, custom fields)
5. **Post** — Send unified update (team deduplicated)

---

## Features

✅ **Dual Source** — SharePoint + local repo with auto-deduplication  
✅ **Extended Actions** — Comments, due dates, assignments, completion  
✅ **Dry-Run Mode** — Preview changes before executing  
✅ **Team Aware** — Automatic deduplication across team members  
✅ **MCP Native** — No Python setup required  

---

## Real-World Examples

### Example 1: Simple Meeting Notes
```
User: "Sync these notes to Asana"
Notes:
  - Update API documentation (task: API docs)
  - Set deadline for auth module to Sep 20
  - Assign compliance review to Jane

↓
Skill: Matched Tasks:
       1. API Documentation (98% match)
       2. Auth Module (direct match)
       3. Compliance Review (assigned to Jane)
       Actions:
         • Added comment: "Updated per meeting"
         • Set due date: 2026-09-20
         • Assigned: Jane
       Confirmation: 3 tasks updated, 1 deduplicated
```

### Example 2: Bulk Status Update
```
User: "Parse team sprint status"
Notes:
  [Dev Task 1] Complete ✓
  [Dev Task 2] In Progress, blocked on API
  [Design Review] Ready for approval

↓
Skill: Matched 3 tasks, executed:
       • Marked complete: Task 1
       • Updated status: In Progress, commented "blocked on API"
       • Added: "Ready for approval"
       Team dedup: 1 duplicate removed
```

---

## Deployment

✅ **Ready for deployment** — MCP skill (primary) + Python backup

See AsanaTaskUpdate.md for extended documentation.

---

See IMPLEMENTATION.md for technical details.
