# Allvue Comprehensive Architecture Reference

**Complete Dependency Graph & Object Model**  
Generated: 2026-09-15  
Source: 4 clients, ~16,500 XML configurations, 70+ object types, 300+ SQL relationships

---

## QUICK START: Universal Object Reference Pattern

Every Allvue configured object follows this pattern:

```
Object (DataPanel, Report, Workflow, etc.)
├─ Name / CodeName (unique identifier)
├─ Type (BMS.LTD.Domain.{Module}.{ObjectType})
├─ References (what objects it depends on)
│  ├─ Direct Type References
│  ├─ SQL ComplexLookup joins
│  ├─ DataSource by name
│  └─ Parameters (@placeholders)
├─ Collections (child objects, role access)
└─ SQL Resolution (database tables/views/functions)
```

---

## OBJECT TYPES BY DOMAIN (170 types, 13 domains)

### 1. Data Layer (Most Referenced)
- **DataPanel** - UI data display grid/form
  - References: DataSource (by ComplexLookup SQL join)
  - Referenced by: WebDashboardWidget, DataPanelView, UI components
  - SQL Pattern: `SELECT dsp.ID FROM [Client].[DataSourceParameter] dsp JOIN [client].[DataSource] ds WHERE dsp.Name='@ParameterName'`

- **DataSource** - SQL table functions / stored procedures
  - References: DataSourceParameter, SQL table/function
  - Referenced by: DataPanel, Report, CalendarPanel
  - SQL Pattern: `Custom.AA_tfnDataDictionaryDataProperty(@parameters)`

- **DataPanelView** - Variant displays of DataPanel
  - References: DataPanel, display rules
  - Referenced by: Web UI layer

### 2. Workflow Layer
- **Workflow** - Order/trade processing rules
  - References: WorkflowType, AssetType, WorkflowStep
  - Uses: WorkflowDataPropertyUsage (maps to Trade, TradeCustom fields)
  - SQL Pattern: `bms:coalesce(/Trade/Factor, 1)`, `bms:bizDate(string(/Trade/TradeDate))`

- **WorkflowStep** - States within workflow
- **Workflow-CVOS** - Change Value On Save rules
- **Workflow-VOS** - Variant On Save rules
- **Workflow-AutoTransitions** - Automatic state transitions

### 3. Portfolio Layer
- **Portfolio** - Fund/vehicle master record
  - Properties: AbbrevName, CurrencyType, InceptionDate, IsPortfolioGroup, HasSubAllocationSplits
  - References: SubPortfolio, PortfolioCustom, PortfolioComplianceSetting

- **SubPortfolio** - Share class / sub-fund
- **PortfolioCustom** - Extended fields (16 Date, 8 Int, 8 Money, 8 Percent, 16 List, 16 Text slots)

### 4. Compliance Layer
- **ComplianceScenario** - What-if compliance tests
  - References: ComplianceScenarioColumn, ComplianceScenarioDataObject, ComplianceScenarioDataSource
  - Sub-types: ComplianceScenarioColumn, Table, Expression, DataSource, DataObject

- **ComplianceTest** - Automated rule testing
- **ComplianceRank** - Severity classification
- **RatingMethodology** - Rating scale definitions
- **RatingRule** - Individual rating rule
- **DiscountLogic** - Collateral haircut rules
- **LongDatedLogic** - Special handling for long-dated securities

### 5. Trade & Allocation Layer
- **AllocationMethodology** - How trades allocate across portfolios
  - Example codes: Available_Capital, ProRata, Available_Capital_Pro_Rata, Target_BPS
  - References: TradeTransactionType
  - ConfigXML: 900+ chars with flags (REMOVE_ZERO_ALLOCATIONS, ALLOW_PARTIAL_ALLOCATION, IGNORE_INCREMENTS, etc.)

- **AllocationTemplate** - Template for standard allocations
- **AllocationRuleExpression** - Expression-based allocation rules
- **AllocationRuleLimit** - Quantity/amount limits
- **AllocationRuleRestriction** - Portfolio restrictions

### 6. Asset/Financial Layer
- **AssetType** - Security classification
  - Examples: Bond, Equity, Loan, ABS, CDS, Option, FX, Repo, TRS, Warrant
  - References: BackOfficeExternalID (e.g., WSO:2000 for Bond)

- **CapStructureTemplate** - Capital structure for credit analysis
- **FinancialTemplate** - Financial statement templates
- **DiscountLogic** - Haircut/discount calculations

### 7. Security & Administration Layer
- **Role** - Access control roles
  - Standard roles: Administrator, Portfolio Manager, Analyst, Trader, Operations, API, Power User
  - References: RoleBasePanel (panel-level access), RoleReport (report access), RoleWebDashboard

- **User** - System user accounts
- **RoleBasePanel** - Role → DataPanel → permissions (CanExport, CanEdit)
- **RoleReport** - Role → Report access

### 8. Reporting Layer
- **Report** - Report definitions
  - References: ReportCategory (hierarchical), DataSource, Export format
  - Report types: Excel (.xlsx), PDF, HTML, Word

- **ReportCategory** - Hierarchical report organization
- **ReportPanel** - Panel-based reporting interface

