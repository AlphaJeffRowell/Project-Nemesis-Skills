# Allvue XPath Navigator Skill

**Purpose**: Write and understand XPath expressions used in Allvue workflows, compliance, and validation  
**Tier**: Foundation+ (Tier 1.5 - specialized but universal)  
**Use**: Build workflow validation rules, compliance expressions, data filtering

---

## What is XPath in Allvue?

XPath expressions in Allvue are used to:
1. **Validate data** (e.g., "SettleDate must be > TradeDate")
2. **Calculate values** (e.g., "Factor if present, else 1.0")
3. **Filter data** (e.g., "Only include if Status = 'Active'")
4. **Transform data** (e.g., "Convert date format")

**Examples from real Allvue workflows:**
```xml
<!-- Allvue uses Allvue's custom XPath dialect with bms: namespace -->
<XPathExpression>bms:coalesce(/Trade/Factor, 1)</XPathExpression>
<XPathExpression>bms:bizDate(string(/Trade/TradeDate))</XPathExpression>
<XPathExpression>/Trade/TradeQuantity > 0</XPathExpression>
<XPathExpression>bms:compare(settle-date, ">", trade-date)</XPathExpression>
```

---

## Input Format

```
XPath Type: [Validation | Calculation | Filter | Transform]
Context: [Trade | Allocation | Portfolio | Compliance | Custom]
Goal: [What you're trying to achieve]
Data Type: [Decimal | DateTime | String | Integer | Boolean]
Example Data: [Sample values to test with]
```

## Examples

```
Type: Validation
Context: Trade
Goal: "SettleDate must be after TradeDate"
Data Type: DateTime
Example: TradeDate=2026-01-15, SettleDate=2026-01-20
→ XPath: /Trade/SettleDate > /Trade/TradeDate

Type: Calculation
Context: Allocation
Goal: "Calculate allocation percentage (allocated qty / trade qty)"
Data Type: Decimal
Example: AllocatedQty=100, TradeQty=500
→ XPath: /Allocation/Quantity div /Trade/TradeQuantity * 100

Type: Validation
Context: Compliance
Goal: "Credit rating must be BBB or higher"
Data Type: String
Example: Rating="Baa2"
→ XPath: bms:ratingTier(/Compliance/Rating) >= 3
```

---

## XPath Fundamentals in Allvue

### Basic Syntax

**Node Selection**:
```xpath
/Trade                          ← Root element
/Trade/TradeDate               ← Child element
/Trade/TradeDate/text()        ← Text content
/Trade/@TradeID                ← Attribute
//Trade                        ← Any Trade element at any depth
```

**Predicates (Filtering)**:
```xpath
/Trade[Status='Executed']      ← Where Status = 'Executed'
/Trade[Quantity > 100]         ← Where Quantity > 100
/Trade[1]                      ← First Trade element
/Trade[last()]                 ← Last Trade element
/Trade[position() <= 3]        ← First 3 trades
```

**Operators**:
```xpath
=, !=                          ← Equality
<, >, <=, >=                   ← Comparison
and, or, not()                 ← Boolean
+, -, *, div, mod              ← Arithmetic
|                              ← Union
```

### Allvue Custom Functions (bms: namespace)

**String Functions**:
```xpath
bms:uppercase(/Trade/Status)           ← Convert to uppercase
bms:lowercase(/Trade/Status)           ← Convert to lowercase
bms:substring(/Trade/Code, 1, 3)       ← Extract substring
bms:length(/Trade/Description)         ← String length
bms:concat(/Trade/ID, "-", /Trade/Status)  ← Concatenate
```

**Numeric Functions**:
```xpath
bms:round(/Allocation/Percentage, 2)   ← Round to 2 decimals
bms:floor(/Trade/Quantity)             ← Round down
bms:ceiling(/Trade/Quantity)           ← Round up
bms:abs(/Trade/Factor)                 ← Absolute value
bms:min(), bms:max()                   ← Min/max
```

**Date/Time Functions**:
```xpath
bms:today()                             ← Today's date
bms:now()                               ← Current datetime
bms:dateAdd(/Trade/TradeDate, 'D', 5)  ← Add 5 days
bms:dateDiff(/Trade/TradeDate, /Trade/SettleDate)  ← Days between
bms:bizDate(string(/Trade/TradeDate))   ← Business day conversion
bms:month(/Trade/TradeDate)             ← Extract month
bms:year(/Trade/TradeDate)              ← Extract year
```

