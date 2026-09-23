# Allvue Report Generator Skill

**Purpose**: Generate reports with correct DataSource binding, role access, and export formats  
**Tier**: Domain-Specific (Tier 2)  
**Use**: Build ad-hoc or scheduled reports with proper data source configuration

**Depends on**: Object Resolver, DataSource Decoder

---

## Input Format

```
Report Name: [string]
Purpose: [Executive Summary | Detail Drill | Exception Report | Scheduled Batch]
Data: [Portfolio data | Trade data | Allocation data | Compliance data]
Metrics: [list of metrics to include]
Filters: [optional: date range, portfolio, asset class]
Export Format: [Excel | PDF | HTML | Word]
Distribution: [Email | User Portal | Automated Batch]
Audience: [Portfolio Managers | Operations | Compliance | Executives]
```

## Examples

```
Name: "Daily Allocation Report"
Purpose: Scheduled Batch
Data: Trade execution, portfolio allocation
Metrics: Trade count, total quantity, allocation variance
Filters: By portfolio, daily
Export: Excel
Distribution: Email to operations team
Audience: Operations, Portfolio Managers

Name: "Compliance Exception Report"
Purpose: Exception Report
Data: Compliance test results
Metrics: Violations, guideline breaches, status
Filters: Open exceptions only
Export: Excel, PDF
Distribution: Email to CIO
Audience: Chief Investment Officer, Compliance
```

---

## Report Design Process

### Step 1: Define Report Purpose & Audience

Map business need to Allvue Report type:

```
Purpose Mapping:
├─ Executive Summary
│  └─ High-level dashboard, KPIs, exceptions
│  └─ Audience: C-suite, board
│  └─ Frequency: Daily, weekly
│
├─ Detail Drill
│  └─ Complete transaction/position data
│  └─ Audience: Portfolio managers, analysts
│  └─ Frequency: Ad-hoc
│
├─ Exception Report
│  └─ Guideline violations, breaches
│  └─ Audience: Compliance, risk management
│  └─ Frequency: Daily
│
└─ Scheduled Batch
   └─ Regulatory filings, month-end close
   └─ Audience: Finance, compliance
   └─ Frequency: Periodic (monthly, quarterly, annual)
```

### Step 2: Select Data Source

Use DataSource Decoder to find or create:

```
Data Source Selection:

For Trade Allocation Data:
├─ Use DataSource: "AA_tfnAllocationReport"
├─ Returns: [Portfolio, Quantity, AllocationPercent, Status]
├─ Parameters: [@StartDate, @EndDate, @PortfolioID]
└─ Cardinality: Typical 5,000-50,000 rows

For Compliance Data:
├─ Use DataSource: "ComplianceTestResults"
├─ Returns: [Portfolio, Test, Value, Limit, Status, DaysViolation]
├─ Parameters: [@PortfolioID, @AsOfDate]
└─ Cardinality: Typical 500-2,000 rows

For Portfolio Valuation:
├─ Use DataSource: "PortfolioValuationSnapshot"
├─ Returns: [Portfolio, Asset, Quantity, Price, MarketValue]
├─ Parameters: [@AsOfDate]
└─ Cardinality: Typical 1,000-10,000 rows
```

If needed, create new DataSource:

```
New DataSource: "TradeExecutionSummary"
├─ Type: Table Function
├─ SQL: Custom.TradeExecutionSummary
├─ Parameters: 
│  ├─ @StartDate (datetime)
│  ├─ @EndDate (datetime)
│  └─ @AssetType (int, optional)
├─ Returns:
│  ├─ TradeDate
│  ├─ Quantity
│  ├─ ExecutionPrice
│  ├─ Counterparty
│  └─ SettlementStatus
└─ Implementation:
   └─ Write SQL function in Custom schema
```

### Step 3: Define Report Metrics

Determine what data to display:

