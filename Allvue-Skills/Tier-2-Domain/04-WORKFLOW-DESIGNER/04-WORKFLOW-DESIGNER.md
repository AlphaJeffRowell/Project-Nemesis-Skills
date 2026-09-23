# Allvue Workflow Designer Skill

**Purpose**: Design trade/order workflows with constraints, fields, and validation  
**Tier**: Domain-Specific (Tier 2)  
**Use**: Build workflows for asset types, trading process, state transitions

**Depends on**: Object Resolver, Reference Tracer

---

## Input Format

```
Workflow Name: [string]
Asset Type: [Bond | Equity | Loan | ABS | CDS | FX | Repo | TRS | Warrant | Option]
Process: [Order Entry | Trade Execution | Settlement | Reconciliation]
Fields: [list of field names to capture]
Constraints: [optional business rules]
Transitions: [optional: state machine definition]
```

## Examples

```
Name: "Bond Private Placement"
Asset Type: Bond
Process: Trade Execution
Fields: CollateralRate, SettleDate, YieldRate
Constraints: SettleDate > TradeDate, Yield > 2%

Name: "Equity Option Exercise"
Asset Type: Option
Process: Order Entry
Fields: StrikePrice, ExerciseDate, Shares
Constraints: ExerciseDate <= Expiration
```

---

## Workflow Design Process

### Step 1: Select Asset Type

Map to Allvue AssetType:
```
Asset Type Mapping:
├─ Bond → BackOfficeSystemID: WSO, ExternalID: 2000
├─ Equity → BackOfficeExternalID: 2001
├─ Loan → BackOfficeExternalID: 2002
├─ ABS → BackOfficeExternalID: 2010
├─ CDS → BackOfficeExternalID: 2011
├─ Option → BackOfficeExternalID: 2012
├─ FX → BackOfficeExternalID: 2013
├─ Repo → BackOfficeExternalID: 2014
├─ TRS → BackOfficeExternalID: 2015
└─ Warrant → BackOfficeExternalID: 2016
```

**Output from Object Resolver**:
- AssetType CodeName and ID
- Existing workflows for this asset type
- Standard field set for this asset

### Step 2: Define Data Properties

For each field, determine:

```
Field Mapping:

Trade Object Fields (Trade table):
├─ TradeQuantity (decimal)
├─ SettleDate (datetime)
├─ TradeDate (datetime)
├─ Factor (decimal)
├─ CollateralRate (decimal)
├─ YieldRate (decimal)
└─ ... [40+ standard fields]

Trade Custom Fields (TradeCustom table):
├─ Date1-Date8 (datetime)
├─ Integer1-Integer8 (int)
├─ Money1-Money8 (money)
├─ Percent1-Percent8 (decimal)
├─ List1-List8 (ListItemID)
└─ Text1-Text16 (nvarchar)
```

Create WorkflowDataPropertyUsage for each field:

```xml
<WorkflowDataPropertyUsage>
  <DataObject>Trade (or TradeCustom)</DataObject>
  <DataProperty>CollateralRate</DataProperty>
  <DisplayMask>p3</DisplayMask> <!-- 3 decimal places -->
  <EditMask>p3</EditMask>
  <IsRequired>True</IsRequired>
  <IsCalculated>False</IsCalculated>
  <XPathExpression></XPathExpression>
</WorkflowDataPropertyUsage>
```

### Step 3: Define Workflow Steps

Create WorkflowStep hierarchy:

```
Workflow: Bond Trading
├─ Step 1: Order Entry
│  ├─ Fields: Quantity, SettleDate, Factor, ReferencePrice
│  ├─ Required: All 4 fields
│  ├─ Auto-Transition: If AllFieldsComplete then Step2
│  └─ Validation: SettleDate > TradeDate
│
├─ Step 2: Verification
│  ├─ Fields: [ReadOnly] Quantity, Factor
│  ├─ Action: Manual approval required
│  ├─ Transitions:
│  │  ├─ Approved → Step 3: Allocation
│  │  └─ Rejected → Step 1: Order Entry (to revise)
│  └─ Auto-Transition: After approval
│
├─ Step 3: Allocation
│  ├─ Auto-calculates: Allocation per portfolio
│  ├─ Action: Uses AllocationMethodology
│  ├─ Auto-Transition: When allocation complete
│  └─ Validates: Total allocation = Quantity
│
└─ Step 4: Settlement
   ├─ Sets: SettledQuantity, SettledDate
   ├─ Completes workflow
   └─ Auto-archival
```

