# Allvue Configuration Cloner Skill

**Purpose**: Clone existing object configurations with adjusted references  
**Tier**: Integration (Tier 3)  
**Use**: Duplicate configurations for new portfolios, asset types, or clients

**Depends on**: Object Resolver, Reference Tracer, DataSource Decoder

---

## Input Format

```
Source Object: {ObjectName/CodeName}
Clone Type: [Portfolio | AssetType | Workflow | Compliance | Report | All]
Target Name: {NewObjectName}
Adjustments: [optional: field mappings, reference updates]
Client: [Apax | BDT-MSD | TWGGlobal | Searchlight]
```

## Examples

```
Source: "AllVue ClearPar Fund 1" | Clone: Portfolio
Target Name: "AllVue ClearPar Fund 2"
Adjustments: Currency=EUR, Inception=2026-09-15

Source: "Bond" | Clone: Workflow
Target Name: "Corporate Bond"
Adjustments: AssetType=Corporate_Bond, TradeTransactionType=Purchase_Only

Source: "Daily Allocation Report" | Clone: Report
Target Name: "Weekly Allocation Summary"
Adjustments: DateFilter=Weekly, Export=PDF, Recipients=updated
```

---

## Configuration Cloning Process

### Step 1: Identify Source Object

Use Object Resolver to load complete configuration:

```
Source Object: "AllVue ClearPar Fund 1" (Portfolio)
├─ Type: BMS.LTD.Domain.Portfolio.Portfolio
├─ File: Portfolio_AllVue ClearPar Fund 1.xml
├─ Current Properties:
│  ├─ Name: AllVue ClearPar Fund 1
│  ├─ AbbrevName: ClearPar1
│  ├─ CurrencyType: USD
│  ├─ InceptionDate: 2025-01-01
│  ├─ ClientID: 1
│  └─ IsPortfolioGroup: False
│
├─ Child Objects:
│  ├─ SubPortfolio (2 records)
│  ├─ PortfolioCustom
│  └─ PortfolioComplianceSetting
│
└─ References:
   ├─ CurrencyType.USD
   ├─ Client.AlphaAlternatives
   └─ (Other portfolio FKs)
```

### Step 2: Classify Clone Scope

Determine what to clone:

```
Scope: Full Clone (Portfolio + Children)

Objects to Clone:
├─ Parent: Portfolio (primary)
│  └─ New CodeName: "AllVue_ClearPar_Fund_2"
│
├─ Children: SubPortfolio (2 records)
│  ├─ SubPortfolio 1 → "ClearPar2-ClassA"
│  └─ SubPortfolio 2 → "ClearPar2-ClassB"
│
├─ Extensions: PortfolioCustom
│  └─ Clone with same custom field values
│
├─ Settings: PortfolioComplianceSetting
│  └─ Clone all compliance rules to new portfolio
│
└─ NOT Cloning (reference to parent only):
   └─ CurrencyType, Client (remain same)
```

### Step 3: Build Clone Map

Create mapping between source and target:

```
Clone Mapping: Portfolio_AllVue_ClearPar_Fund_2

Source → Target Mapping:

Object Type | Source Name | Target Name | New CodeName | Adjustments |
---|---|---|---|---|
Portfolio | AllVue ClearPar Fund 1 | AllVue ClearPar Fund 2 | AllVue_ClearPar_Fund_2 | Inception: 2026-09-15 |
SubPortfolio | ClearPar1-ClassA | ClearPar2-ClassA | ClearPar2_ClassA | [same as parent] |
SubPortfolio | ClearPar1-ClassB | ClearPar2-ClassB | ClearPar2_ClassB | [same as parent] |
PortfolioCustom | ClearPar1_Custom | ClearPar2_Custom | ClearPar2_Custom | [copy all fields] |
ComplianceSetting | ClearPar1_Compliance | ClearPar2_Compliance | ClearPar2_Compliance | [copy all rules] |

Reference Adjustments:
- Portfolio.ClientID: 1 → 1 (same)
- SubPortfolio.PortfolioID: {Portfolio1.ID} → {Portfolio2.ID} (new FK)
```

