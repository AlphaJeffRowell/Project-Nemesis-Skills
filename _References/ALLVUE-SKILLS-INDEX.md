# Allvue Skills Suite - Master Index

**Complete skill set for Allvue system architecture, configuration, and project delivery**

---

## What You Have

**11 Comprehensive Skills** — 10 Allvue-specific organized in 3 tiers, plus 1 cross-project automation skill — supporting 4 real-world client implementations (16,500+ XML configurations analyzed).

**Master Architecture Reference** documenting 170 Allvue object types, 300+ SQL relationships, and complete dependency graphs.

**Expression & Transform Skills** for XPath validation rules and XSLT data transformations used throughout Allvue.

---

## Files & Organization

### Main Reference Document
📖 [ALLVUE-ARCHITECTURE-REFERENCE.md](ALLVUE-ARCHITECTURE-REFERENCE.md)
- Complete object model (170 types across 13 domains)
- 300+ SQL foreign key relationships
- Universal reference chains with examples
- Client distribution (Apax, BDT-MSD, Searchlight, TWGGlobal)
- Performance metrics and estimation frameworks

### Skills Directory
📁 [ALLVUE-SKILLS/](ALLVUE-SKILLS/)

#### Tier 1: Foundation (Universal for any object type)
1. **[01-OBJECT-RESOLVER.md](ALLVUE-SKILLS/01-OBJECT-RESOLVER.md)**
   - Resolve ANY Allvue object to complete dependency chain
   - Find: Type, references, SQL resolution, usage context
   - Answer: "What is X? What does it reference? Who uses it?"

2. **[02-REFERENCE-TRACER.md](ALLVUE-SKILLS/02-REFERENCE-TRACER.md)**
   - Trace impact of changes on downstream objects
   - Calculate: Cascading dependencies, risk level, SQL cleanup needed
   - Answer: "If I change X, what breaks? How many objects affected?"

3. **[03-DATASOURCE-DECODER.md](ALLVUE-SKILLS/03-DATASOURCE-DECODER.md)**
   - Decode DataSource definitions to SQL signature
   - Extract: Function parameters, returned fields, SQL joins, usage
   - Answer: "What does this DataSource query? What SQL joins occur?"

### Tier 1.5: Expression & Transform (Specialized but universal)
4. **[09-XPATH-NAVIGATOR.md](ALLVUE-SKILLS/09-XPATH-NAVIGATOR.md)**
   - Write XPath expressions for workflow validation and calculations
   - Build: Validation rules, conditional logic, data calculations, filters
   - Answer: "How do I validate that SettleDate > TradeDate? Calculate allocation %?"

5. **[10-XSLT-TRANSFORMER.md](ALLVUE-SKILLS/10-XSLT-TRANSFORMER.md)**
   - Create XSLT transformations to convert and map XML data
   - Build: Data imports, system integrations, configuration exports
   - Answer: "How do I map Geneva portfolios to Allvue? Transform custodian feeds?"

#### Tier 2: Domain-Specific (Build configurations)
6. **[04-WORKFLOW-DESIGNER.md](ALLVUE-SKILLS/04-WORKFLOW-DESIGNER.md)**
   - Design trade/order workflows for any asset type
   - Build: Steps, validation rules, state transitions, role access
   - Answer: "How do I build a Bond workflow? An Option exercise flow?"

7. **[05-COMPLIANCE-ARCHITECT.md](ALLVUE-SKILLS/05-COMPLIANCE-ARCHITECT.md)**
   - Design compliance rule matrices, scenario tests, ratings
   - Create: Tests, scenarios, rating methodologies, portfolio matrices
   - Answer: "How do I set up sector concentration limits? Credit quality rules?"

8. **[06-REPORT-GENERATOR.md](ALLVUE-SKILLS/06-REPORT-GENERATOR.md)**
   - Generate reports with proper DataSource binding and access control
   - Build: Multi-format exports, role-based access, scheduled delivery
   - Answer: "How do I create a daily operations report? Executive dashboard?"

### Tier 3: Integration (Complex multi-step tasks)
9. **[07-CONFIGURATION-CLONER.md](ALLVUE-SKILLS/07-CONFIGURATION-CLONER.md)**
   - Clone object configurations with reference adjustments
   - Generate: Cloned XML + import package + validation scripts
   - Answer: "How do I duplicate a portfolio? Clone a workflow for new asset?"

10. **[08-SOW-SCOPE-GENERATOR.md](ALLVUE-SKILLS/08-SOW-SCOPE-GENERATOR.md)**
    - Generate Statement of Work from client scope
    - Produce: Object count estimates, timelines, cost breakdown, resource plan
    - Answer: "How much will this project cost? How long will it take?"

#### Navigation
📋 [ALLVUE-SKILLS/README.md](ALLVUE-SKILLS/README.md)
- Quick reference table (which skill to use for what)
- Skill dependency diagram
- Real-world client examples
- Usage scenarios

---

## Cross-Project Automation Skills

**Project Management & Workflow Automation** (works with any client project):