### Step 4: Define Constraints & Validation

Create validation rules (WorkflowStepValidateOnSaveRule):

```
Validation Rules:

1. Date Validation
   Rule: SettleDate > TradeDate
   Message: "Settlement date must be after trade date"
   XPath: bms:compare(settle-date, ">", trade-date)

2. Quantity Validation
   Rule: Quantity > 0
   Message: "Quantity must be positive"
   XPath: /Trade/TradeQuantity > 0

3. Rate Validation
   Rule: YieldRate >= 2%
   Message: "Yield must be at least 2%"
   XPath: /Trade/YieldRate >= 2

4. Dependent Field Validation
   Rule: If Option then ExerciseDate must be filled
   Message: "Exercise date required for options"
   XPath: if(asset-type='Option', exists(exercise-date), true())

5. Business Logic
   Rule: Collateral Factor <= 1.0
   XPath: /Trade/CollateralRate <= 1.0
```

### Step 5: Configure State Transitions

Define WorkflowStepTransition:

```
Transitions:

Manual Transitions (RoleBasePanel determines who can perform):
├─ Order Entry → Verification (Analyst role required)
├─ Verification → Order Entry (Portfolio Manager can reject)
└─ Settlement → Complete (Operations)

Auto Transitions (WorkflowStepAutoTransition):
├─ Order Entry → Verification (when AllFieldsPopulated)
├─ Verification → Allocation (when Approved)
└─ Allocation → Settlement (when AllocationComplete)

Conditional Transitions (using XPath):
├─ If Quantity > 100M then require Senior Approval
├─ If Asset is CDS then go to RiskReview before Settlement
└─ If ExternalCounterparty then add Compliance review
```

### Step 6: Bind to Trade Transaction Types

Connect to TradeTransactionType:

```
Workflow → TradeTransactionType mapping:

For "Purchase" transactions:
├─ Create TradeTransaction (Trade record created)
├─ Execute workflow steps
├─ Update Allocation records
└─ Complete: Settle position

For "Sale" transactions:
├─ Verify existing position
├─ Create TradeTransaction
├─ Execute workflow steps
└─ Complete: Reduce position

For "Cover" transactions:
├─ Match to original short
├─ Create offsetting trade
├─ Execute workflow steps
└─ Complete: Close position
```

### Step 7: Set Role-Based Access

Create RoleBasePanel for each step:

```
Workflow Step Access:

Order Entry Step:
├─ Analyst: CanEdit=True, CanView=True
├─ Trader: CanEdit=True, CanView=True
├─ Portfolio Manager: CanView=True, CanEdit=False
└─ Operations: CanView=True, CanEdit=False

Verification Step:
├─ Analyst: CanEdit=False, CanView=True
├─ Portfolio Manager: CanEdit=True, CanView=True
└─ Operations: CanView=False

Settlement Step:
├─ Portfolio Manager: CanView=True
└─ Operations: CanEdit=True, CanView=True
```

### Step 8: Generate XML Configuration

Create complete Workflow.xml:

```xml
<DataImportRequest Type="BMS.LTD.Domain.Workflow.Workflow">
  <DataObjectImports>
    <DataObjectImport Type="BMS.LTD.Domain.Workflow.Workflow">
      <DataProperties>
        <DataProperty Name="CodeName">
          <SimpleDataProperty Value="Bond_Private_Placement" />
        </DataProperty>
        <DataProperty Name="Name">
          <SimpleDataProperty Value="Bond Private Placement" />
        </DataProperty>
        <DataProperty Name="AssetTypeID">
          <DataObjectDataProperty Type="BMS.LTD.Domain.Asset.AssetType">
            <Lookup>
              <DataProperties>
                <DataProperty name="CodeName" value="Bond" />
              </DataProperties>
            </Lookup>
          </DataObjectDataProperty>
        </DataProperty>
        <DataProperty Name="WorkflowTypeID">
          <SimpleDataProperty Value="1" />
        </DataProperty>
        <DataProperty Name="IsDeleted">
          <SimpleDataProperty Value="False" />
        </DataProperty>
      </DataProperties>
      <ComplexLookup Type="BMS.LTD.Domain.Workflow.Workflow" 
        value="SELECT w.ID FROM Workflow.Workflow AS w 
               JOIN Asset.AssetType AS a ON a.ID = w.AssetTypeID 
               WHERE w.CodeName = 'Bond_Private_Placement' AND a.CodeName = 'Bond'" />
    </DataObjectImport>
  </DataObjectImports>
</DataImportRequest>
```