**Conditional Functions**:
```xpath
bms:if(condition, true_value, false_value)
bms:choose(condition1, val1, condition2, val2, default)
bms:coalesce(val1, val2, val3)  ← Return first non-null
```

**Comparison Functions**:
```xpath
bms:compare(val1, operator, val2)  ← Compare with operator
bms:ratingTier(/Rating)            ← Convert rating to tier
bms:between(value, min, max)       ← Check range
```

---

## Common Patterns

### Pattern 1: Validation Rules

**Pattern**: Field X must be > Y
```xpath
/Trade/TradeQuantity > 0
<!-- English: Trade quantity must be positive -->
```

**Pattern**: Field X must be between Y and Z
```xpath
bms:between(/Trade/Factor, 0, 1)
<!-- English: Factor must be between 0 and 1 -->
```

**Pattern**: If condition, then required field must exist
```xpath
if(/Trade/AssetType='Option', /Trade/ExerciseDate, true())
<!-- English: If asset is Option, ExerciseDate is required; else always true -->
```

**Pattern**: Date X must be after Date Y
```xpath
/Trade/SettleDate > /Trade/TradeDate
<!-- English: Settlement date must be after trade date -->
```

### Pattern 2: Calculations

**Pattern**: Weighted calculation
```xpath
(/Allocation/Quantity * /Allocation/Price) div /Portfolio/TotalAUM * 100
<!-- English: Calculate allocation % of portfolio value -->
```

**Pattern**: Conditional calculation
```xpath
bms:if(/Trade/AssetType='Bond', 
  /Trade/Quantity * /Trade/Price * (1 + /Trade/Accrual),
  /Trade/Quantity * /Trade/Price)
<!-- English: Include accrual for bonds, not for other assets -->
```

**Pattern**: Fallback value
```xpath
bms:coalesce(/Trade/CustomFactor, /Trade/DefaultFactor, 1.0)
<!-- English: Use custom factor if exists, else default, else 1.0 -->
```

### Pattern 3: Filtering

**Pattern**: Only include active items
```xpath
/Portfolio/Holdings[Status='Active']
<!-- English: Return only active holdings -->
```

**Pattern**: Only include above threshold
```xpath
/Portfolio/Holdings[Position/Value > 100000]
<!-- English: Return positions worth > $100K -->
```

**Pattern**: Complex filter
```xpath
/Portfolio/Holdings[Status='Active' and AssetType='Bond' and Rating >= 'BBB']
<!-- English: Active bonds rated BBB or better -->
```

### Pattern 4: Rating/Tier Conversions

**Pattern**: Map rating string to numeric tier
```xpath
bms:case(
  /Compliance/Rating='Aaa', 1,
  /Compliance/Rating='Aa1', 2,
  /Compliance/Rating='Aa2', 2,
  /Compliance/Rating='Aa3', 2,
  /Compliance/Rating='A1', 3,
  4)  <!-- default tier 4 for anything else -->
<!-- English: Convert Moody's rating to internal tier -->
```

**Pattern**: Tiered limits based on rating
```xpath
bms:if(bms:ratingTier(/Holdings/Rating) <= 2,
  0.15,  <!-- Tier 2 or better: 15% limit -->
  bms:if(bms:ratingTier(/Holdings/Rating) <= 3,
    0.10,  <!-- Tier 3: 10% limit -->
    0.05))  <!-- Tier 4+: 5% limit -->
<!-- English: Concentration limit depends on credit rating -->
```

---

## Real Allvue Examples from Workflows

### Example 1: Bond Workflow Validation
```xml
<!-- From Workflow_Bond.xml -->
<WorkflowStepValidateOnSaveRule>
  <XPathExpression>
    bms:if(
      /Trade/AssetType='Bond',
      /Trade/SettleDate > bms:dateAdd(/Trade/TradeDate, 'D', 0) and
      /Trade/Factor > 0 and /Trade/Factor <= 1.0 and
      /Trade/YieldRate >= 0,
      true()
    )
  </XPathExpression>
  <ErrorMessage>Bond trade validation failed: Check settle date, factor (0-1), and yield rate</ErrorMessage>
</WorkflowStepValidateOnSaveRule>
```