### Step 4: Extract Source XML

Read source configuration files:

```
Files to Extract:

1. C:\repo\Clients\BDT-MSD\App Exports\Portfolio\Portfolio_AllVue ClearPar Fund 1.xml
   └─ Extract all <DataProperty> elements

2. C:\repo\Clients\BDT-MSD\App Exports\SubPortfolio\SubPortfolio_ClearPar1-ClassA.xml
   └─ Extract and mark for re-keying

3. C:\repo\Clients\BDT-MSD\App Exports\PortfolioCustom\PortfolioCustom_ClearPar1.xml
   └─ Extract custom field values

4. ... [other related files]
```

### Step 5: Transform Configuration

Adjust all references and identifiers:

```
Transformation Rules:

1. CodeName Transformation
   OLD: CodeName = "AllVue_ClearPar_Fund_1"
   NEW: CodeName = "AllVue_ClearPar_Fund_2"

2. Name Transformation
   OLD: Name = "AllVue ClearPar Fund 1"
   NEW: Name = "AllVue ClearPar Fund 2"

3. Display Abbreviation
   OLD: AbbrevName = "ClearPar1"
   NEW: AbbrevName = "ClearPar2"

4. Custom Field Values (if needed)
   OLD: Date1 = "2025-01-01"
   NEW: Date1 = "2026-09-15" (from adjustments)

5. Foreign Key References
   OLD: CurrencyID = 1 (USD)
   NEW: CurrencyID = 1 (unchanged - same currency)

6. Child Object References
   OLD: SubPortfolio.PortfolioID = {Portfolio1.ID}
   NEW: SubPortfolio.PortfolioID = {Portfolio2.ID} (to be created)

7. Lookup References
   OLD: <DataProperty name="CodeName" value="USD" />
   NEW: <DataProperty name="CodeName" value="USD" /> (unchanged)

8. Deletion Status
   OLD: IsDeleted = True/False
   NEW: IsDeleted = False (reset for new object)
```

### Step 6: Generate Target XML

Create new XML files with transformed values:

```xml
<!-- NEW FILE: Portfolio_AllVue ClearPar Fund 2.xml -->
<DataImportRequest Type="BMS.LTD.Domain.Portfolio.Portfolio">
  <DataObjectImports>
    <DataObjectImport Type="BMS.LTD.Domain.Portfolio.Portfolio">
      <DataProperties>
        <DataProperty Name="CodeName">
          <SimpleDataProperty Value="AllVue_ClearPar_Fund_2" /> <!-- CHANGED -->
        </DataProperty>
        <DataProperty Name="Name">
          <SimpleDataProperty Value="AllVue ClearPar Fund 2" /> <!-- CHANGED -->
        </DataProperty>
        <DataProperty Name="AbbrevName">
          <SimpleDataProperty Value="ClearPar2" /> <!-- CHANGED -->
        </DataProperty>
        <DataProperty Name="InceptionDate">
          <SimpleDataProperty Value="2026-09-15" /> <!-- CHANGED from adjustments -->
        </DataProperty>
        <DataProperty Name="CurrencyType" ReferenceType="ObjectMemberName">
          <DataObjectDataProperty Type="BMS.LTD.Domain.Reference.CurrencyType">
            <Lookup>
              <DataProperties>
                <DataProperty name="CodeName" value="USD" /> <!-- UNCHANGED -->
              </DataProperties>
            </Lookup>
          </DataObjectDataProperty>
        </DataProperty>
        <!-- ... other properties copied from source ... -->
      </DataProperties>
      <ComplexLookup Type="BMS.LTD.Domain.Portfolio.Portfolio" 
        value="SELECT p.ID FROM Portfolio.Portfolio AS p 
               WHERE p.CodeName = 'AllVue_ClearPar_Fund_2'" /> <!-- CHANGED -->
    </DataObjectImport>
  </DataObjectImports>
</DataImportRequest>
```

### Step 7: Handle Dependencies

Create child objects with proper references:

