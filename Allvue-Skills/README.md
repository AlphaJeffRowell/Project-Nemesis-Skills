# Allvue Skills Suite

**Comprehensive, production-ready skill set for Allvue/Everest configuration, architecture, and SOW generation**

A unified deployment package containing 10 specialized skills organized in 4 tiers. Each skill builds on previous layers to enable complete Allvue implementation workflows.

---

## Suite Overview

| Tier | Skills | Purpose |
|------|--------|---------|
| **Tier 1: Foundation** | Object Resolver, Reference Tracer, DataSource Decoder | Understand any Allvue object, SQL schema, and impact of changes |
| **Tier 1.5: Transform** | XPath Navigator, XSLT Transformer | Write validation rules and transform XML data |
| **Tier 2: Domain-Specific** | Workflow Designer, Compliance Architect, Report Generator | Build workflows, compliance rules, and reports |
| **Tier 3: Integration** | Configuration Cloner, SOW Generator | Orchestrate complex multi-step implementations |

---

## Quick Start by Use Case

### "I need to understand what an object does"
1. Start with **Tier 1: Foundation** — master Object Resolver, Reference Tracer, DataSource Decoder
2. **Skill**: 01-OBJECT-RESOLVER
3. **Output**: Complete dependency chain, SQL schema, usage context

### "I'm building a workflow for bond trading"
1. **Tier 1.5**: XPath Navigator (for validation rules)
2. **Tier 2**: Workflow Designer
3. **Skills**: 09-XPATH-NAVIGATOR, 04-WORKFLOW-DESIGNER
4. **Output**: Complete workflow XML with validation rules

### "I need to design compliance rules with stress testing"
1. **Tier 1**: DataSource Decoder (understand available data)
2. **Tier 1.5**: XPath Navigator (write rule expressions)
3. **Tier 2**: Compliance Architect
4. **Skills**: 03-DATASOURCE-DECODER, 09-XPATH-NAVIGATOR, 05-COMPLIANCE-ARCHITECT
5. **Output**: Compliance framework with scenario tests

### "I need to estimate a full implementation project"
1. **All tiers**: SOW Generator uses all previous skills for estimation
2. **Skill**: 08-SOW-SCOPE-GENERATOR
3. **Input**: Client scope (portfolios, asset classes, compliance, integrations, users)
4. **Output**: SOW document, resource plan, cost breakdown, timeline

---

## Tier Structure & Dependencies

### Tier 1: Foundation (Understanding Layer)

**Must master first** — provides foundational knowledge of any Allvue object.

#### [01-OBJECT-RESOLVER](./Tier-1-Foundation/01-OBJECT-RESOLVER)
- **Purpose**: Resolve ANY Allvue object to its complete dependency chain
- **Input**: Object name/CodeName
- **Output**: Type, references, SQL resolution, impact
- **Example**: "What is 'Daily Allocation Report'?" → Full dependency chain with SQL

#### [02-REFERENCE-TRACER](./Tier-1-Foundation/02-REFERENCE-TRACER)
- **Purpose**: Trace cascading impact of changes on downstream objects
- **Input**: Object + operation (create/modify/delete)
- **Output**: Impact matrix, risk assessment, SQL cleanup
- **Example**: "If I delete ComplianceTest X, what breaks?" → 15 direct impacts, risk level HIGH

#### [03-DATASOURCE-DECODER](./Tier-1-Foundation/03-DATASOURCE-DECODER)
- **Purpose**: Decode DataSource to SQL signature and returned fields
- **Input**: DataSource name/CodeName
- **Output**: SQL function, parameters, fields, joins, usage
- **Example**: "What does AA_tfnAllocationReport query?" → Function signature, joins, field list

---

### Tier 1.5: Expression & Transform (Specialized Universal)

**Enables rule writing and data transformation** — used by Tier 2 and 3 skills.

