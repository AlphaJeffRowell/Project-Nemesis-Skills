# Skills Metadata Registry

**Master definitions for all 11 Allvue & Cross-Project Skills**

---

## Tier 1: Foundation Skills (Universal Understanding)

### 01-OBJECT-RESOLVER

| Attribute | Value |
|-----------|-------|
| **Title** | Object Resolver — Complete Dependency Chain Resolution |
| **Overall Value Add** | Answer "What is this object?" — resolve ANY Allvue object to its complete type, references, SQL resolution, and usage context across the system |
| **Internal/External** | **Internal** — Used within Allvue; powers architecture investigation and impact analysis |
| **Explanation is** | For any Allvue object (Portfolio, Report, Workflow, etc.), this skill resolves: object type, complete foreign key references, SQL-level dependencies, and all downstream usage. Answers: "Where is X used? What does it depend on? What breaks if deleted?" |
| **Demo** | Input: "Daily Allocation Report" → Output: Type (BMS.LTD.Domain.UI.Report), DataSource (AA_tfnAllocationReport), SQL (Custom.AA_tfnAllocationReport with parameters), Joins (Trade + Portfolio + Allocation), Referenced by (WebDashboard, ScheduledTask, RoleReport) |

---

### 02-REFERENCE-TRACER

| Attribute | Value |
|-----------|-------|
| **Title** | Reference Tracer — Cascading Impact Analysis & Risk Assessment |
| **Overall Value Add** | Answer "If I change/delete X, what breaks?" — trace cascading dependencies, quantify impact, assess risk, and provide mitigation strategies |
| **Internal/External** | **Internal** — Used within Allvue for change management and risk assessment |
| **Explanation is** | When you modify, delete, or reconfigure an Allvue object, this skill traces ALL downstream impacts: broken references, broken reports, broken workflows, and provides impact severity (LOW/MEDIUM/HIGH/CRITICAL) with SQL cleanup steps. Used before making architectural changes. |
| **Demo** | Input: Delete ComplianceTest "SectorConcentration_Limit" → Output: Direct impact (15 PortfolioComplianceSetting records), Broken reports (ComplianceExceptionReport, DailyMonitoring), Risk level (HIGH — automated workflows depend), Mitigation (Re-assign to different test first), SQL cleanup (DELETE from PortfolioComplianceSetting WHERE ComplianceTestID=X) |

---

### 03-DATASOURCE-DECODER

| Attribute | Value |
|-----------|-------|
| **Title** | DataSource Decoder — SQL Signature & Field Resolution |
| **Overall Value Add** | Answer "What SQL does this DataSource execute?" — decode DataSource definitions to complete SQL function signature, parameters, returned fields, and joins |
| **Internal/External** | **Internal** — Used within Allvue for data flow understanding and report building |
| **Explanation is** | For any DataSource in Allvue (used in reports, web dashboards, workflows), this skill resolves: underlying SQL function name and signature, all parameters (with defaults), returned fields/columns, SQL joins involved, row count estimates, and all objects that consume it. Powers report building and data integration. |
| **Demo** | Input: "AA_tfnAllocationReport" → Output: Function (Custom.AA_tfnAllocationReport(@StartDate, @EndDate, @PortfolioID)), Returns ([Portfolio, TotalQty, AllocationCount, Variance%, Status]), Joins (Portfolio JOIN Trade JOIN Allocation), Base table ([Trade].[Allocation], 500K-2M rows typical), Used by (Report_DailyAllocation, WebDashboard_Operations) |

---

## Tier 1.5: Expression & Transform Skills (Specialized but Universal)

### 09-XPATH-NAVIGATOR

| Attribute | Value |
|-----------|-------|
| **Title** | XPath Navigator — Validation Rule & Calculation Expression Builder |
| **Overall Value Add** | Build XPath expressions for workflow validation rules, compliance conditions, and field calculations — handles all expression logic needed throughout Allvue |
| **Internal/External** | **Internal** — Used within Allvue workflows, compliance tests, and validation rules |
| **Explanation is** | XPath powers validation rules in Allvue workflows and compliance checks. This skill helps you write correct XPath for: date validations (SettleDate > TradeDate), quantity checks (Qty < MaxQty), calculations (allocation %, weighted averages), and conditional logic (IF SettleType='T+0' THEN Rate<=X). Includes test cases and English translation. |
| **Demo** | Input: Goal="Validate SettleDate > TradeDate" → Output: XPath (/Trade/SettleDate > /Trade/TradeDate), Used in (Workflow validation, compliance conditions), Test (TradeDate=2026-01-15, SettleDate=2026-01-20 → true ✓), English (Settlement date must be after trade date) |

