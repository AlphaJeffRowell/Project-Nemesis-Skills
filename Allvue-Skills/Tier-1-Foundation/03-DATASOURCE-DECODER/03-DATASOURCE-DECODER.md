# Allvue DataSource Decoder Skill

**Purpose**: Decode DataSource definitions to SQL and returned data structure  
**Tier**: Foundation (Tier 1)  
**Use**: Understand what data a DataPanel actually queries

---

## Input Format

```
DataSource Name / CodeName: [string]
Show: [optional: "signature", "sql", "joins", "fields", "full"]
Client: [optional: Apax | BDT-MSD | Searchlight | TWGGlobal]
```

## Examples

```
"AA_tfnDataDictionaryDataProperty" [full]
"AllocationReportDataSource" [sql]
"Calendar Master" [signature]
```

---

## Decoding Process

### Step 1: Locate DataSource File

Search in client App Exports:
```
C:\repo\Clients\{Client}\App Exports\DataSource\DataSource_{CodeName}.xml
```

Extract XML properties:
- CodeName
- Name
- Description (often has documentation link)
- ExternalID (database object name)
- Data integration type (table function, stored procedure, query)

### Step 2: Extract SQL Definition

From XML, find:
```xml
<DataProperty Name="ExternalID">
  <SimpleDataProperty Value="Custom.AA_tfnDataDictionaryDataProperty" />
</DataProperty>
```

This tells you:
- **Schema**: Custom
- **Object Name**: AA_tfnDataDictionaryDataProperty
- **Type**: Table Function (tfn = table-valued function)

### Step 3: Parse DataSourceParameter References

Extract parameters collection:
```
DataSourceParameter
├─ @DataObjectID (input, type: int)
├─ @StartDate (input, type: datetime)
├─ @EndDate (input, type: datetime)
└─ @PortfolioID (input, type: int)
```

For each parameter:
- Name (starts with @)
- Type (int, nvarchar, datetime, bit, etc.)
- Direction (input, output, return)
- Usage (UserInput, Derived, Fixed)

### Step 4: Resolve SQL Signature

Look up SQL definition to determine:

```
Function Signature:
CREATE FUNCTION Custom.AA_tfnDataDictionaryDataProperty (
    @Custom_AA_tfnDataDictionaryDataProperty_DataObjectID int
)
RETURNS TABLE AS RETURN (
    SELECT 
        DataPropertyID,
        DataPropertyName,
        DataObjectID,
        DataObjectName,
        DataObjectSchemaID,
        DataObjectSchemaName,
        DataObjectTypeID,
        DataObjectTypeName
    FROM [Dictionary].[DataProperty]
    WHERE DataObjectID = @Custom_AA_tfnDataDictionaryDataProperty_DataObjectID
)
```

### Step 5: Extract Return Fields

Parse SELECT clause:
| Field Name | Type | Source Table | Notes |
|-----------|------|-------------|-------|
| DataPropertyID | int | Dictionary.DataProperty | PK |
| DataPropertyName | nvarchar | Dictionary.DataProperty | |
| DataObjectID | int | Dictionary.DataProperty | FK |
| DataObjectName | nvarchar | Dictionary.DataObject | |
| DataObjectSchemaID | int | Dictionary.DataObject | FK |
| DataObjectSchemaName | nvarchar | Dictionary.DataObject | |
| DataObjectTypeID | int | Dictionary.DataObjectType | FK |
| DataObjectTypeName | nvarchar | Dictionary.DataObjectType | |

### Step 6: Trace SQL Joins

Parse FROM and JOIN clauses:

```
Base Table: [Dictionary].[DataProperty] AS p

JOINs:
├─ JOIN [Dictionary].[DataObject] AS o 
│   ON o.ID = p.DataObjectID
├─ JOIN [Dictionary].[DataObjectType] AS t 
│   ON t.ID = o.DataObjectTypeID
└─ LEFT JOIN [Dictionary].[DataObjectSchema] AS s 
    ON s.ID = o.DataObjectSchemaID
```

### Step 7: Understand WHERE Clauses

Extract filter logic:

```
WHERE p.DataObjectID = @Custom_AA_tfnDataDictionaryDataProperty_DataObjectID

Means:
- Filters to specific DataObject (passed via parameter)
- Parameter must be provided at runtime
- Returns only fields for that object
```

### Step 8: Document Usage Context

Find where this DataSource is used:

```
Used By:
├─ DataPanel: "AA Data Dictionary" (references via ComplexLookup)
├─ Report: "Data Property Reference" (direct DataSource binding)
├─ WebDashboard: "System Admin Dashboard" (widget uses DataPanel)
└─ CalendarPanel: "System Calendar" (for reference data)
```

---

## Output Format

