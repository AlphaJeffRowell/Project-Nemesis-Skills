# Allvue Object Resolver Skill

**Purpose**: Resolve any Allvue object to its complete dependency chain  
**Tier**: Foundation (Tier 1)  
**Use**: Find what an object references and what references it

---

## Input Format

```
Object Name / CodeName: [string]
Scope: [optional: "references", "referenced_by", "full"]
Details: [optional: yes/no for detailed SQL]
```

## Examples

```
"AA Data Dictionary" [full, details=yes]
"Available_Capital_Pro_Rata" [references]
"Bond" [referenced_by]
"Portfolio.Portfolio" [full]
```

---

## Resolution Process

### Step 1: Object Identification
Search for object across all clients:
- Exact CodeName match
- Partial name match
- Type path if provided (BMS.LTD.Domain.*)
- File location in App Exports

### Step 2: Extract Direct References
From XML, identify:
- **Type references**: `Type="BMS.LTD.Domain.*"` elements
- **Lookup references**: `DataObjectDataProperty` with `Lookup` sub-elements
- **ComplexLookup SQL**: Extract SQL join logic
- **DataSource references**: DataSourceName attributes
- **Collections**: Child object references
- **Parameters**: @placeholder references

### Step 3: Resolve SQL
For each reference:
- SQL ComplexLookup → parse JOIN and WHERE clauses
- Table function names → resolve to Custom schema
- Foreign key columns → trace to referenced tables
- Parameter bindings → show @name substitutions

### Step 4: Build Dependency Graph
Structure as:

```
Object: {Name}
├─ Type: BMS.LTD.Domain.{Module}.{ObjectType}
├─ Direct References (5):
│  ├─ {RefObject1} (via {ReferenceType})
│  ├─ {RefObject2} (via SQL ComplexLookup)
│  └─ ...
├─ SQL Resolution:
│  ├─ Table Function: Custom.{FunctionName}
│  ├─ Parameters: [@param1: type, @param2: type]
│  ├─ SQL: {ComplexLookup query}
│  └─ Joins: {t1} JOIN {t2} ON {condition}
├─ Referenced By (3):
│  ├─ {Object3} (DataPanel references this via DataSource)
│  └─ ...
└─ Impact: Changing this affects {N} downstream objects
```

### Step 5: Cross-Client Validation
- Is this object in Apax? BDT-MSD? Searchlight? TWGGlobal?
- Is it universal or specialized?
- Show variations across clients if applicable

---

## Reference Mapping (Allvue Object → SQL)

| XML Object Type | SQL Schema | SQL Table | Resolution |
|-----------------|-----------|-----------|-----------|
| BMS.LTD.Domain.UI.DataPanel | UI | DataPanel | Direct mapping |
| BMS.LTD.Domain.Client.DataSource | Client | DataSource | Direct mapping |
| BMS.LTD.Domain.Trade.AllocationMethodology | Trade | AllocationMethodology | Direct mapping |
| BMS.LTD.Domain.Workflow.Workflow | Workflow | Workflow | Direct mapping |
| BMS.LTD.Domain.Portfolio.Portfolio | Portfolio | Portfolio | Direct mapping |
| BMS.LTD.Domain.Security.Role | Security | Role | Direct mapping |
| BMS.LTD.Domain.UI.Report | UI | Report | Direct mapping |
| BMS.LTD.Domain.Compliance.ComplianceScenario | Compliance | ComplianceScenario | Direct mapping |

---

## Output Format

```markdown
# Object Resolution: {ObjectName}

## Identification
- **Type**: BMS.LTD.Domain.{Module}.{ObjectType}
- **CodeName**: {CodeName}
- **Clients**: Apax, BDT-MSD, TWGGlobal [, Searchlight]
- **File Location**: C:\repo\Clients\BDT-MSD\App Exports\{Category}\{FileName}.xml

## Direct References ({N} found)
1. {ReferenceObject1}
   - Type: {ReferenceType}
   - Lookup Condition: {WHERE clause from SQL}
   - Join Pattern: {JOIN details}

2. {ReferenceObject2}
   - Type: {ReferenceType}
   - ...

## SQL Resolution
**Resolved Table Function**: Custom.{FunctionName}
**Parameters**: @parameter1 (type), @parameter2 (type)
**ComplexLookup SQL**:
\`\`\`sql
{Full SQL query extracted from XML}
\`\`\`

**Joins**: 
- Primary table: [{Schema}].[{TableName}]
- Join to: [{Schema}].[{ReferenceTable}]
- On condition: {join_condition}

**Return Fields**: 
- {FieldName1}: {type}
- {FieldName2}: {type}

## Referenced By ({N} objects)
1. {ReferencingObject1} (Type: {ObjectType})
2. {ReferencingObject2} (Type: {ObjectType})

## Impact Analysis
- **Critical**: Changing this object affects {N} downstream objects
- **Chain Depth**: Max {depth} hops to reach database
- **Circular Dependencies**: None / {list if any}

## Complete Dependency Chain
\`\`\`
{This Object}
  ├─ references: {Reference1}, {Reference2}
  ├─ references via SQL: {SQLJoin}
  └─ SQL tables: {Table1}, {Table2}, {Table3}
\`\`\`

## Related Objects
- Similar: {SimilarObject1}, {SimilarObject2}
- Child objects: {ChildObject1}, {ChildObject2}
- Parent object: {ParentObject}
```

---

## Implementation Notes

1. **XML Parsing**: Extract all Type attributes, Lookup elements, ComplexLookup values, DataSource references
2. **SQL Parsing**: Identify SELECT, FROM, JOIN, WHERE, GROUP BY patterns
3. **Cross-reference**: Check all 4 clients for this object
4. **Bidirectional**: Show both what it references AND what references it
5. **SQL Details**: If requested, include full SQL with parameter substitutions

---

## Quick Reference

**For any object named X:**
1. Find X in App Exports across all clients
2. Extract its Type path (BMS.LTD.Domain.*)
3. List all objects it directly references (XML Type attributes)
4. Parse SQL ComplexLookup to show SQL joins
5. Find all objects that reference X (reverse lookup)
6. Calculate impact (how many downstream objects affected)

This is the **foundational skill** — all other skills use this resolver as their engine.