---

### 10-XSLT-TRANSFORMER

| Attribute | Value |
|-----------|-------|
| **Title** | XSLT Transformer — XML Data Mapping & Integration Transformations |
| **Overall Value Add** | Build XSLT transformations to map and convert XML data between Allvue and external systems — handles all system integration scenarios |
| **Internal/External** | **Internal/External** — Maps between Allvue (internal) and external systems (Geneva, Bloomberg, custodians, legacy OMS) |
| **Explanation is** | XSLT transforms XML data for imports, exports, and integrations. This skill builds complete XSLT stylesheets to: map field names (FundID → CodeName), convert data types (dates, numbers), calculate new fields (from source data), filter records, and structure XML for Allvue import. Includes test data and validation. |
| **Demo** | Input: Source=Geneva XML, Target=Allvue Portfolio XML → Output: Complete XSLT mapping template, Field transformations (FundID → CodeName, dates ISO→SQL, numbers decimal→currency), Structure mapping (Geneva XML hierarchy → Allvue flat), Result (Allvue-ready XML ready to import), Test data with 5 sample records |

---

## Tier 2: Domain-Specific Skills (Building Configurations)

### 04-WORKFLOW-DESIGNER

| Attribute | Value |
|-----------|-------|
| **Title** | Workflow Designer — Trading & Order Process Workflow Builder |
| **Overall Value Add** | Design complete trading/order workflows for any asset type with validation rules, state transitions, and role-based access control|
| **Internal/External** | **Internal** — Used within Allvue for trade execution, order management, and process automation |
| **Explanation is** | Builds complete Allvue Workflow configurations for trading processes. This skill creates: workflow structure (name, description, process type), workflow steps (sequence with conditions), validation rules (XPath expressions), state transitions (Order → Confirmed → Allocated → Settled), role access (who can edit each step), and complete XML ready to import. Works for any asset class (Bond, Equity, Loan, Warrant, Option, etc.). |
| **Demo** | Input: Asset Type=Bond, Process=Trade Execution, Fields=[Quantity, SettleDate, Factor, CollateralRate], Rules=[SettleDate>TradeDate, Factor≤1.0] → Output: Workflow "Bond Trading", Steps (Order Entry→Verification→Allocation→Settlement), Validations (XPath for date/qty/rate), Roles (Analyst step 1, PM step 2, Operations step 4), Workflow_Bond_Trading.xml (ready to import) |

---

### 05-COMPLIANCE-ARCHITECT

| Attribute | Value |
|-----------|-------|
| **Title** | Compliance Architect — Rule Matrix, Scenario, & Rating Framework Builder |
| **Overall Value Add** | Design compliance rule matrices, scenario tests, and rating methodologies — builds complete compliance framework for portfolios |
| **Internal/External** | **Internal** — Used within Allvue for compliance testing, monitoring, and reporting |
| **Explanation is** | Builds complete Allvue Compliance configurations including: ComplianceTest objects (limits, rules), RatingMethodology (map external ratings to internal risk tiers), ComplianceScenario (market stress tests, liquidity stress), PortfolioComplianceMatrix (which rules apply to which portfolios), and all XML ready to import. Handles sector limits, credit quality, leverage constraints, and stress scenarios. |
| **Demo** | Input: Guidelines=[No sector>25% AUM, Min 80% BBB+, Max leverage 2.0x], Ratings=Moody's, Scenarios=[20% market drop, liquidity crisis] → Output: ComplianceTest "SectorConcentration_Limit", RatingMethodology "Moody's→InternalRiskTier", ComplianceScenario "MarketStress_20pct_Drop", PortfolioComplianceMatrix (5 portfolios × 8 rules), Compliance_Framework.xml (ready to import) |

