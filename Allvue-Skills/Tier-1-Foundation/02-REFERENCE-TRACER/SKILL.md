# Reference Tracer Skill

**Trigger:** "trace impact", "reference check", "what breaks if"  
**Purpose:** Trace cascading impact of changes on downstream objects  
**Status:** Ready for deployment  
**Tier:** Foundation (Understanding Layer)

---

## Quick Start

Ask the skill to see what breaks when you change something:
- "What breaks if I delete AllocationMethodology?"
- "Trace impact of Report change"
- "Reference check for Compliance Rule modification"

The skill will:
1. Find all objects that reference the target
2. Calculate cascading impacts
3. Identify risk level
4. Show SQL cleanup needed
5. Suggest mitigation steps

---

## What It Does

Answers: "If I change X, what breaks? How many objects affected? What's the risk?"

**Inputs:**
- Object name to change
- Change type (delete, modify, rename)

**Outputs:**
- Direct references (objects immediately affected)
- Cascading impacts (downstream broken dependencies)
- Risk assessment (LOW/MEDIUM/HIGH/CRITICAL)
- SQL cleanup requirements
- Remediation steps

---

## How It Works

1. **Search** — Find all references to target object
2. **Classify** — Direct vs. cascading impacts
3. **Assess** — Calculate risk level based on impact count
4. **SQL** — Generate cleanup queries
5. **Mitigate** — Suggest fixes and workarounds

---

## Real-World Examples

### Example 1: Delete AllocationMethodology
```
User: "What breaks if I delete AllocationMethodology?"
↓
Skill: Direct References: 15 objects
       Cascading: 23 reports broken, 8 workflows affected
       Risk Level: CRITICAL (47 total affected)
       SQL Cleanup: DELETE statement for allocation_methods
       Mitigation: Migrate to standard method first, then delete
```

### Example 2: Modify Report DataSource
```
User: "What if I change the Daily Summary DataSource?"
↓
Skill: Direct References: 3 role assignments
       Cascading: 2 dashboard panels, 4 compliance rules
       Risk Level: HIGH (9 total affected)
       Impact: Dashboard breaks, compliance auto-calcs fail
       Mitigation: Update role assignments + retrain compliance
```

---

## Deployment

✅ **Ready for deployment** — Maps all 300+ SQL relationships

---

See IMPLEMENTATION.md for technical details.