```
Report Metrics: "Daily Allocation Report"

Column 1: Portfolio Name
└─ Source: Portfolio.Name
└─ Type: Text

Column 2: Total Quantity
└─ Source: SUM(Trade.TradeQuantity where Status='Executed')
└─ Type: Decimal
└─ Format: 0.00

Column 3: Allocation Count
└─ Source: COUNT(Allocation.*) where PortfolioID={PortfolioID}
└─ Type: Integer

Column 4: Allocation Variance %
└─ Source: ABS((SUM(Allocation.Quantity) - Trade.TradeQuantity) / Trade.TradeQuantity)
└─ Type: Percent
└─ Format: 0.00%

Column 5: Status
└─ Source: CASE WHEN Variance < 0.1% THEN 'OK' ELSE 'INVESTIGATE'
└─ Type: Text
└─ Color: Green/Red
```

### Step 4: Define Filters & Parameters

Allow dynamic filtering:

```
Filter Parameters:

Parameter 1: Date Range
├─ Label: "Report Date"
├─ Type: @AsOfDate (datetime)
├─ Default: Yesterday
├─ Required: Yes
└─ Usage: Filter trades by TradeDate

Parameter 2: Portfolio
├─ Label: "Select Portfolio"
├─ Type: @PortfolioID (int, multi-select)
├─ Default: [All Portfolios]
├─ Required: No
└─ Usage: Filter allocations by PortfolioID

Parameter 3: Asset Class
├─ Label: "Asset Class"
├─ Type: @AssetTypeID (int, multi-select)
├─ Default: [All Assets]
├─ Required: No
└─ Usage: Filter by Asset.AssetTypeID

Parameter 4: Status
├─ Label: "Status"
├─ Type: List (ListItemID)
├─ Options: [Executed, Settled, Pending, Cancelled]
├─ Default: [Executed, Settled]
└─ Usage: WHERE Trade.Status IN (...)
```

### Step 5: Configure Export Formats

Define available export options:

```
Export Formats:

1. Excel (.xlsx)
   ├─ Format: Tabular with headers
   ├─ Features: Sorting, filtering, charts
   ├─ Size Limit: Up to 1M rows
   └─ Typical Use: Daily operations reports

2. PDF
   ├─ Format: Formatted report layout
   ├─ Features: Page breaks, footer/header
   ├─ Size Limit: Up to 100M
   └─ Typical Use: Executive summaries, distribution

3. HTML
   ├─ Format: Web-based interactive
   ├─ Features: Drill-down links, filters
   └─ Typical Use: Real-time dashboards

4. Word (.docx)
   ├─ Format: Narrative + table
   ├─ Features: Formatting, charts embedded
   └─ Typical Use: Monthly status reports
```

### Step 6: Set Role-Based Access

Define who can view/export:

```
Role-Based Permissions:

RoleReport: "Daily Allocation Report"

Administrator:
├─ CanView: Yes
├─ CanEdit: Yes
├─ CanExport: Yes
└─ CanSchedule: Yes

Portfolio Manager:
├─ CanView: Yes (own portfolios)
├─ CanEdit: No
├─ CanExport: Yes
└─ CanSchedule: No

Analyst:
├─ CanView: Yes
├─ CanEdit: No
├─ CanExport: Yes (Excel only)
└─ CanSchedule: No

Operations:
├─ CanView: Yes
├─ CanEdit: No
├─ CanExport: Yes
└─ CanSchedule: No
```

Create RoleReport entries:

```xml
<RoleReport>
  <ReportID>Report_{ReportCodeName}</ReportID>
  <RoleID>Role_Administrator</RoleID>
  <CanEdit>True</CanEdit>
  <CanExport>True</CanExport>
</RoleReport>

<RoleReport>
  <ReportID>Report_{ReportCodeName}</ReportID>
  <RoleID>Role_PortfolioManager</RoleID>
  <CanEdit>False</CanEdit>
  <CanExport>True</CanExport>
</RoleReport>
```

### Step 7: Design Report Structure