11. **[AsanaTaskUpdate.md](AsanaTaskUpdate.md)** — Unified Meeting Notes to Asana Sync
    - Transform meeting notes (natural language + optional syntax) into Asana task updates
    - Parse items → fuzzy search or direct task match → confirm → execute actions → post with team deduplication
    - Dual-source (SharePoint + local repo) with automatic deduplication across team
    - Extended Asana actions: comments, due dates, assignments, completion, custom fields
    - Parallel execution: MCP skill (primary) or Python script (secondary)
    - Dry-run preview mode for safety validation
    - Answer: "How do I sync meeting notes to Asana with extended actions and team coordination?"

---

## Quick Start

### I want to...

**Understand an object**
→ Use [Object Resolver](ALLVUE-SKILLS/01-OBJECT-RESOLVER.md)
```
Input: "Daily Allocation Report"
Output: Type, references, SQL, who uses it
```

**See impact of a change**
→ Use [Reference Tracer](ALLVUE-SKILLS/02-REFERENCE-TRACER.md)
```
Input: "Delete AllocationMethodology"
Output: 15 broken references, 3 broken reports, risk: HIGH
```

**Understand what SQL a panel queries**
→ Use [DataSource Decoder](ALLVUE-SKILLS/03-DATASOURCE-DECODER.md)
```
Input: "AA_tfnAllocationReport"
Output: Function signature, parameters, joins, fields
```

**Build a trading workflow**
→ Use [Workflow Designer](ALLVUE-SKILLS/04-WORKFLOW-DESIGNER.md)
```
Input: Asset=Bond, Fields=[Qty, SettleDate, Rate]
Output: Workflow + steps + validation XML
```

**Set up compliance rules**
→ Use [Compliance Architect](ALLVUE-SKILLS/05-COMPLIANCE-ARCHITECT.md)
```
Input: Rules=[Sector<25%, CreditQuality>=BBB]
Output: Compliance framework + tests + scenarios
```

**Create a report**
→ Use [Report Generator](ALLVUE-SKILLS/06-REPORT-GENERATOR.md)
```
Input: Purpose=Daily, Data=Allocations, Export=Excel
Output: Report XML + parameters + role access
```

**Duplicate a configuration**
→ Use [Configuration Cloner](ALLVUE-SKILLS/07-CONFIGURATION-CLONER.md)
```
Input: Source=Fund1, Target=Fund2
Output: Cloned XML + import package
```

**Estimate a project**
→ Use [SOW Generator](ALLVUE-SKILLS/08-SOW-SCOPE-GENERATOR.md)
```
Input: 5 portfolios, 4 asset classes, 3 integrations
Output: Object counts, timeline, cost, resource plan
```

---

## Architecture Map

```
UNDERSTANDING LAYER
├─ Object Resolver: What is X?
├─ Reference Tracer: What breaks if I change X?
└─ DataSource Decoder: What SQL does X execute?

BUILDING LAYER (use Understanding Layer + domain expertise)
├─ Workflow Designer: Build trading workflows
├─ Compliance Architect: Design compliance rules
└─ Report Generator: Create reports

INTEGRATION LAYER (combine Understanding + Building)
├─ Configuration Cloner: Duplicate configurations
└─ SOW Generator: Estimate projects

FOUNDATION
└─ ALLVUE-ARCHITECTURE-REFERENCE.md: Master reference for all skills
   ├─ 170 object types
   ├─ 300+ SQL relationships
   ├─ Universal reference chains
   └─ Client examples
```

---

## Real-World Examples

### Example 1: Add a New Fund
1. **Object Resolver**: Look up existing fund "AllVue ClearPar Fund 1"
2. **Configuration Cloner**: Clone to "AllVue ClearPar Fund 2"
3. **Reference Tracer**: Verify all compliance rules copied
4. **Result**: New fund in production in 30 minutes

### Example 2: Fix Broken Compliance Report
1. **Object Resolver**: Find report "Daily Compliance Summary"
2. **DataSource Decoder**: Understand its data source
3. **Reference Tracer**: See what changed in upstream data source
4. **Rebuild**: Update report with new fields
5. **Result**: Report working again

### Example 3: Build New Bond Trading Workflow
1. **Workflow Designer**: Create "Corporate Bond Trading" workflow
2. **Reference Tracer**: Check what else references workflow (compliance, reports)
3. **Result**: Complete workflow ready for UAT

### Example 4: Estimate a $1M Project
1. **SOW Generator**: Input scope (10 portfolios, 5 asset classes, 4 integrations, 50 users)
2. **Output**: 
   - 280 objects to configure
   - 2,100 hours effort
   - $350K cost
   - 16-week timeline
   - 5-person team
3. **Reference Tracer**: Identify complexity drivers
4. **Result**: Accurate project estimate with confidence

---

## Supported Clients & Deployments

**Production Implementations Analyzed**:
- ✅ Apax Partners (OMS + Portfolio Management)
- ✅ BDT-MSD (Portfolio Management + Compliance)
- ✅ Searchlight Capital (Lite deployment)
- ✅ TWG Global (Multi-module: IA + FA + FO + Nexius)

