# Skills Quick Reference Card

**Where to Find What You Need**

---

## 🎯 By Use Case

### "I want to understand an object"
**→ [01-OBJECT-RESOLVER](01-OBJECT-RESOLVER/)**
- What is X? What does it reference? Who uses it?
- Trigger: "What is the Daily Allocation Report?"

### "I want to see what breaks if I change something"
**→ [02-REFERENCE-TRACER](02-REFERENCE-TRACER/)**
- If I change X, what breaks? How many objects affected?
- Trigger: "What breaks if I delete AllocationMethodology?"

### "I want to understand what SQL a DataSource executes"
**→ [03-DATASOURCE-DECODER](03-DATASOURCE-DECODER/)**
- What SQL does X execute? What fields does it return?
- Trigger: "What SQL does AA_tfnAllocationReport execute?"

### "I want to write validation rules"
**→ [09-XPATH-NAVIGATOR](09-XPATH-NAVIGATOR/)**
- How do I validate that SettleDate > TradeDate?
- Trigger: "Write XPath: SettleDate > TradeDate"

### "I want to transform data between systems"
**→ [10-XSLT-TRANSFORMER](10-XSLT-TRANSFORMER/)**
- How do I map Geneva portfolios to Allvue?
- Trigger: "Create XSLT to map Geneva to Allvue"

### "I want to build a trading workflow"
**→ [04-WORKFLOW-DESIGNER](04-WORKFLOW-DESIGNER/)**
- How do I build a Bond workflow? What steps? What validations?
- Trigger: "Design a Bond Trading workflow"

### "I want to set up compliance rules"
**→ [05-COMPLIANCE-ARCHITECT](05-COMPLIANCE-ARCHITECT/)**
- How do I set up sector concentration limits?
- Trigger: "Design compliance rules for sector limits"

### "I want to create a report"
**→ [06-REPORT-GENERATOR](06-REPORT-GENERATOR/)**
- How do I create an executive dashboard?
- Trigger: "Create a Daily Allocations report"

### "I want to duplicate a configuration"
**→ [07-CONFIGURATION-CLONER](07-CONFIGURATION-CLONER/)**
- How do I clone a portfolio? How do I adjust references?
- Trigger: "Clone Fund 1 to Fund 2"

### "I want to estimate a project"
**→ [08-SOW-SCOPE-GENERATOR](08-SOW-SCOPE-GENERATOR/)**
- How much will this cost? How long will it take?
- Trigger: "Estimate: 5 portfolios, 4 asset classes"

### "I want to sync meeting notes to Asana"
**→ [11-ASANA-TASK-UPDATE](11-ASANA-TASK-UPDATE/)**
- How do I get meeting notes into Asana with actions?
- Trigger: "Sync meeting notes to Asana"

---

## 📂 By Folder

| Folder | What It Does | Start With |
|--------|-------------|-----------|
| 01-OBJECT-RESOLVER | Resolve objects to dependency chains | SKILL.md |
| 02-REFERENCE-TRACER | Trace cascading impacts | SKILL.md |
| 03-DATASOURCE-DECODER | Understand SQL definitions | SKILL.md |
| 04-WORKFLOW-DESIGNER | Build trading workflows | SKILL.md |
| 05-COMPLIANCE-ARCHITECT | Design compliance rules | SKILL.md |
| 06-REPORT-GENERATOR | Create reports | SKILL.md |
| 07-CONFIGURATION-CLONER | Clone configurations | SKILL.md |
| 08-SOW-SCOPE-GENERATOR | Estimate projects | SKILL.md |
| 09-XPATH-NAVIGATOR | Write XPath rules | SKILL.md |
| 10-XSLT-TRANSFORMER | Transform data | SKILL.md |
| 11-ASANA-TASK-UPDATE | Sync to Asana | SKILL.md |

---

## 📚 Master Indexes

| File | Purpose | Read Time |
|------|---------|-----------|
| **SKILLS-INDEX.md** | Central navigation for all 11 skills | 5 min |
| **ORGANIZATION_SUMMARY.md** | Overview of organization | 3 min |
| **COMPLETE_SKILLS_STRUCTURE.txt** | Visual ASCII tree | 2 min |
| **ALLVUE-ARCHITECTURE-REFERENCE.md** | 170 object types + SQL | 30 min |
| **ALLVUE-SKILLS-INDEX.md** | Full skill descriptions | 10 min |

---

## 🎓 Learning Path

### Day 1: Foundation
1. Read SKILLS-INDEX.md (5 min) — overview
2. Read 01-OBJECT-RESOLVER/SKILL.md (5 min) — quick ref
3. Read 01-OBJECT-RESOLVER/README.md (10 min) — deployment
4. Try it: "What is a workflow?"

### Day 2: Impact Analysis
1. Read 02-REFERENCE-TRACER/SKILL.md (5 min)
2. Try it: "What breaks if I delete X?"

### Day 3: Data Understanding
1. Read 03-DATASOURCE-DECODER/SKILL.md (5 min)
2. Try it: "What SQL does this execute?"

### Day 4: Building (Pick One)
**If Developer:** Read 04-WORKFLOW-DESIGNER/SKILL.md  
**If Analyst:** Read 06-REPORT-GENERATOR/SKILL.md  
**If Compliance:** Read 05-COMPLIANCE-ARCHITECT/SKILL.md  

### Day 5: Expressions
1. Read 09-XPATH-NAVIGATOR/SKILL.md (5 min)
2. Read 10-XSLT-TRANSFORMER/SKILL.md (5 min)

### Day 6: Integration
1. Read 07-CONFIGURATION-CLONER/SKILL.md (5 min)
2. Read 08-SOW-SCOPE-GENERATOR/SKILL.md (5 min)

---

## 💡 Common Workflows

### Workflow 1: Understand & Impact Check
```
1. 01-OBJECT-RESOLVER   → "What is this?"
2. 02-REFERENCE-TRACER  → "What breaks?"
Done in 10 minutes
```

### Workflow 2: Duplicate Configuration
```
1. 01-OBJECT-RESOLVER      → Find source object
2. 07-CONFIGURATION-CLONER → Clone it
3. 02-REFERENCE-TRACER     → Verify references
Done in 30 minutes
```

### Workflow 3: Build Complex Workflow
```
1. 04-WORKFLOW-DESIGNER → Design steps
2. 09-XPATH-NAVIGATOR  → Write validation rules
3. 02-REFERENCE-TRACER → Check impacts
Done in 2-4 hours
```

### Workflow 4: Estimate Full Project
```
1. 08-SOW-SCOPE-GENERATOR → Get estimate
2. 02-REFERENCE-TRACER    → Identify complexity
Done in 1-2 hours
```

---

## ⚡ Super Quick Start

**Don't know where to start?**
1. Read this file (you are here) ✓
2. Go to [SKILLS-INDEX.md](SKILLS-INDEX.md) (5 min)
3. Pick a skill that matches your need
4. Go to that folder
5. Read SKILL.md (1 page, 5 min)
6. Try it!

---

## 📞 Need Help?

**For any skill:**
- Folder contains: SKILL.md (quick) + README.md (detailed)
- Check real-world examples in README.md
- Review integration section to see what works together

**For the big picture:**
- Read ALLVUE-ARCHITECTURE-REFERENCE.md
- Understand 170 object types + 300+ relationships
- See how everything connects

---

**Created:** September 16, 2026  
**Status:** All 11 skills organized and ready ✅