### 9. UI/Web Layer
- **WebDashboard** - Dashboard interface
- **WebDashboardWidget** - Widget within dashboard
- **WebPanel** - Web form/page
- **WebDataPanelView** - Web variant of DataPanelView
- **WebChart** - Chart visualization
- **Hub** - Portal navigation interface

### 10. Reference Data Layer
- **List** - Master list definitions
- **ListItem** - List values (e.g., "Active", "Inactive", "On Watch")
- **Country** - Geographic country codes
- **CurrencyType** - Supported currencies (USD, EUR, GBP, etc.)
- **StateProvince** - Geographic state/province data

### 11. Business Rules Layer
- **RuleExpression** - Reusable calculation rules
- **RuleFunction** - Custom function definitions
- **GlobalAction** - Global-level custom actions

### 12. Configuration & Templates Layer
- **DataObjectTemplate** - Form template for object entry
- **ClientSetting** - Client-level configuration
- **ApplicationSetting** - System-wide settings
- **Custom Fields** - Extensible field definitions
- **DocumentTemplate** - Document generation templates

### 13. Integration Layer
- **DataSource** - SQL integration endpoints
- **EventSubscription** - Event-driven automation
- **Listener** - Event listeners
- **Publisher** - Event publishers
- **ExtractionPackage** - Data extraction definitions

---

## REFERENCE CHAINS: Complete Examples

### Chain 1: WebDashboard Widget → Trade Data
```
WebDashboardWidget
  ├─ references: DataPanel (CodeName="AA Data Dictionary")
  └─ DataPanel
     ├─ executes ComplexLookup SQL
     ├─ joins: [Client].[DataSourceParameter] + [Client].[DataSource]
     └─ finds: DataSource (CodeName="AA_tfnDataDictionaryDataProperty")
        └─ executes: Custom.AA_tfnDataDictionaryDataProperty(@DataObjectID)
           └─ queries: [Dictionary].[DataProperty], [Dictionary].[DataObject]
              └─ returns: DataPropertyID, DataPropertyName, DataObjectID, DataObjectName
```

### Chain 2: Trade Workflow → Execution
```
Workflow (CodeName="Bond")
  ├─ WorkflowType: Bond Processing
  ├─ AssetType: Bond (BackOfficeSystemID=WSO, ExternalID=2000)
  ├─ WorkflowDataPropertyUsage (5 fields):
  │  ├─ CollateralRate (Trade.CollateralRate)
  │  ├─ SettleDate (Trade.SettleDate)
  │  ├─ TargetWeightOrdered (Trade.TargetWeightOrdered)
  │  ├─ Date1 (TradeCustom.Date1, label="Repo End Date")
  │  └─ Number3 (TradeCustom.Number3)
  ├─ XPath Expressions:
  │  ├─ bms:coalesce(/Trade/Factor, 1)
  │  └─ bms:bizDate(string(/Trade/TradeDate))
  └─ WorkflowStep variations (CVOS, VOS, AutoTransitions)
```

### Chain 3: Allocation Methodology → Portfolio Split
```
AllocationMethodology (CodeName="Available_Capital_Pro_Rata")
  ├─ TradeTransactionType: Purchase
  ├─ ConfigXML flags:
  │  ├─ IS_TARGETED: True
  │  ├─ REMOVE_ZERO_ALLOCATIONS: True
  │  └─ ALLOW_PARTIAL_ALLOCATION: False
  ├─ applied to: Trade objects
  └─ creates: Allocation records
     ├─ Portfolio: Allocated portfolio
     ├─ AllocationQuantity: Calculated split
     └─ stored in: [Trade].[Allocation]
```

### Chain 4: Compliance Scenario → Rule Enforcement
```
ComplianceScenario (e.g., "Sector Concentration")
  ├─ ComplianceScenarioColumn (definition of calculation column)
  ├─ ComplianceScenarioDataSource (SQL source)
  ├─ ComplianceScenarioDataObject (references Portfolio, Position, etc.)
  ├─ ComplianceScenarioExpression (calculation logic)
  ├─ ComplianceScenarioTable (result table structure)
  ├─ RatingMethodology (e.g., Moody's ratings)
  └─ stored in: [Compliance].[ComplianceScenario*] tables
```

### Chain 5: Report Generation → Export
```
Report (CodeName="Allocation Report Excel")
  ├─ ReportCategory: "Reports > Trade > Allocation"
  ├─ DataSource: "AllocationReportDataSource"
  ├─ ReportTypeID: 109110 (Excel)
  ├─ AvailableExportFormats: [106905, 106909]
  ├─ RoleReport (access control):
  │  ├─ Administrator: CanEdit=True, CanExport=True
  │  └─ Analyst: CanExport=True, CanEdit=False
  └─ execution:
     ├─ resolves DataSource to: Custom.AA_tfnAllocationReport
     ├─ executes with parameters: @StartDate, @EndDate, @Portfolio
     └─ returns: Allocation data for Excel export
```

---

## UNIVERSAL SQL PATTERNS