**All skills work across all 4 client implementations** — they're universal to the Allvue platform.

---

## Key Metrics

- **170** Allvue object types documented
- **300+** SQL foreign key relationships mapped
- **13** domains (Portfolio, Workflow, Compliance, UI, etc.)
- **16,500+** XML configurations analyzed
- **1,710+** SQL table definitions reviewed
- **~4,000** objects per typical client deployment
- **8** skills covering all use cases
- **4** real-world client examples

---

## How These Skills Work Together

### Simple Tasks (1-2 skills)
```
Task: "Add a field to a report"
1. Object Resolver → find report
2. DataSource Decoder → see what fields are available
3. Report Generator → add new field
Done!
```

### Medium Tasks (2-3 skills)
```
Task: "Clone a portfolio with new compliance rules"
1. Configuration Cloner → clone portfolio structure
2. Reference Tracer → verify all compliance references updated
3. Compliance Architect → adjust rules for new portfolio
Done!
```

### Complex Tasks (4+ skills)
```
Task: "Implement new client with 5 funds + compliance"
1. SOW Generator → estimate scope + cost
2. Workflow Designer → build trading workflows
3. Compliance Architect → set up compliance rules
4. Report Generator → create operational reports
5. Configuration Cloner → duplicate across funds
6. Reference Tracer → verify no broken references
Done!
```

---

## Documentation Quality

Each skill includes:
- ✅ Clear purpose statement
- ✅ Input/output format
- ✅ Step-by-step process
- ✅ Real-world examples
- ✅ Implementation algorithm
- ✅ Output template
- ✅ Dependency information
- ✅ Validation checklist

---

## Getting Started

**Step 1**: Read [ALLVUE-ARCHITECTURE-REFERENCE.md](ALLVUE-ARCHITECTURE-REFERENCE.md) (30 min)
- Understand 170 object types
- Grasp the dependency model
- See how everything connects

**Step 2**: Pick one Tier 1 skill and master it (1-2 hours)
- Start with [Object Resolver](ALLVUE-SKILLS/01-OBJECT-RESOLVER.md)
- Practice on real objects from clients
- Understand how to read XML + SQL

**Step 3**: Learn Tier 1.5 Expression skills (1-2 hours)
- [XPath Navigator](ALLVUE-SKILLS/09-XPATH-NAVIGATOR.md) - for validation rules
- [XSLT Transformer](ALLVUE-SKILLS/10-XSLT-TRANSFORMER.md) - for data mapping
- These power workflows, compliance, and integrations

**Step 4**: Move to Tier 2 based on your role (varies)
- PM/Business: Start with [SOW Generator](ALLVUE-SKILLS/08-SOW-SCOPE-GENERATOR.md)
- Developer: Start with [Workflow Designer](ALLVUE-SKILLS/04-WORKFLOW-DESIGNER.md)
- Analyst: Start with [Report Generator](ALLVUE-SKILLS/06-REPORT-GENERATOR.md)
- Compliance: Start with [Compliance Architect](ALLVUE-SKILLS/05-COMPLIANCE-ARCHITECT.md)
- Integrations: Start with [XSLT Transformer](ALLVUE-SKILLS/10-XSLT-TRANSFORMER.md)

**Step 5**: Combine skills for real projects
- Use multiple skills together
- Reference the architecture as needed
- Validate using Reference Tracer

---

## Where to Find Configs

**Real configurations from clients**:
- C:\repo\Clients\Apax_Partners\App Exports\
- C:\repo\Clients\BDT-MSD\App Exports\
- C:\repo\Clients\Searchlight\App Exports\
- C:\repo\Clients\TWGGlobal\App Exports\

**Each client has 70 subdirectories** with thousands of XML configuration files:
- Portfolio, Workflow, Report, DataPanel, Compliance, Security, etc.

**Skills teach you how to read and interpret these files.**

---

## Support & Help

Each skill file includes:
- Examples with real client data
- Troubleshooting section
- Implementation checklist
- Validation queries

**Common questions answered by skills**:
- "What type is this object?" → Object Resolver
- "Where is this used?" → Reference Tracer
- "What SQL runs?" → DataSource Decoder
- "How do I build X?" → Domain-specific skill (Workflow/Compliance/Report)
- "Can I duplicate this?" → Configuration Cloner
- "How much will it cost?" → SOW Generator

---

## Status

✅ **Production-Ready** — Based on complete analysis of 4 real client implementations

✅ **Universal** — Works across all Allvue deployments (Apax, BDT-MSD, Searchlight, TWGGlobal)

✅ **Comprehensive** — Covers all 170 object types and all major use cases

✅ **Actionable** — Each skill has clear steps, examples, and templates

---

**Created**: September 15, 2026  
**Based on**: 16,500+ XML configurations + 1,710+ SQL definitions  
**Scope**: Complete Allvue platform architecture + 4 real client implementations  
**Status**: Ready for production use