```
Child Object Creation Order:

1. Portfolio (parent)
   └─ Wait for: ID generation from database

2. SubPortfolio (2 children)
   ├─ FK to: Portfolio (newly created)
   └─ CodeName: ClearPar2_ClassA, ClearPar2_ClassB

3. PortfolioCustom (extension)
   ├─ FK to: Portfolio (newly created)
   └─ Copy all custom field values

4. PortfolioComplianceSetting
   ├─ FK to: Portfolio (newly created)
   └─ Copy all compliance rules

5. Related Objects (optional)
   ├─ CashAccount (if exists)
   └─ PortfolioGroupMembership (if exists)
```

### Step 8: Validate Cloned Configuration

Verify all references are correct:

```
Validation Checks:

✓ All CodeNames are unique (not duplicated)
✓ All foreign keys point to valid objects
✓ All child objects reference new parent
✓ No deleted objects are included (IsDeleted != True)
✓ All required fields are populated
✓ Lookup references resolve correctly
✓ ComplexLookup SQL uses new CodeNames
✓ Custom field values are valid
✓ No circular references
✓ Role/security settings copied
✓ Dates are valid (InceptionDate <= Today)
✓ Currency/client references intact
```

### Step 9: Generate Deployment Package

Create XML import package:

```
CLONE_PACKAGE: AllVue_ClearPar_Fund_2_YYYYMMDD.zip
├─ Portfolio_AllVue ClearPar Fund 2.xml
├─ SubPortfolio_ClearPar2-ClassA.xml
├─ SubPortfolio_ClearPar2-ClassB.xml
├─ PortfolioCustom_ClearPar2.xml
├─ PortfolioComplianceSetting_ClearPar2.xml
├─ CLONE_MANIFEST.json (metadata)
│  ├─ Source Portfolio: AllVue ClearPar Fund 1
│  ├─ Target Portfolio: AllVue ClearPar Fund 2
│  ├─ Objects Cloned: 5 (Portfolio + 4 children)
│  ├─ References Updated: 12
│  ├─ Adjustments Applied: 2 (Inception Date, Abbrev)
│  ├─ Created By: {User}
│  ├─ Created Date: {Date}
│  └─ Client: BDT-MSD
│
└─ IMPORT_INSTRUCTIONS.txt
   ├─ Step 1: Backup current database
   ├─ Step 2: Run Portfolio_AllVue ClearPar Fund 2.xml
   ├─ Step 3: Run SubPortfolio_*.xml files
   ├─ Step 4: Run PortfolioCustom_*.xml
   ├─ Step 5: Run PortfolioComplianceSetting_*.xml
   ├─ Step 6: Verify clone in UI
   └─ Step 7: Run validation queries
```

### Step 10: Create Validation & Rollback Scripts

Generate SQL for verification:

```sql
-- VALIDATION QUERIES

-- 1. Verify clone exists
SELECT ID, CodeName, Name FROM Portfolio.Portfolio 
WHERE CodeName = 'AllVue_ClearPar_Fund_2';

-- 2. Verify children created
SELECT ID, CodeName, PortfolioID FROM Portfolio.SubPortfolio 
WHERE CodeName LIKE 'ClearPar2%';

-- 3. Check custom field values
SELECT PortfolioID, Date1, Integer1, Money1 
FROM Portfolio.PortfolioCustom 
WHERE PortfolioID = (SELECT ID FROM Portfolio.Portfolio WHERE CodeName='AllVue_ClearPar_Fund_2');

-- 4. Verify compliance settings
SELECT PortfolioID, TestID, LimitValue 
FROM Compliance.PortfolioComplianceSetting 
WHERE PortfolioID = (SELECT ID FROM Portfolio.Portfolio WHERE CodeName='AllVue_ClearPar_Fund_2');

-- ROLLBACK SCRIPT (if needed)
DELETE FROM Portfolio.PortfolioComplianceSetting 
WHERE PortfolioID = (SELECT ID FROM Portfolio.Portfolio WHERE CodeName='AllVue_ClearPar_Fund_2');

DELETE FROM Portfolio.PortfolioCustom 
WHERE PortfolioID = (SELECT ID FROM Portfolio.Portfolio WHERE CodeName='AllVue_ClearPar_Fund_2');

DELETE FROM Portfolio.SubPortfolio 
WHERE PortfolioID = (SELECT ID FROM Portfolio.Portfolio WHERE CodeName='AllVue_ClearPar_Fund_2');

DELETE FROM Portfolio.Portfolio 
WHERE CodeName='AllVue_ClearPar_Fund_2';
```