**What it does**:
- If asset is Bond: Validate SettleDate > TradeDate, Factor 0-1, YieldRate >= 0
- If not Bond: Always valid (true())

### Example 2: Allocation Calculation
```xml
<!-- From AllocationRuleExpression -->
<AllocationExpression>
  bms:round(
    (/Trade/TradeQuantity * /Portfolio/TargetWeight) div 100,
    0
  )
</AllocationExpression>
```

**What it does**:
- Multiply trade quantity by portfolio's target weight %
- Divide by 100 to convert percentage
- Round to nearest whole number (0 decimals)

### Example 3: Compliance Scenario Expression
```xml
<!-- From ComplianceScenario_SectorConcentration -->
<ComplianceScenarioExpression>
  (
    bms:sum(
      /Portfolio/Holdings[Sector=$SectorID]/MarketValue
    ) div /Portfolio/TotalAUM
  ) * 100
</ComplianceScenarioExpression>
<ComplianceLimit>25</ComplianceLimit>
```

**What it does**:
- Sum market value of all holdings in specific sector
- Divide by total portfolio AUM
- Multiply by 100 for percentage
- Check if > 25% limit

### Example 4: Rating-Based Haircut
```xml
<!-- From DiscountLogic -->
<HaircutExpression>
  bms:case(
    bms:ratingTier(/Asset/Rating) = 1, 0.02,    <!-- AAA-A: 2% -->
    bms:ratingTier(/Asset/Rating) = 2, 0.03,    <!-- BBB: 3% -->
    bms:ratingTier(/Asset/Rating) = 3, 0.05,    <!-- BB: 5% -->
    bms:ratingTier(/Asset/Rating) = 4, 0.10,    <!-- B: 10% -->
    0.20)                                        <!-- Below B: 20% -->
</HaircutExpression>
```

**What it does**:
- Map credit rating to haircut percentage
- Higher risk = higher haircut

---

## XPath Writing Process

### Step 1: Understand the Data Structure

```xml
<!-- Trade object structure (XML) -->
<Trade>
  <TradeID>12345</TradeID>
  <TradeDate>2026-01-15</TradeDate>
  <SettleDate>2026-01-20</SettleDate>
  <AssetType>Bond</AssetType>
  <Quantity>1000</Quantity>
  <Price>98.50</Price>
  <Factor>0.95</Factor>
  <Status>Executed</Status>
  <Allocation>
    <PortfolioID>1</PortfolioID>
    <Quantity>500</Quantity>
  </Allocation>
</Trade>
```

### Step 2: Identify What You're Checking

Goal: "Validate that Factor is between 0 and 1, and SettleDate is after TradeDate"

### Step 3: Build XPath Components

```xpath
/Trade/Factor > 0                  ← Factor positive
/Trade/Factor <= 1                 ← Factor <= 1
/Trade/SettleDate > /Trade/TradeDate  ← SettleDate after TradeDate
```

### Step 4: Combine with Operators

```xpath
/Trade/Factor > 0 and /Trade/Factor <= 1 and /Trade/SettleDate > /Trade/TradeDate
```

Or use built-in function:

```xpath
bms:between(/Trade/Factor, 0, 1) and /Trade/SettleDate > /Trade/TradeDate
```

### Step 5: Test with Sample Data

```
Test: TradeDate=2026-01-15, SettleDate=2026-01-20, Factor=0.95
Result: true() ✓

Test: TradeDate=2026-01-15, SettleDate=2026-01-10, Factor=0.95
Result: false() ✓ (SettleDate before TradeDate)

Test: TradeDate=2026-01-15, SettleDate=2026-01-20, Factor=1.5
Result: false() ✓ (Factor > 1)
```

---

## Common XPath Mistakes & Fixes

### Mistake 1: Wrong Syntax for "and"
```xpath
❌ /Trade/Factor > 0 & /Trade/Factor <= 1
✅ /Trade/Factor > 0 and /Trade/Factor <= 1
```

### Mistake 2: Forgetting "/" for Absolute Path
```xpath
❌ Trade/TradeDate > TradeDate  (this looks for nested element)
✅ /Trade/TradeDate > /Trade/TradeDate
```

### Mistake 3: String vs Number Comparison
```xpath
❌ /Trade/Status > 'Active'  (can't compare strings with >)
✅ /Trade/Status = 'Active'
```