Organize columns and sections:

```
Report Structure: "Daily Allocation Report"

Header Section:
├─ Report Title: "Daily Allocation Report"
├─ Run Date: {AsOfDate}
├─ Run Time: {CurrentTime}
└─ Filter Summary: Portfolio={Portfolio}, Date={AsOfDate}

Detail Section:
├─ Column 1: Portfolio (width: 20%)
├─ Column 2: Total Quantity (width: 15%, right-aligned, format: 0.00)
├─ Column 3: Allocation Count (width: 15%, right-aligned)
├─ Column 4: Allocation Variance (width: 15%, right-aligned, format: 0.00%)
├─ Column 5: Status (width: 15%, colored)
├─ Column 6: Last Updated (width: 20%, format: 'MM/DD/YYYY HH:MM')
└─ Sorting: By Portfolio Name (ascending)

Summary Section:
├─ Total: All Portfolios
├─ Total Quantity (all): SUM(Column 2)
├─ Average Variance (all): AVG(Column 4)
├─ Status Breakdown: Count by status

Footer Section:
├─ Report Generated By: {UserName}
├─ Data Source: AA_tfnAllocationReport
├─ Refresh Frequency: Daily at 8:00 AM
└─ Contact: operations@firm.com
```

### Step 8: Create Scheduled Distribution

Define automated report delivery:

```
ReportScheduledTask: "Daily Allocation Report - Email"

Schedule:
├─ Frequency: Daily
├─ Time: 8:00 AM EST
├─ Timezone: America/New_York
└─ Days: Monday - Friday

Distribution:
├─ Format: Excel
├─ Recipients: 
│  ├─ operations@firm.com (To)
│  ├─ pm@firm.com (CC)
│  └─ cio@firm.com (BCC)
├─ Subject: "Daily Allocation Report - {AsOfDate}"
├─ Message: "See attached report for daily allocation summary"
└─ Attach: Daily_Allocation_{YYYYMMDD}.xlsx

Parameters:
├─ @AsOfDate: Yesterday's date (auto-calculated)
├─ @PortfolioID: All portfolios
└─ @Status: [Executed, Settled]

Error Handling:
├─ If data missing: Skip send, log error
├─ If timeout: Retry 3x with 5-min delay
└─ If send fails: Email alert to operations team
```

### Step 9: Generate Report XML Configuration

Create Report.xml:

```xml
<DataImportRequest Type="BMS.LTD.Domain.UI.Report">
  <DataObjectImports>
    <DataObjectImport Type="BMS.LTD.Domain.UI.Report">
      <DataProperties>
        <DataProperty Name="CodeName">
          <SimpleDataProperty Value="Daily_Allocation_Report" />
        </DataProperty>
        <DataProperty Name="Name">
          <SimpleDataProperty Value="Daily Allocation Report" />
        </DataProperty>
        <DataProperty Name="ReportCategoryID">
          <SimpleDataProperty Value="123" /> <!-- Reports > Daily > Allocation -->
        </DataProperty>
        <DataProperty Name="DataSourceID">
          <DataObjectDataProperty Type="BMS.LTD.Domain.Client.DataSource">
            <Lookup>
              <DataProperties>
                <DataProperty name="CodeName" value="AA_tfnAllocationReport" />
              </DataProperties>
            </Lookup>
          </DataObjectDataProperty>
        </DataProperty>
        <DataProperty Name="ReportTypeID">
          <SimpleDataProperty Value="109110" /> <!-- Excel type -->
        </DataProperty>
        <DataProperty Name="AvailableExportFormatIDs">
          <SimpleDataProperty Value="106905,106909" /> <!-- Excel, PDF -->
        </DataProperty>
        <DataProperty Name="PresentationTypeIDs">
          <SimpleDataProperty Value="112501,112502" />
        </DataProperty>
      </DataProperties>
    </DataObjectImport>
  </DataObjectImports>
</DataImportRequest>
```