---

## Output Format

```markdown
# Configuration Cloner: {SourceObjectName} → {TargetObjectName}

## Clone Definition
- **Source**: {SourceObjectName} ({Type})
- **Target**: {TargetObjectName}
- **Clone Type**: {Full | Partial}
- **Objects to Clone**: {N} objects
- **Package Date**: {Date}

## Clone Scope

**Primary Object**:
- Type: {ObjectType}
- Source CodeName: {SourceCodeName}
- Target CodeName: {TargetCodeName}
- New Name: {TargetName}

**Child Objects** ({N} objects):
1. {ChildType}: {SourceChildName} → {TargetChildName}
2. ...

**Referenced Objects** (NOT cloned, reused):
- CurrencyType: USD
- Client: Alpha Alternatives

## Transformation Map

| Object | Source CodeName | Target CodeName | Field Changes | References Updated |
|--------|-----------------|-----------------|----------------|-------------------|
| Portfolio | AllVue_ClearPar_Fund_1 | AllVue_ClearPar_Fund_2 | Inception, Abbrev | 0 (client refs) |
| SubPortfolio | ClearPar1_ClassA | ClearPar2_ClassA | [none] | 1 (parent) |
| SubPortfolio | ClearPar1_ClassB | ClearPar2_ClassB | [none] | 1 (parent) |
| PortfolioCustom | ClearPar1_Custom | ClearPar2_Custom | [none] | 1 (parent) |
| ComplianceSetting | ClearPar1_Comp | ClearPar2_Comp | [none] | 1 (parent) |

## Adjustments Applied

1. **Inception Date**: 2025-01-01 → 2026-09-15
2. **Abbreviation**: ClearPar1 → ClearPar2
3. **Currency**: USD (unchanged)
4. **Client**: Alpha Alternatives (unchanged)

## XML Files Generated

- [ ] Portfolio_AllVue ClearPar Fund 2.xml
- [ ] SubPortfolio_ClearPar2-ClassA.xml
- [ ] SubPortfolio_ClearPar2-ClassB.xml
- [ ] PortfolioCustom_ClearPar2.xml
- [ ] PortfolioComplianceSetting_ClearPar2.xml
- [ ] CLONE_MANIFEST.json
- [ ] IMPORT_INSTRUCTIONS.txt
- [ ] VALIDATION_QUERIES.sql
- [ ] ROLLBACK_SCRIPT.sql

## Import Sequence

1. Portfolio_AllVue ClearPar Fund 2.xml (creates parent, gets ID)
2. SubPortfolio_ClearPar2-ClassA.xml (references parent ID)
3. SubPortfolio_ClearPar2-ClassB.xml (references parent ID)
4. PortfolioCustom_ClearPar2.xml (references parent ID)
5. PortfolioComplianceSetting_ClearPar2.xml (references parent ID)

## Validation Checklist

- [ ] Clone unique CodeName not duplicated
- [ ] All foreign keys valid
- [ ] No deleted objects included
- [ ] Dates valid and in order
- [ ] Custom fields populated correctly
- [ ] Compliance rules copied
- [ ] Role access configured
- [ ] Lookup references resolve

## Rollback Plan

If import fails:
1. Execute ROLLBACK_SCRIPT.sql
2. Verify all clone objects deleted
3. Re-run with corrected XML

## Deployment Notes

- Estimated import time: {Duration}
- Estimated disk space: {Size}
- Requires admin privileges: Yes
- Can run during business hours: No (recommend off-hours)
- Backup recommended before import: Yes

---

This skill answers: **"How do I duplicate an object configuration?"**