### Pattern 1: ComplexLookup SQL Join
```sql
SELECT {ObjectTable}.ID 
FROM [{Schema}].[{ObjectTable}] AS {t1}
JOIN [{Schema}].[{ReferenceTable}] AS {t2} 
  ON {t2}.ID = {t1}.{ForeignKeyColumn}
WHERE {t1}.CodeName = '{CodeNameValue}' 
  AND {t2}.CodeName = '{ReferenceCodeNameValue}'
```

### Pattern 2: DataSourceParameter Resolution
```sql
SELECT dsp.ID 
FROM [Client].[DataSourceParameter] dsp 
INNER JOIN [client].[DataSource] ds ON ds.ID = dsp.DataSourceID 
WHERE dsp.[Name]='@{ParameterName}' 
  AND ds.CodeName='{DataSourceCodeName}'
```

### Pattern 3: Table Function Invocation
```sql
SELECT * FROM Custom.{TableFunctionName}(@parameter1, @parameter2, ...)
```

### Pattern 4: Foreign Key Reference
```sql
REFERENCES [Schema].[TableName] ([ColumnName])
```

---

## CLIENT DISTRIBUTION: Universal vs. Specialized

### Universal (All 4 Clients: Apax, BDT-MSD, Searchlight, TWGGlobal)
- DataPanel, DataSource, DataPanelView
- Workflow (all variations)
- Role, User, Security
- Report, ReportPanel, ReportCategory
- Portfolio, SubPortfolio
- AssetType, List, ListItem
- WebDashboard, WEB-Hub, WebPanel
- ApplicationSetting, ConfigurationSetting

### Specialized (Apax, BDT-MSD, TWGGlobal only - NOT Searchlight)
- Allocation Methodology, AllocationTemplate, AllocationRule*
- ComplianceScenario (full 6 variations), ComplianceTest, ComplianceRank
- CapStructureTemplate, FinancialTemplate
- DiscountLogic, LongDatedLogic, RatingMethodology
- Portfolio Compliance Matrix, Portfolio Compliance Setting
- GlobalAction, GlobalLink
- Listener, Publisher, EventSubscription
- DocumentExtractionHandler, ExtractionPackage

### Client-Specific
- TWGGlobal: Custom.BloombergIndices (schema extension)
- BDT-MSD: Heavy portfolio configuration (51 portfolios vs 0-6 in others)

---

## KEY METRICS

| Metric | Range | Notes |
|--------|-------|-------|
| Total Object Types | 31-70 | Searchlight=31 (lite), Others=69-70 (full) |
| DataPanels | 46-773 | Searchlight sparse (46), Others ~750+ |
| DataSources | 179-1,142 | Searchlight sparse (179), Others ~1,000+ |
| Workflows | 17-32 | Consistent 17-32 across all clients |
| Reports | 3-114 | Searchlight sparse (3), Others ~110 |
| Portfolios | 0-51 | BDT-MSD=51 (heavy), TWGGlobal=0, Others=5-6 |
| Roles | 2-36 | Varies by deployment size |
| Total XML Files | ~300-4,200 | Searchlight~300, Full clients~4,000+ |

---

## REFERENCE DATABASE SCHEMA (Key Tables)

```
[Client] Schema
├─ Client, Company, Contact, DataSource, DataSourceParameter, ClientSetting

[Security] Schema
├─ User, Role, RoleBasePanel, RoleReport, RoleWebDashboard

[Dictionary] Schema
├─ DataObject, DataProperty, DataObjectType

[Asset] Schema
├─ Asset, AssetType, AssetGroup, Contract LegType, Calendar, Country, CurrencyType

[Portfolio] Schema
├─ Portfolio, SubPortfolio, CashAccount, PortfolioCustom

[Trade] Schema
├─ Trade, Allocation, TradeTransactionType, AllocationMethodology

[Workflow] Schema
├─ Workflow, WorkflowType, WorkflowStep, WorkflowEntry, WorkflowList

[Compliance] Schema
├─ ComplianceScenarioColumn, ComplianceScenarioTable, RatingMethodology

[UI] Schema
├─ DataPanel, DataPanelField, WebPanel, WebDashboard, Report

[Apex] Schema (Custom Domain)
├─ Core_HistoricalLot, Core_ExternalAccounts, Recon_BackOfficeCashflow, Sub_HypoInvestorAllocation, CMP_*
```

---

## FILE LOCATIONS

- **BDT-MSD Example Files**: C:\repo\Clients\BDT-MSD\App Exports\
  - DataPanel example: DataPanel_AA Data Dictionary.xml
  - DataSource: DataSource_AA_tfnDataDictionaryDataProperty.xml
  - Workflow: Workflow_ABS Repo.xml
  - Allocation Methodology: Allocation Methodology_Available Capital (Pro Rata).xml

- **Database Schema**: C:\repo\Clients\BDT-MSD\Database\
  - Tables, Views, StoredProcedures, Functions, Types, Triggers folders

- **Allvue Library Docs**: C:\Repo\Project\_Allvue_Library\
  - Client registry, case studies, module guides

---

**Last Updated**: 2026-09-15  
**Data Sources**: Comprehensive analysis of 4 clients, ~16,500 XML configurations, 1,710+ SQL table definitions
