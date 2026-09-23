# Allvue Reference Tracer Skill

**Purpose**: Trace impact of changes on downstream objects  
**Tier**: Foundation (Tier 1)  
**Use**: "If I change X, what breaks?" Impact analysis for modifications

---

## Input Format

```
Starting Object: {ObjectName or CodeName}
Operation: [create | modify | delete]
Change Details: [optional: what specifically is changing]
```

## Examples

```
Portfolio: "AllVue ClearPar Fund 1" | Operation: modify (add sub-portfolio)
Workflow: "Bond" | Operation: modify (add new field)
AllocationMethodology: "Available_Capital" | Operation: delete
ComplianceScenario: "Sector Concentration" | Operation: modify (change limit)
DataSource: "AA_tfnAllocationReport" | Operation: modify (add parameter)
```

---

## Impact Analysis Process

### Step 1: Identify Starting Object
Use Object Resolver to get complete object context:
- Type, CodeName, file location
- All direct references
- All object that reference this

### Step 2: Classify Change Type

**CREATE**
- New object needs to exist
- Check: Do references exist? Are they complete?
- Find: Who would reference this (what listens for new objects)?

**MODIFY**
- Changing properties, references, or configuration
- Check: What depends on the current values?
- Find: Child/related objects affected
- Check: SQL queries that join to this

**DELETE**
- Removing the object
- Check: What references this (must be cleaned up)?
- Find: All downstream objects that become invalid
- Identify: Orphaned child objects

### Step 3: Build Impact Graph

For CREATE:
```
New Object
├─ Required References (must exist):
│  ├─ Parent Object: {Parent}
│  ├─ Related Objects: {Related1}, {Related2}
│  └─ Security: Requires Role assignment
└─ Potential Listeners:
   ├─ DataPanel: References via DataSource
   ├─ Workflow: References via AssetType
   └─ Reports: References via DataSource
```

For MODIFY:
```
Modified Object: {Name}
├─ Direct Impact:
│  ├─ Child Objects: {Child1} (recalculation needed), {Child2}
│  ├─ Joined SQL: {N} queries affected
│  └─ Reports: {Report1}, {Report2} (results change)
├─ Indirect Impact (1 hop):
│  ├─ Objects referencing this: {Ref1}, {Ref2}, {Ref3}
│  └─ Their downstream: {Indirect1}, {Indirect2}
├─ Secondary Impact (2+ hops):
│  └─ Chain: {Object1} → {Object2} → {FinalObject}
└─ UI Impact:
   └─ Dashboards affected: {Dashboard1}, {Dashboard2}
```

For DELETE:
```
Object to Delete: {Name}
├─ Must be removed from:
│  ├─ Direct References: {RefObject1}, {RefObject2}
│  ├─ SQL Foreign Keys: {N} tables
│  ├─ Collections: {Collection1}, {Collection2}
│  └─ Role Assignments: {RoleReference1}
├─ Child Objects:
│  ├─ Cascade Delete: {Child1}, {Child2}
│  ├─ Become Orphaned: {Orphan1}
│  └─ Require Re-assignment: {Reassign1}
├─ Downstream:
│  ├─ Reports Broken: {Report1} (DataSource missing)
│  ├─ Workflows Broken: {Workflow1} (AssetType missing)
│  └─ DataPanels Broken: {Panel1} (DataSource missing)
└─ Cleanup Required:
   ├─ DELETE FROM [Trade].[AllocationMethodology] WHERE ID={ID}
   ├─ UPDATE [Trade].[Trade] SET AllocationMethodologyID=NULL
   └─ DELETE FROM [Security].[RoleBasePanel] WHERE...
```

### Step 4: SQL Impact Analysis

For each affected table:
- Show foreign key constraints that would be violated
- Identify CASCADE DELETE rules
- List stored procedures that reference this
- Show trigger implications

Example:
```
DELETE [Trade].[AllocationMethodology] WHERE CodeName='Available_Capital'

Would violate FK in:
- [Trade].[Allocation].AllocationMethodologyID
  → 15,342 rows in [Trade].[Allocation] reference this
  
Solutions:
1. SET AllocationMethodologyID=NULL (leaves orphans)
2. DELETE dependent [Trade].[Allocation] rows first
3. Re-assign allocations to different methodology
```

### Step 5: Cross-Client Impact

Check: How many clients affected?
```
Affected Clients:
- Apax (10 objects reference this)
- BDT-MSD (25 objects reference this)
- TWGGlobal (8 objects reference this)
- Searchlight (NOT AFFECTED - lite deployment)

Total Impact: 43 objects across 3 clients
```

### Step 6: Risk Assessment

```
Risk Level: [LOW | MEDIUM | HIGH | CRITICAL]

Risk Factors:
- Depth: {depth} levels of dependencies
- Breadth: {breadth} objects affected
- Automation: {automation_count} automated workflows depend on this
- Reports: {report_count} reports depend on this
- Data Volume: {volume} SQL rows reference this

Mitigation:
- Backup strategy
- Testing scope
- Rollback plan
- Client notification (if multi-tenant)
```

---

