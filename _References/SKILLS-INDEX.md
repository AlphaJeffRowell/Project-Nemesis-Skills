# Allvue Skills Suite - Complete Index

**11 organized skills for Allvue system architecture, configuration, and project delivery**

**Status:** ✅ All Skills Organized with Full Documentation  
**Created:** 2026-09-16

---

## Quick Navigation

### 🎯 Tier 1: Foundation (Understanding)
These skills help you UNDERSTAND any Allvue object and its ecosystem.

1. **[01-OBJECT-RESOLVER/](01-OBJECT-RESOLVER/)** — Resolve objects to dependency chains
   - Q: "What is this object?"
   - Start here for any investigation

2. **[02-REFERENCE-TRACER/](02-REFERENCE-TRACER/)** — Trace cascading impacts of changes
   - Q: "If I change X, what breaks?"
   - Use after Object Resolver

3. **[03-DATASOURCE-DECODER/](03-DATASOURCE-DECODER/)** — Decode SQL definitions
   - Q: "What SQL does this DataSource execute?"
   - Use to understand data flows

---

### 🔧 Tier 1.5: Expressions & Transforms (Specialized but Universal)
These skills help you BUILD validation rules and data transformations.

4. **[09-XPATH-NAVIGATOR/](09-XPATH-NAVIGATOR/)** — Write XPath validation rules
   - Q: "How do I validate SettleDate > TradeDate?"
   - Used in all workflows

5. **[10-XSLT-TRANSFORMER/](10-XSLT-TRANSFORMER/)** — Create XSLT data transformations
   - Q: "How do I map Geneva to Allvue?"
   - Used in integrations and imports

---

### 🏗️ Tier 2: Domain-Specific (Building)
These skills help you BUILD specific Allvue configurations.

6. **[04-WORKFLOW-DESIGNER/](04-WORKFLOW-DESIGNER/)** — Design trading workflows
   - Q: "How do I build a Bond workflow?"
   - Creates complete workflow structures

7. **[05-COMPLIANCE-ARCHITECT/](05-COMPLIANCE-ARCHITECT/)** — Design compliance rules
   - Q: "How do I set up sector limits?"
   - Creates compliance frameworks

8. **[06-REPORT-GENERATOR/](06-REPORT-GENERATOR/)** — Generate reports
   - Q: "How do I create an executive dashboard?"
   - Creates reports with DataSource bindings

---

### 🔀 Tier 3: Integration (Complex Multi-Step)
These skills combine Understanding + Building for complex tasks.

9. **[07-CONFIGURATION-CLONER/](07-CONFIGURATION-CLONER/)** — Clone configurations
   - Q: "How do I duplicate a portfolio?"
   - Handles all reference adjustments

10. **[08-SOW-SCOPE-GENERATOR/](08-SOW-SCOPE-GENERATOR/)** — Estimate projects
    - Q: "How much will this cost? How long?"
    - Generates full SOWs

---

### 🤖 Cross-Project Automation
These skills work with any project, not just Allvue.

11. **[11-ASANA-TASK-UPDATE/](11-ASANA-TASK-UPDATE/)** — Sync notes to Asana
    - Q: "How do I get meeting notes into Asana?"
    - Supports all task update actions

---

## Folder Structure

```
Skills/
├── 01-OBJECT-RESOLVER/
│   ├── SKILL.md              (quick reference)
│   ├── README.md             (deployment guide)
│   ├── 01-OBJECT-RESOLVER.md (full implementation)
│   └── [supporting files]
├── 02-REFERENCE-TRACER/
│   ├── SKILL.md
│   ├── README.md
│   ├── 02-REFERENCE-TRACER.md
│   └── [supporting files]
├── ... (9 more skills)
├── 11-ASANA-TASK-UPDATE/
│   ├── SKILL.md
│   ├── README.md
│   ├── AsanaTaskUpdate.md
│   ├── asana-sync-enhanced.py
│   └── [supporting files]
├── ALLVUE-ARCHITECTURE-REFERENCE.md  (master reference)
├── ALLVUE-SKILLS-INDEX.md            (full index with examples)
├── SKILLS-INDEX.md                   (this file)
└── new-project/                      (project scaffolding skill)
```

---

## How to Get Started

### Step 1: Pick Your Use Case

**I want to understand an object**
→ Use [01-OBJECT-RESOLVER](01-OBJECT-RESOLVER/)

**I want to see what breaks if I change something**
→ Use [02-REFERENCE-TRACER](02-REFERENCE-TRACER/)

**I want to understand what SQL a DataSource executes**
→ Use [03-DATASOURCE-DECODER](03-DATASOURCE-DECODER/)

**I want to build a workflow**
→ Use [04-WORKFLOW-DESIGNER](04-WORKFLOW-DESIGNER/)

**I want to set up compliance rules**
→ Use [05-COMPLIANCE-ARCHITECT](05-COMPLIANCE-ARCHITECT/)