### Step 10: Build Report Dashboard View

Create web dashboard integration:

```
WebDashboard: "Reports Center"
├─ Widget 1: Available Reports
│  ├─ DataPanel: "ReportList"
│  └─ Links to: Daily Allocation, Compliance, etc.
│
├─ Widget 2: Recent Reports
│  ├─ DataPanel: "RecentReports"
│  └─ Shows: Report name, run date, user, format
│
└─ Widget 3: Scheduled Reports
   ├─ DataPanel: "ScheduledReports"
   └─ Shows: Report, frequency, recipients, next run
```

---

## Output Format

```markdown
# Report Generator: {ReportName}

## Report Definition
- **Name**: {ReportName}
- **CodeName**: {CodeName}
- **Purpose**: {Purpose}
- **Category**: Reports > {Category} > {SubCategory}
- **Status**: Draft / Ready for Approval

## Data Configuration

**Primary DataSource**: {DataSourceName}
- **CodeName**: {DataSourceCodeName}
- **Type**: Table Function
- **SQL Function**: Custom.{FunctionName}
- **Cardinality**: Typical {RowCount} rows

**Parameters**:
| Parameter | Type | Default | Required | Usage |
|-----------|------|---------|----------|-------|
| @AsOfDate | datetime | Yesterday | Yes | Filter by date |
| @PortfolioID | int | All | No | Filter by portfolio |

## Report Metrics ({N} columns)

1. Portfolio Name
   - Source: Portfolio.Name
   - Type: Text
   - Width: 20%

2. Total Quantity
   - Source: SUM(Trade.TradeQuantity)
   - Type: Decimal
   - Format: 0.00
   - Width: 15%

3. [Additional columns...]

## Filters & Parameters

User-provided filters:
- [ ] Date Range (auto-populated to yesterday)
- [ ] Portfolio (multi-select, default all)
- [ ] Asset Class (multi-select, default all)
- [ ] Status (dropdown, default: Executed/Settled)

## Export Formats

Available exports:
- [x] Excel (.xlsx)
- [x] PDF
- [ ] HTML
- [ ] Word

## Role-Based Access

| Role | View | Export | Edit | Schedule |
|------|------|--------|------|----------|
| Administrator | Yes | Yes | Yes | Yes |
| Portfolio Manager | Yes | Excel | No | No |
| Analyst | Yes | Excel | No | No |
| Operations | Yes | Yes | No | No |

## Report Layout

**Header**:
- Title, Run Date/Time, Filter Summary

**Detail Section**:
- 6 columns with sorting by Portfolio Name
- Colored status indicators
- Typical 50-200 rows per portfolio

**Summary Section**:
- Total quantities, average variance, status breakdown

**Footer**:
- Report metadata, data source, contact info

## Scheduled Distribution

**Schedule**: Daily at 8:00 AM EST (M-F)
**Format**: Excel
**Recipients**: operations@firm.com, pm@firm.com (CC)
**Subject**: "Daily Allocation Report - {Date}"

## Implementation Checklist

- [ ] DataSource exists and tested
- [ ] Report parameters defined and validated
- [ ] Metrics SQL queries verified
- [ ] Role-based access configured
- [ ] Export format templates created
- [ ] Distribution list validated
- [ ] Error handling configured
- [ ] UAT completed and approved
- [ ] User training scheduled
- [ ] Production deployment ready

## Testing Checklist

- [ ] Data accuracy verified
- [ ] All parameters work correctly
- [ ] Export formats valid
- [ ] Role access enforced
- [ ] Performance acceptable (<5 sec for 100K rows)
- [ ] Email distribution working
- [ ] Retry logic functioning

## Related Objects

**DataSource**: {DataSourceName}
**ReportCategory**: Reports > {Category}
**ReportScheduledTask**: {ScheduledTaskName}
**WebDashboard**: Reports Center

---

This skill answers: **"How do I build a report?"**