#### [09-XPATH-NAVIGATOR](./Tier-1.5-Transform/09-XPATH-NAVIGATOR)
- **Purpose**: Write XPath expressions for workflow validation and calculations
- **Input**: Goal (validate, calculate, filter), data structure, test data
- **Output**: XPath expression, test cases, English translation
- **Used by**: Workflow Designer, Compliance Architect
- **Example**: "Validate SettleDate > TradeDate" → XPath expression + test cases

#### [10-XSLT-TRANSFORMER](./Tier-1.5-Transform/10-XSLT-TRANSFORMER)
- **Purpose**: Create XSLT transformations to convert and map XML data
- **Input**: Source format, target format, mapping rules
- **Output**: Complete XSLT stylesheet, test results
- **Used by**: Integration workflows, data imports
- **Example**: "Map Geneva XML to Allvue XML" → Complete XSLT transformation ready to run

---

### Tier 2: Domain-Specific (Building Layer)

**Build configurations** — each depends on Tier 1 Foundation + Tier 1.5 Transform.

#### [04-WORKFLOW-DESIGNER](./Tier-2-Domain/04-WORKFLOW-DESIGNER)
- **Purpose**: Design trade/order workflows with constraints and validation
- **Uses**: Object Resolver, Reference Tracer, XPath Navigator
- **Input**: Asset type, process, fields, business rules
- **Output**: Workflow + steps + validation rules + XML
- **Example**: "Build a Bond trading workflow" → Complete workflow XML ready to import

#### [05-COMPLIANCE-ARCHITECT](./Tier-2-Domain/05-COMPLIANCE-ARCHITECT)
- **Purpose**: Design compliance rule matrices, scenario tests, ratings
- **Uses**: Object Resolver, Reference Tracer, DataSource Decoder, XPath Navigator
- **Input**: Guidelines, ratings, test cases, portfolios
- **Output**: Compliance framework + tests + scenarios + matrix
- **Example**: "Build sector concentration limits with stress testing" → Complete compliance framework

#### [06-REPORT-GENERATOR](./Tier-2-Domain/06-REPORT-GENERATOR)
- **Purpose**: Generate reports with DataSource binding, roles, export formats
- **Uses**: Object Resolver, DataSource Decoder
- **Input**: Purpose, data source, metrics, filters, export format
- **Output**: Report + parameters + role access + distribution
- **Example**: "Build daily allocation report" → Report XML with scheduling

---

### Tier 3: Integration (Complex Multi-Step)

**Orchestrate complex implementations** — combine all previous tiers.

#### [07-CONFIGURATION-CLONER](./Tier-3-Integration/07-CONFIGURATION-CLONER)
- **Purpose**: Clone object configurations with reference adjustments
- **Uses**: Object Resolver, Reference Tracer, DataSource Decoder
- **Input**: Source object + target name + adjustments
- **Output**: Cloned XML files + import package + validation scripts
- **Example**: "Duplicate a portfolio with new inception date" → Complete import package ready to deploy

#### [08-SOW-SCOPE-GENERATOR](./Tier-3-Integration/08-SOW-SCOPE-GENERATOR)
- **Purpose**: Generate SOW with object estimates, timelines, costs
- **Uses**: All Tier 1, 1.5, & 2 skills for comprehensive estimation
- **Input**: Client scope (portfolios, asset classes, compliance, integrations, users)
- **Output**: SOW document + resource plan + cost breakdown + timeline
- **Example**: "Estimate a new client project" → Complete SOW with effort & cost

---

## Directory Structure

```
Allvue-Skills/
├── Tier-1-Foundation/
│   ├── 01-OBJECT-RESOLVER/
│   │   ├── SKILL.md              (1-page quick reference)
│   │   ├── README.md             (deployment guide)
│   │   └── 01-OBJECT-RESOLVER.md (full implementation)
│   ├── 02-REFERENCE-TRACER/
│   ├── 03-DATASOURCE-DECODER/
│
├── Tier-1.5-Transform/
│   ├── 09-XPATH-NAVIGATOR/
│   └── 10-XSLT-TRANSFORMER/
│
├── Tier-2-Domain/
│   ├── 04-WORKFLOW-DESIGNER/
│   ├── 05-COMPLIANCE-ARCHITECT/
│   └── 06-REPORT-GENERATOR/
│
├── Tier-3-Integration/
│   ├── 07-CONFIGURATION-CLONER/
│   └── 08-SOW-SCOPE-GENERATOR/
│
├── README.md                 (this file)
└── SUITE-MANIFEST.json       (deployment manifest)
```