## Output Format

```markdown
# Impact Analysis: {ObjectName}

## Change Summary
- **Object**: {ObjectName} ({Type})
- **Operation**: {CREATE | MODIFY | DELETE}
- **Scope**: {ChangeDetails}

## Direct Impact ({N} objects)
1. {ImpactedObject1}
   - Type: {Type}
   - Impact Type: {FieldValueChange | ReferenceChange | ChildDelete}
   - Recovery Required: Yes/No
   - Severity: {CRITICAL | HIGH | MEDIUM | LOW}

2. {ImpactedObject2}
   - ...

## SQL Impact ({N} tables)

### Affected Foreign Keys
- [{Schema}].[{Table}].{ForeignKeyColumn} → {N} rows
- [{Schema}].[{Table2}].{ForeignKeyColumn2} → {N} rows

### Required Updates
\`\`\`sql
-- Option 1: Set to NULL (leaves orphans)
UPDATE [{Schema}].[{Table}] 
SET {ForeignKeyColumn} = NULL 
WHERE {ForeignKeyColumn} = {ObjectID};

-- Option 2: Cascade delete
DELETE FROM [{Schema}].[{Table}] 
WHERE {ForeignKeyColumn} = {ObjectID};

-- Option 3: Re-assign
UPDATE [{Schema}].[{Table}] 
SET {ForeignKeyColumn} = {NewObjectID} 
WHERE {ForeignKeyColumn} = {ObjectID};
\`\`\`

## Cascade Analysis

**Level 1 (Direct)**:
- {DirectObject1}, {DirectObject2}, {DirectObject3}

**Level 2 (One hop)**:
- {IndirectObject1}, {IndirectObject2}

**Level 3+ (Multiple hops)**:
- {DeepObject1}

**Maximum Depth**: {depth} hops to root cause

## Cross-Client Impact
- **Apax**: {count} objects affected
- **BDT-MSD**: {count} objects affected
- **TWGGlobal**: {count} objects affected
- **Searchlight**: {count} objects affected
- **Total**: {total} objects across {client_count} clients

## Risk Assessment
**Overall Risk**: {CRITICAL | HIGH | MEDIUM | LOW}

### Risk Factors
- Depth of dependency tree: {depth}
- Number of downstream dependencies: {count}
- Automated workflows affected: {count}
- Reports affected: {count}
- User-facing impact: {yes/no}

### Critical Path
```
{StartingObject}
  → {CriticalObject1} [HIGH IMPACT]
  → {CriticalObject2} [REPORTS BREAK]
  → {CriticalObject3} [AUTOMATED WORKFLOWS FAIL]
```

## Recommendations

### Immediate Actions
1. [Action 1]
2. [Action 2]
3. [Action 3]

### Testing Scope
- [ ] Unit test for {Object1}
- [ ] Integration test for {Object2}
- [ ] UAT for reports: {Report1}, {Report2}
- [ ] Workflow test for: {Workflow1}
- [ ] Cross-client validation

### Rollback Plan
- Backup before: {PrepareStatement}
- Rollback SQL: {RollbackSQL}
- Verify: {VerificationQuery}

### Communication
- [ ] Notify users using {Report1}, {Report2}
- [ ] Schedule downtime (if required)
- [ ] Update documentation

## Change Log Entry
```
BEFORE:
{CurrentConfiguration}

AFTER:
{ProposedConfiguration}

IMPACT:
{ImpactSummary}
```
```

---

## Implementation Algorithm

```
1. INPUT: starting_object, operation, change_details
2. resolved = ObjectResolver(starting_object)  // Get full context
3. 
4. IF operation == "CREATE":
5.   referenced_by = find_all_objects_that_reference_type(resolved.type)
6.   missing = find_required_references(resolved)
7.   output: "Would create {resolved.name}, listeners: {referenced_by}, missing: {missing}"
8. 
9. ELSE IF operation == "MODIFY":
10.   children = find_child_objects(resolved)
11.   dependents = find_all_objects_referencing(resolved)
12.   sql_impact = find_affected_sql_queries(resolved)
13.   depth = calculate_dependency_depth(dependents)
14.   output: impact_graph(children, dependents, sql_impact, depth)
15. 
16. ELSE IF operation == "DELETE":
17.   cascade = find_cascade_delete_targets(resolved)
18.   orphans = find_orphaned_objects(resolved)
19.   cleanup = generate_cleanup_sql(resolved, cascade, orphans)
20.   output: cleanup_instructions(cleanup, cascade, orphans)
21. 
22. RETURN: risk_assessment + impact_matrix + recommendations
```

---

## Key Insights

- **Depth matters**: 3-hop dependencies are usually safe, 5+ hops get risky
- **SQL cascades**: Check for CASCADE DELETE rules before deleting
- **Circular dependencies**: Rare but critical (e.g., Asset.Asset → Asset.Asset parent)
- **Role assignments**: RoleBasePanel references are often overlooked
- **Cross-client**: Multi-tenant deployments need per-client impact analysis
- **Test order**: Always test upstream dependencies before downstream

This skill answers: **"What happens if I change X?"**