---

### 06-REPORT-GENERATOR

| Attribute | Value |
|-----------|-------|
| **Title** | Report Generator — Configuration-Driven Report Builder |
| **Overall Value Add** | Generate reports with DataSource bindings, role-based access, export formats, and scheduled delivery — creates complete report configurations |
| **Internal/External** | **Internal** — Used within Allvue for operational reporting, executive dashboards, and scheduled delivery |
| **Explanation is** | Builds complete Allvue Report configurations including: Report object (name, parameters, filters), DataSource binding (which SQL DataSource provides data), Column definitions (field names, formats, calculations), RoleReport (role-based access: Admin/PM/Operations with different export options), ReportScheduledTask (email delivery schedule), and all XML ready to import. Handles Excel export, PDF output, and dashboard embedding. |
| **Demo** | Input: Purpose=Daily operations, Data=Allocation by portfolio, Metrics=[Qty, variance, status], Export=Excel, Distribution=Email daily 8am → Output: Report "Daily Allocation Report", DataSource "AA_tfnAllocationReport", Columns (Portfolio, Qty, Count, Variance%, Status), RoleReport (Admin full, PM Excel export, Operations view), ReportScheduledTask (daily 8am delivery), Report_DailyAllocation.xml (ready to import) |

---

## Tier 3: Integration Skills (Complex Multi-Step Tasks)

### 07-CONFIGURATION-CLONER

| Attribute | Value |
|-----------|-------|
| **Title** | Configuration Cloner — Object Duplication with Reference Adjustments |
| **Overall Value Add** | Clone any Allvue object configuration (portfolio, workflow, compliance rules) with automatic reference updates — handles all dependencies |
| **Internal/External** | **Internal** — Used within Allvue for rapid configuration replication and deployment|
| **Explanation is** | Takes a source Allvue object and clones it to a new target with reference adjustments. For portfolios: creates Portfolio, SubPortfolio, PortfolioCustom, PortfolioComplianceSetting with updated references. For workflows: creates new workflow with same structure, updated names. Generates cloned XML files, CLONE_MANIFEST.json (metadata), VALIDATION_QUERIES.sql (verify success), ROLLBACK_SCRIPT.sql (if needed), and IMPORT_INSTRUCTIONS.txt. |
| **Demo** | Input: Source="AllVue ClearPar Fund 1" (Portfolio), Target="AllVue ClearPar Fund 2", Adjustments=[Inception=2026-09-15, Currency=EUR] → Output: Portfolio_ClearPar_Fund2.xml, SubPortfolio_ClearPar2-ClassA.xml, SubPortfolio_ClearPar2-ClassB.xml, PortfolioCustom_ClearPar2.xml, PortfolioComplianceSetting_ClearPar2.xml, CLONE_MANIFEST.json, VALIDATION_QUERIES.sql, ROLLBACK_SCRIPT.sql, IMPORT_INSTRUCTIONS.txt |

---

### 08-SOW-SCOPE-GENERATOR

| Attribute | Value |
|-----------|-------|
| **Title** | SOW Scope Generator — Project Estimation & Statement of Work Builder |
| **Overall Value Add** | Generate complete Statements of Work with accurate object count estimates, effort calculations, cost breakdowns, resource plans, and timelines |
| **Internal/External** | **External** — Used for client SOWs, project estimation, and sales proposals |
| **Explanation is** | Takes client scope (number of portfolios, asset classes, compliance rules, integrations, users) and generates complete SOW including: object count estimates (based on Allvue architecture), effort in hours (configuration, testing, UAT), resource plan (team size, roles, duration), cost breakdown (labor, infrastructure, contingency), timeline with phases (weeks), risk assessment, and mitigations. Produces professional SOW_Document.docx ready to send to client. |
| **Demo** | Input: Portfolios=5, Asset Classes=[Bond, Equity, Loan, Warrant], Compliance=[8 rules+stress], Integrations=[Geneva, Bloomberg, Custodian], Users=25, Timeline=6 months → Output: Object count 180+ to configure, Effort 1,300 config hours + testing, Resource plan 1 lead+2 devs+1 QA (8-12 weeks), Cost $244K labor+$43K infra+contingency=$292K, Timeline 12 weeks (phases), Risk assessment & mitigations, SOW_Document.docx (ready to send) |