**I want to create a report**
→ Use [06-REPORT-GENERATOR](06-REPORT-GENERATOR/)

**I want to duplicate a configuration**
→ Use [07-CONFIGURATION-CLONER](07-CONFIGURATION-CLONER/)

**I want to estimate a project**
→ Use [08-SOW-SCOPE-GENERATOR](08-SOW-SCOPE-GENERATOR/)

**I need to write validation rules**
→ Use [09-XPATH-NAVIGATOR](09-XPATH-NAVIGATOR/)

**I need to transform data between systems**
→ Use [10-XSLT-TRANSFORMER](10-XSLT-TRANSFORMER/)

**I need to sync meeting notes to Asana**
→ Use [11-ASANA-TASK-UPDATE](11-ASANA-TASK-UPDATE/)

---

### Step 2: Read the Skill

Each skill folder contains:
- **SKILL.md** — 1-page quick reference (start here)
- **README.md** — Deployment guide with examples
- **[SkillName].md** — Full implementation details

---

### Step 3: Use the Skill

In Claude Code or AI session:
```
User: "Create a Bond Trading workflow"
↓
Skill: Workflow Designer activates
↓
Output: Complete workflow XML ready to import
```

---

## Common Workflows

### Simple: Understand What an Object Does
```
1. Object Resolver → "What is Daily Allocation Report?"
2. Reference Tracer → "Who uses it? What breaks if deleted?"
3. Done!
```

### Medium: Duplicate a Configuration
```
1. Object Resolver → Find source portfolio
2. Configuration Cloner → Clone to new portfolio
3. Reference Tracer → Verify all references updated
4. Done!
```

### Complex: Implement New Fund with Full Setup
```
1. SOW Generator → Estimate scope
2. Workflow Designer → Build trading workflows
3. Compliance Architect → Set up compliance rules
4. Report Generator → Create operational reports
5. Configuration Cloner → Copy across funds
6. Reference Tracer → Final validation
7. Done!
```

---

## Master References

**[ALLVUE-ARCHITECTURE-REFERENCE.md](ALLVUE-ARCHITECTURE-REFERENCE.md)**
- 170 object types documented
- 300+ SQL relationships mapped
- Complete dependency model
- Real examples from 4 clients

**[ALLVUE-SKILLS-INDEX.md](ALLVUE-SKILLS-INDEX.md)**
- Complete skill descriptions
- Real-world examples
- Skill dependencies
- Client implementations

---

## Skill Dependencies

```
UNDERSTANDING LAYER (Learn these first)
├─ 01-OBJECT-RESOLVER (foundation)
├─ 02-REFERENCE-TRACER (learn what breaks)
└─ 03-DATASOURCE-DECODER (understand SQL)

BUILDING BLOCKS (Use for creating configs)
├─ 09-XPATH-NAVIGATOR (validation rules)
└─ 10-XSLT-TRANSFORMER (data mapping)

DOMAIN-SPECIFIC (Build with these)
├─ 04-WORKFLOW-DESIGNER (requires XPath)
├─ 05-COMPLIANCE-ARCHITECT (requires understanding)
└─ 06-REPORT-GENERATOR (requires DataSource knowledge)

INTEGRATION (Combine multiple skills)
├─ 07-CONFIGURATION-CLONER (requires understanding + building)
└─ 08-SOW-SCOPE-GENERATOR (requires all understanding)

CROSS-PROJECT (Independent)
└─ 11-ASANA-TASK-UPDATE (works standalone)
```

---

## Key Metrics

- **11** skills (10 Allvue + 1 cross-project)
- **170** Allvue object types covered
- **300+** SQL relationships documented
- **4** real-world client implementations
- **16,500+** XML configurations analyzed
- **~4,000** objects per typical deployment

---

## Next Steps

1. **Read** [ALLVUE-ARCHITECTURE-REFERENCE.md](ALLVUE-ARCHITECTURE-REFERENCE.md) (30 min)
   - Understand the 170 object types
   - Learn the dependency model

2. **Master One Tier 1 Skill** (1-2 hours)
   - Start with Object Resolver
   - Practice on your objects

3. **Learn Tier 1.5 Skills** (1-2 hours)
   - XPath Navigator for validation
   - XSLT Transformer for integration

4. **Pick Your Path** (varies)
   - **PM/Business:** SOW Generator
   - **Developer:** Workflow Designer + XSLT
   - **Analyst:** Report Generator
   - **Compliance:** Compliance Architect

5. **Combine Skills** (3-5 hours)
   - Use multiple skills together
   - Work on real projects

---

## Deployment Status

✅ **All skills organized with full documentation**  
✅ **11 folders with SKILL.md + README.md structure**  
✅ **Master index and references ready**  
✅ **Ready for Claude Code integration**  

---

**Created:** September 16, 2026  
**Status:** Production-Ready ✅  
**Last Updated:** 2026-09-16