---

## How to Use

### For Individual Skills
1. Navigate to the tier folder (Tier-1-Foundation, Tier-2-Domain, etc.)
2. Open the skill folder (e.g., 01-OBJECT-RESOLVER)
3. Start with **SKILL.md** — 1-page quick reference (5 min read)
4. Read **README.md** — deployment guide with examples (10 min read)
5. Refer to implementation file for full details

### For Suite Deployments
1. Deploy all tiers together as a unified "Allvue Skills" package
2. Each tier depends on previous tiers — deploy in order:
   - **Step 1**: Deploy Tier 1 Foundation (Skills 01-03)
   - **Step 2**: Deploy Tier 1.5 Transform (Skills 09-10)
   - **Step 3**: Deploy Tier 2 Domain (Skills 04-06)
   - **Step 4**: Deploy Tier 3 Integration (Skills 07-08)
3. Users access all 10 skills; they can start at any appropriate tier for their use case

---

## Real-World Example Workflows

### Workflow 1: Add a New Portfolio
1. **Object Resolver**: Look up existing portfolio structure
2. **Configuration Cloner**: Clone to new portfolio with adjustments
3. **Reference Tracer**: Verify no broken references
4. **Done** — ready to deploy

### Workflow 2: Create Compliance Rules with Stress Testing
1. **Object Resolver**: Understand existing compliance tests
2. **DataSource Decoder**: Verify compliance data source has required fields
3. **XPath Navigator**: Design rule expressions for stress scenarios
4. **Compliance Architect**: Build scenario matrix + tests
5. **Reference Tracer**: Map which portfolios are affected
6. **Done** — ready to deploy

### Workflow 3: Estimate a Full Implementation Project
1. **SOW Generator**: Input client scope (portfolios, asset classes, compliance, integrations, users)
2. **Output**: Object counts, effort estimates, timeline, cost
3. **Reference Tracer**: Identify complexity drivers
4. **Done** — SOW ready to send

---

## Based On

All skills are built on the [Allvue Architecture Reference](../_References/ALLVUE-ARCHITECTURE-REFERENCE.md):

- **170 Allvue Object Types** across 13 domains
- **300+ Foreign Key Relationships** in SQL schema
- **1,710+ SQL Table Definitions** with complete schema
- **16,500+ XML Configurations** from 4 real client implementations
- **4 Client Reference Implementations**: Apax, BDT-MSD, Searchlight, TWGGlobal

---

## Deployment Ready

✅ **Production-Ready** — All 10 skills tested across 4 real client implementations  
✅ **Fully Documented** — SKILL.md + README.md + full implementation per skill  
✅ **Dependency Mapped** — Clear tier structure and inter-skill dependencies  
✅ **Real Examples** — Every skill includes practical, tested examples  
✅ **Unified Reference** — All skills reference single Allvue architecture model

---

## Next Steps

1. **New to Allvue?** Start with **Tier 1: Foundation** to master the basics
2. **Building a workflow?** Use **Tier 1.5 + Tier 2** workflow path
3. **Designing compliance?** Use **Tier 1 + Tier 1.5 + Tier 2** compliance path
4. **Estimating a project?** Use **Tier 3 SOW Generator** which calls all skills

Each skill is self-contained but most powerful when combined with others in the suite.

---

**Status**: Production-Ready  
**Last Updated**: 2026-09-23  
**Based On**: Complete Allvue analysis across 4 clients, 16,500+ configurations  
**Version**: 1.0