---

## Cross-Project Automation Skills

### 11-ASANA-TASK-UPDATE

| Attribute | Value |
|-----------|-------|
| **Title** | Asana Task Update — Meeting Notes to Task Sync with Extended Actions |
| **Overall Value Add** | Transform meeting notes (natural language + optional syntax) into Asana task updates with full action support (comments, due dates, assignments, completion, custom fields) — unified sync across teams |
| **Internal/External** | **External** — Works with any project; dual-source (SharePoint + local repo) with team deduplication |
| **Explanation is** | Parses meeting notes to identify action items, fuzzy-matches to existing Asana tasks (or creates new ones), executes extended actions (add comment, set due date, assign, mark complete, update custom fields), and posts summary with team deduplication. Supports dry-run preview mode for validation. Primary: MCP skill (recommended). Secondary: Python script (fallback). Answers: "How do I get meeting notes into Asana with extended actions and team coordination?" |
| **Demo** | Input: Meeting notes "Bob: Update Allvue config by Friday. Sarah: Review compliance rules." → Parse: Task 1 (update config, assign Bob, due Fri), Task 2 (review rules, assign Sarah) → Fuzzy match existing tasks → Execute: Add comments, set due dates, assign → Dry-run preview → Post with deduplication → Result: Asana updated, meeting notes → tasks automated |

---

## Cross-Project Scaffolding Skills

### new-project (Scaffolding & Deployment)

| Attribute | Value |
|-----------|-------|
| **Title** | New Project Scaffolder — Client Project Structure & Deployment Automation |
| **Overall Value Add** | Scaffold complete client project folder structure with phase nesting, git initialization, templates, deployment scripts, and AI settings — ready for Phase 1 |
| **Internal/External** | **Internal** — Used to set up new client implementation projects |
| **Explanation is** | Creates standardized folder hierarchy for new client projects at C:\Repo\Project\Project-<CLIENT>. Includes: phase-nested directories (Phase 1 - <TYPE>), git repo initialization, README templates, deployment scripts, .claude/settings.json for AI tooling, CLAUDE.md instructions. All folders structured for handoff between team members and Claude Code automation. |
| **Demo** | Input: ClientCode="TWG", ClientName="TWG Global", PhaseDescription="Multi-Module IA/FA/FO Setup" → Output: Project-TWG/ folder with Phase 1 - Multi-Module IA/FA/FO Setup/, git init, CLAUDE.md, .claude/settings.json, README.md, deployment scripts, ready for team |

---

## Master Metadata Summary

| # | Skill Name | Type | Value Add (One Line) | I/E | Tier |
|---|------------|------|-------|-----|------|
| 1 | Object Resolver | Foundation | Resolve any object to complete dependency chain | INT | 1 |
| 2 | Reference Tracer | Foundation | Trace cascading impacts of changes + risk assessment | INT | 1 |
| 3 | DataSource Decoder | Foundation | Decode DataSource to SQL signature + fields | INT | 1 |
| 4 | XPath Navigator | Expression | Write XPath validation rules + calculations | INT | 1.5 |
| 5 | XSLT Transformer | Transform | Create XSLT data mappings between systems | INT/EXT | 1.5 |
| 6 | Workflow Designer | Domain | Build trading/order workflows with validation | INT | 2 |
| 7 | Compliance Architect | Domain | Design compliance rule matrices + scenarios | INT | 2 |
| 8 | Report Generator | Domain | Generate reports with DataSource binding | INT | 2 |
| 9 | Configuration Cloner | Integration | Clone objects with reference adjustments | INT | 3 |
| 10 | SOW Scope Generator | Integration | Generate SOW with project estimates | EXT | 3 |
| 11 | Asana Task Update | Automation | Sync meeting notes to Asana with actions | EXT | X |
| 12 | New Project Scaffolder | Scaffolding | Scaffold client project structure | INT | X |

---

**Created:** 2026-09-17  
**Status:** Complete ✅  
**All 12 skills defined with Title, Value Add, Internal/External, Explanation, and Demo**