### Mistake 4: Not Escaping Quotes
```xpath
❌ /Trade[Status='Executed']  (mismatched quotes)
✅ /Trade[Status = 'Executed']
✅ /Trade[@Status = "Executed"]
```

### Mistake 5: Forgetting dateAdd Second Parameter
```xpath
❌ bms:dateAdd(/Trade/TradeDate, 5)  (missing unit: D, M, Y)
✅ bms:dateAdd(/Trade/TradeDate, 'D', 5)  (Add 5 Days)
✅ bms:dateAdd(/Trade/TradeDate, 'M', 1)  (Add 1 Month)
```

### Mistake 6: Confusing "=" with "=="
```xpath
❌ /Trade/Status == 'Active'  (XPath uses single =)
✅ /Trade/Status = 'Active'
```

### Mistake 7: Missing bms: Namespace
```xpath
❌ round(/Trade/Factor, 2)  (not recognized)
✅ bms:round(/Trade/Factor, 2)
```

---

## Output Format

```markdown
# XPath Expression: {Purpose}

## Goal
{What you're trying to achieve}

## Data Structure
\`\`\`xml
{XML structure showing element names and types}
\`\`\`

## Expression
\`\`\`xpath
{Complete XPath expression}
\`\`\`

## English Translation
{What this expression does in plain English}

## Components
1. {Component 1}: {Explanation}
2. {Component 2}: {Explanation}
3. ...

## Test Cases

**Test 1**: {Sample data}
- Expected: {Expected result}
- Actual: {Actual result}
- Status: ✓ PASS / ✗ FAIL

**Test 2**: {Edge case data}
- Expected: {Expected result}
- Actual: {Actual result}
- Status: ✓ PASS / ✗ FAIL

## Used In
- Workflow: {WorkflowName}
- Compliance: {ComplianceRule}
- Validation: {RuleName}

## Related Expressions
- {RelatedExpression1}
- {RelatedExpression2}
```

---

## XPath Functions Reference

| Category | Function | Example | Result |
|----------|----------|---------|--------|
| **Numeric** | bms:round(x, n) | bms:round(3.14159, 2) | 3.14 |
| | bms:floor(x) | bms:floor(3.9) | 3 |
| | bms:ceiling(x) | bms:ceiling(3.1) | 4 |
| | bms:abs(x) | bms:abs(-5) | 5 |
| | bms:min(a,b) | bms:min(3,5) | 3 |
| | bms:max(a,b) | bms:max(3,5) | 5 |
| **String** | bms:uppercase(s) | bms:uppercase("bond") | BOND |
| | bms:lowercase(s) | bms:lowercase("BOND") | bond |
| | bms:substring(s, start, len) | bms:substring("12345", 1, 3) | 123 |
| | bms:length(s) | bms:length("hello") | 5 |
| | bms:concat(s1,s2) | bms:concat("A","-","B") | A-B |
| **Date** | bms:today() | bms:today() | 2026-09-15 |
| | bms:now() | bms:now() | 2026-09-15T10:30:00 |
| | bms:dateAdd(d, u, n) | bms:dateAdd(date, 'D', 5) | date+5days |
| | bms:month(d) | bms:month(2026-09-15) | 9 |
| | bms:year(d) | bms:year(2026-09-15) | 2026 |
| **Logical** | bms:if(c,t,f) | bms:if(x>0, "pos", "neg") | "pos" if x>0 |
| | bms:coalesce(a,b,c) | bms:coalesce(null, 5) | 5 |
| | bms:between(v,min,max) | bms:between(3, 1, 5) | true |
| **Rating** | bms:ratingTier(r) | bms:ratingTier("Baa2") | 3 |
| | bms:case() | bms:case(r='A',1,r='B',2,3) | 1 or 2 or 3 |

---

## Implementation Checklist

- [ ] Understand data structure (XML elements/attributes)
- [ ] Write XPath expression
- [ ] Test with valid data
- [ ] Test with edge case data
- [ ] Test with invalid data
- [ ] Verify error handling
- [ ] Document English translation
- [ ] Get business review
- [ ] Deploy to development environment
- [ ] Validate in system
- [ ] Move to production

---

This skill answers: **"How do I write XPath expressions for Allvue workflows, validation, and calculations?"**