```markdown
# DataSource Decoder: {DataSourceName}

## Identification
- **CodeName**: {CodeName}
- **Name**: {Name}
- **External ID**: {ExternalID} (SQL object name)
- **Type**: Table Function / Stored Procedure / Query
- **Clients**: {ClientList}
- **File**: C:\repo\Clients\{Client}\App Exports\DataSource\DataSource_{CodeName}.xml

## Description
[From DataSource Description field]

Link: [Documentation URL if present]

## Function Signature
\`\`\`sql
CREATE FUNCTION {Schema}.{FunctionName} (
    @parameter1 {type},
    @parameter2 {type},
    ...
)
RETURNS TABLE AS RETURN (
    SELECT ...
)
\`\`\`

## Parameters

| Parameter | Type | Direction | Usage | Description |
|-----------|------|-----------|-------|-------------|
| @param1 | int | input | UserInput | [Description] |
| @param2 | nvarchar | input | Derived | [Description] |
| @param3 | datetime | input | Fixed | [Description] |

**Required Parameters**: {count}
**Optional Parameters**: {count}
**Parameter Binding**: Manual / Automatic

## Return Fields ({N} fields)

| Field Name | Type | Nullable | Source | FK Reference |
|-----------|------|----------|--------|--------------|
| FieldName1 | int | No | Table1 | {Table2.ID} |
| FieldName2 | nvarchar(100) | Yes | Table1 | |
| FieldName3 | datetime | Yes | Table1 JOIN Table2 | |

**Total Fields**: {count}
**Primary Key**: {PKField}
**Indexed Fields**: {IndexedFields}

## SQL Query Structure

### Base Tables
- Primary: [{Schema}].[{TableName}]
- Cardinality: {N} rows typical

### JOINs ({N} joins)
1. INNER JOIN [{Schema}].[Table2] ON condition
2. LEFT JOIN [{Schema}].[Table3] ON condition

**Join Diagram**:
\`\`\`
[Dictionary].[DataProperty]
├─ INNER JOIN [Dictionary].[DataObject]
│  └─ INNER JOIN [Dictionary].[DataObjectType]
└─ LEFT JOIN [Dictionary].[DataObjectSchema]
\`\`\`

### WHERE Clause
\`\`\`sql
WHERE {FilterCondition}
\`\`\`

**Filters**:
- {FilterName1}: {FilterLogic}
- {FilterName2}: {FilterLogic}

### ORDER BY / GROUP BY
\`\`\`sql
ORDER BY {OrderColumn1}, {OrderColumn2}
GROUP BY {GroupColumn1}
\`\`\`

## Typical Execution
\`\`\`sql
SELECT * FROM {Schema}.{FunctionName}(
    @parameter1 = {ExampleValue1},
    @parameter2 = {ExampleValue2}
)

Expected Rows: {TypicalRowCount}
Expected Execution Time: {TimingEstimate}
\`\`\`

## Used By ({N} objects)

### DataPanels ({count})
- {DataPanel1}
- {DataPanel2}

### Reports ({count})
- {Report1}
- {Report2}

### WebDashboards ({count})
- {WebDashboard1}

### Other Objects ({count})
- {CalendarPanel1}
- {GlobalAction1}

## Related DataSources

**Similar functionality**:
- {RelatedDataSource1}
- {RelatedDataSource2}

**Prerequisite**:
- {PrerequisiteDataSource}

**Dependent**:
- {DependentDataSource}

## Performance Notes

- **Cardinality**: {LowMediumHigh} result set
- **Index Coverage**: {YesNo} - uses {IndexName}
- **Join Strategy**: {Strategy}
- **Typical Rows**: {RowCount}
- **Cache**: {YesNo} - refresh frequency: {Frequency}

## Parameter Behavior

### @parameter1: {Name}
- **Type**: int
- **Usage**: Filters to specific object
- **Constraints**: Must be valid ID from [Dictionary].[DataObject]
- **Default**: None (required)
- **Example**: 23 (Trade object)

### @parameter2: {Name}
- **Type**: datetime
- **Usage**: Start date filter
- **Constraints**: Must be before @parameter3
- **Default**: None (required)
- **Example**: 2026-01-01

## Code Example

### Usage in DataPanel
\`\`\`xml
<DataPanel>
  <DataSourceReference>
    <ComplexLookup value="SELECT dsp.ID FROM [Client].[DataSourceParameter] dsp 
      INNER JOIN [client].[DataSource] ds ON ds.ID = dsp.DataSourceID 
      WHERE dsp.[Name]='@DataObjectID' AND ds.CodeName='AA_tfnDataDictionaryDataProperty'"/>
  </DataSourceReference>
  <Parameters>
    <Parameter Name="@DataObjectID" Type="int" Value="23"/>
  </Parameters>
</DataPanel>
\`\`\`

### Usage in Reporting
\`\`\`sql
DECLARE @StartDate datetime = '2026-01-01'
DECLARE @EndDate datetime = '2026-01-31'

SELECT 
    ObjectName,
    COUNT(*) as PropertyCount,
    MAX(DataPropertyID) as MaxPropertyID
FROM Custom.AA_tfnDataDictionaryDataProperty(@DataObjectID = 23)
GROUP BY ObjectName
\`\`\`

## Troubleshooting

### Issue: Parameter Binding Error
**Solution**: Check parameter types and order in ComplexLookup

### Issue: No Data Returned
**Solution**: Verify filter parameters are valid IDs

### Issue: Performance Slow
**Solution**: Check index usage on join columns

## Cross-Client Variations

| Client | CodeName | Differences | Parameters |
|--------|----------|------------|-----------|
| Apax | {CodeName} | {Variant1} | Standard |
| BDT-MSD | {CodeName} | {Variant2} | Standard |
| Searchlight | {CodeName} | {Variant3} (simplified) | Subset |
| TWGGlobal | {CodeName} | {Variant4} | Extended |

## SQL DDL

\`\`\`sql
{Complete CREATE FUNCTION statement from database}
\`\`\`

---

This skill answers: **"What does this DataSource actually query?"**

Usage Pattern:
1. Find DataSource name (from DataPanel reference)
2. Decode to understand parameters
3. Understand return fields
4. Know which tables are queried
5. Calculate impact of schema changes
