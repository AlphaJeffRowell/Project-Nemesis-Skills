# XPath Navigator Skill

**Trigger:** "write xpath", "build validation rule", "xpath expression"  
**Purpose:** Write XPath expressions for workflow validation and calculations  
**Status:** Ready for deployment  
**Tier:** Expressions & Transforms (Specialized Universal)

---

## Quick Start

Ask the skill to write validation rules:
- "Write XPath: SettleDate > TradeDate"
- "Build validation for Quantity > 0"
- "Calculate allocation percentage"

The skill will:
1. Analyze requirement
2. Write XPath expression
3. Explain the syntax
4. Show examples
5. Validate the logic

---

## What It Does

Answers: "How do I validate that X > Y? How do I calculate percentages in XPath?"

**Inputs:**
- Validation requirement (English)
- Field names
- Condition type
- Error message

**Outputs:**
- XPath expression (ready to use)
- Logic explanation
- Usage context
- Example scenarios
- Error handling

---

## How It Works

1. **Parse** — Understand requirement
2. **Map** — Identify field names
3. **Write** — Create XPath expression
4. **Test** — Validate with examples
5. **Deploy** — Ready for workflow rules

---

## Real-World Examples

### Example 1: Date Validation
```
User: "Write XPath: SettleDate > TradeDate"
↓
Skill: XPath: @SettleDate > @TradeDate
       Syntax: Compares two date fields
       Usage: Bond workflow validation
       Example: TradeDate=2026-09-15 → SettleDate must be >= 2026-09-17
```

### Example 2: Percentage Calculation
```
User: "Calculate allocation percentage"
↓
Skill: XPath: (@AllocQty div @TotalQty) * 100
       Returns: Numeric percentage
       Usage: Allocation workflow step
       Example: 25 / 100 = 25%
```

### Example 3: Complex Validation
```
User: "Validate: Qty > 0 AND Price in range AND Funds available"
↓
Skill: XPath: @Qty > 0 and @Price >= @MinPrice and @Price <= @MaxPrice and @AvailableFunds >= (@Qty * @Price)
       Type: Multi-condition with AND logic
       Usage: Order entry validation
```

---

## Deployment

✅ **Ready for deployment** — 150+ XPath patterns documented

---

See IMPLEMENTATION.md for technical details.