---

## Output Format

```markdown
# Workflow Design: {WorkflowName}

## Configuration Summary
- **Name**: {WorkflowName}
- **Asset Type**: {AssetType} (ID: {ID})
- **Process**: {ProcessType}
- **Status**: Draft / Ready for Import
- **File**: Workflow_{CodeName}.xml

## Data Properties ({N} fields)

| Field | Type | Object | Source | Required | Validation |
|-------|------|--------|--------|----------|-----------|
| {Field1} | decimal | Trade | TradeQuantity | Yes | > 0 |
| {Field2} | datetime | Trade | SettleDate | Yes | > TradeDate |
| {Field3} | decimal | Trade | Factor | No | <= 1.0 |
| {Field4} | nvarchar | TradeCustom | Text1 | Yes | Ref Price |

## Workflow Steps

### Step 1: Order Entry
- **Fields**: Quantity, SettleDate, Factor, ReferencePrice
- **Required**: All
- **Role Access**: Analyst (Edit), Trader (Edit), PM (View)
- **Validations**: 
  - SettleDate > TradeDate
  - Quantity > 0
- **Auto-Transition**: When all fields filled
- **Next Step**: Verification

### Step 2: Verification
- **Fields**: [ReadOnly display of Order Entry]
- **Role Access**: Portfolio Manager (Edit), Analyst (View)
- **Actions**: 
  - Approve → Allocation
  - Reject → Order Entry
- **Validation**: Compliance checks

### Step 3: Allocation
- **Auto-calculated**: Allocation split
- **Methodology**: {AllocationMethodology}
- **Validation**: Sum(Allocations) = Quantity
- **Auto-Transition**: When complete
- **Next Step**: Settlement

### Step 4: Settlement
- **Fields**: SettledQuantity, SettledDate
- **Role Access**: Operations (Edit)
- **Validation**: All positions settled
- **Completion**: Archives trade

## Validation Rules ({N} rules)

1. **Date Validation**: SettleDate > TradeDate
2. **Quantity Validation**: Quantity > 0
3. **Rate Validation**: YieldRate >= 2%
4. **Dependent Validation**: If Option then ExerciseDate required
5. **Business Logic**: CollateralRate <= 1.0

## State Transitions

### Manual Transitions
- Order Entry → Verification (Analyst)
- Verification → Order Entry (PM can reject)

### Auto Transitions
- Order Entry → Verification (when AllFieldsPopulated)
- Verification → Allocation (when Approved)
- Allocation → Settlement (when Complete)

### Conditional Transitions
- If Quantity > 100M then Senior Approval required
- If CDS then add RiskReview step

## Cross-Reference

**Uses Allvue Objects**:
- AssetType: Bond
- AllocationMethodology: {MethodologyName}
- TradeTransactionType: Purchase, Sale, Cover
- Role: Analyst, Portfolio Manager, Operations

**Referenced By**:
- DataPanel: {PanelName}
- Report: {ReportName}
- Automated Job: {JobName}

## Implementation Steps

1. [ ] Create AssetType record (if needed)
2. [ ] Design WorkflowDataPropertyUsage (fields to capture)
3. [ ] Define WorkflowStep hierarchy (states)
4. [ ] Add validation rules (XPath expressions)
5. [ ] Configure state transitions (manual/auto)
6. [ ] Set role-based access (RoleBasePanel)
7. [ ] Generate XML configuration
8. [ ] Test in development environment
9. [ ] Deploy to production
10. [ ] Train users on workflow steps

## Deployment Checklist

- [ ] XML validation passes
- [ ] All referenced objects exist
- [ ] Role permissions configured
- [ ] Test workflow end-to-end
- [ ] Test each transition path
- [ ] Validate all field constraints
- [ ] Verify allocation calculations
- [ ] Test error conditions
- [ ] User documentation complete
- [ ] Training sessions scheduled

## Related Workflows

**Similar Asset Types**:
- {SimilarWorkflow1}
- {SimilarWorkflow2}

**Template Used**:
- Standard Bond Processing (template)

**Parent Process**:
- Trade Order Management

---

This skill answers: **"How do I build a workflow for {AssetType}?"**
