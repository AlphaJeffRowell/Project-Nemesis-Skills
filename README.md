# Skills Hub

Central repository for Claude Code skills, organized into **deployable suites** and **independent tools**.

---

## 📦 Allvue Skills Suite (Skills 1-10)

**Production-ready suite for Allvue/Everest configuration, architecture, and SOW generation**

A unified package of 10 specialized skills organized in 4 tiers. Each skill builds on previous layers to enable complete Allvue implementation workflows.

### Quick Navigation

**👉 [Open Allvue Skills Suite](./Allvue-Skills/README.md)** for complete documentation

### Suite Structure

```
Allvue-Skills/
├── Tier-1-Foundation/          (Understanding)
│   ├── 01-OBJECT-RESOLVER      → Resolve any Allvue object
│   ├── 02-REFERENCE-TRACER     → Trace impact of changes
│   └── 03-DATASOURCE-DECODER   → Decode SQL definitions
│
├── Tier-1.5-Transform/         (Universal Tools)
│   ├── 09-XPATH-NAVIGATOR      → Write validation rules
│   └── 10-XSLT-TRANSFORMER     → Transform XML data
│
├── Tier-2-Domain/              (Building)
│   ├── 04-WORKFLOW-DESIGNER    → Design workflows
│   ├── 05-COMPLIANCE-ARCHITECT → Build compliance rules
│   └── 06-REPORT-GENERATOR     → Create reports
│
└── Tier-3-Integration/         (Orchestration)
    ├── 07-CONFIGURATION-CLONER → Clone configurations
    └── 08-SOW-SCOPE-GENERATOR  → Estimate projects
```

### Use Cases

| Question | Tier | Skills |
|----------|------|--------|
| "What is this object?" | Tier 1 | Object Resolver |
| "If I change X, what breaks?" | Tier 1 | Reference Tracer |
| "What SQL does this query?" | Tier 1 | DataSource Decoder |
| "Write validation rules" | Tier 1.5 | XPath Navigator |
| "Map data between systems" | Tier 1.5 | XSLT Transformer |
| "Build a bond workflow" | Tier 2 | Workflow Designer |
| "Design compliance rules" | Tier 2 | Compliance Architect |
| "Create a daily report" | Tier 2 | Report Generator |
| "Duplicate a portfolio" | Tier 3 | Configuration Cloner |
| "Estimate scope & cost" | Tier 3 | SOW Generator |

### Deployment

**Status**: Production-Ready ✅
- Tested across 4 real client implementations
- 16,500+ XML configurations analyzed
- 170 Allvue object types documented
- 300+ SQL relationships mapped

**Deployment**: Single unified package
- All 10 skills deployed together as "Allvue Skills"
- Tiers can be adopted incrementally (Tier 1 → Tier 1.5 → Tier 2 → Tier 3)
- Each skill is self-contained but most powerful when combined

**Reference**: [Allvue Architecture Reference](./_References/ALLVUE-ARCHITECTURE-REFERENCE.md)

---

## 🛠️ Independent Skills

### [11-ASANA-TASK-UPDATE](./11-ASANA-TASK-UPDATE/)
**Purpose**: Sync tasks to Asana project management  
**Use**: Cross-project team automation and task tracking  
**Status**: Production-Ready

### [new-project](./new-project/)
**Purpose**: Claude Code skill for creating new projects  
**Use**: Project scaffolding and initialization  
**Status**: Production-Ready

---

## 📚 Reference Documents

Located in [_References/](./_References/):

| Document | Purpose |
|----------|---------|
| **ALLVUE-ARCHITECTURE-REFERENCE.md** | Master reference: 170 object types, 300+ relationships, SQL schema |
| **ALLVUE-SKILLS-INDEX.md** | Index of all 11 skills with navigation |
| **SKILLS-METADATA-REGISTRY.md** | Metadata definitions for all skills |
| **ORGANIZATION_SUMMARY.md** | Tier-based organization map |
| **QUICK_REFERENCE.md** | Quick lookup for object types and patterns |

---

## Directory Structure

```
Skills/
├── Allvue-Skills/              ← Deployable suite (Skills 1-10)
│   ├── Tier-1-Foundation/
│   ├── Tier-1.5-Transform/
│   ├── Tier-2-Domain/
│   ├── Tier-3-Integration/
│   ├── README.md               (suite documentation)
│   └── SUITE-MANIFEST.json     (deployment manifest)
│
├── 11-ASANA-TASK-UPDATE/       ← Independent skill
├── new-project/                ← Independent skill
├── _References/                ← Shared documentation
└── README.md                   (this file)
```

---

## Getting Started

### For Allvue Implementations

1. **Start with Tier 1**: Master Object Resolver, Reference Tracer, DataSource Decoder
2. **Move to Tier 1.5**: Learn XPath Navigator and XSLT Transformer
3. **Build with Tier 2**: Use Workflow Designer, Compliance Architect, Report Generator
4. **Orchestrate with Tier 3**: Use Configuration Cloner and SOW Generator

**→ [Open Allvue Skills Suite](./Allvue-Skills/README.md)**

### For Quick Lookup

- **Architecture**: See [Allvue Architecture Reference](./_References/ALLVUE-ARCHITECTURE-REFERENCE.md)
- **Skills Overview**: See [Allvue Skills Index](./_References/ALLVUE-SKILLS-INDEX.md)
- **Object Types**: See [Quick Reference](./_References/QUICK_REFERENCE.md)

### For Deployment

- **Suite Manifest**: See [Allvue-Skills/SUITE-MANIFEST.json](./Allvue-Skills/SUITE-MANIFEST.json)
- **Suite Documentation**: See [Allvue-Skills/README.md](./Allvue-Skills/README.md)

---

## Deployment Stats

**Allvue Skills Suite (Skills 1-10)**
- ✅ 10 skills organized in 4 tiers
- ✅ 170 Allvue object types documented
- ✅ 300+ SQL foreign key relationships mapped
- ✅ 1,710+ SQL table definitions
- ✅ 16,500+ XML configurations analyzed
- ✅ 4 real client implementations (Apax, BDT-MSD, Searchlight, TWGGlobal)
- ✅ Production-Ready

**Independent Skills**
- ✅ 11-ASANA-TASK-UPDATE (task sync)
- ✅ new-project (project scaffolding)

---

## File Organization Principles

- **One folder per skill** — Skills are self-contained with supporting files inside
- **Tier subdirectories** — Allvue Skills 1-10 organized by tier for logical grouping
- **SKILL.md** — 1-page quick reference for each skill
- **README.md** — Deployment guide with examples
- **SUITE-MANIFEST.json** — Machine-readable deployment manifest

---

**Status**: Production-Ready  
**Last Updated**: 2026-09-23  
**Version**: 1.0
