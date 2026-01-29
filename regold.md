# REGOLD - Analysis & Next Steps Guide

## Overview

A **REGOLD** is required when the test failure represents a valid/improved change that should become the new baseline (gold file).

---

## When to Categorize as REGOLD

Use this category when:
- ✅ Output improved (better metrics, fewer issues)
- ✅ Expected behavioral change from known tool updates
- ✅ Format/presentation changes that don't affect correctness
- ✅ Acceptable noise variations within tolerance
- ✅ Algorithm improvements causing different (but correct) results
- ✅ Version string or timestamp changes
- ✅ Ordering changes that don't affect correctness

---

## Proof Required

Before categorizing as REGOLD, you MUST provide:

1. **The exact diff content** showing what changed
2. **Explanation of WHY** the new output is valid/better
3. **Confirmation** no functional regression occurred
4. **Evidence** that change is expected or beneficial

---

## When NOT to REGOLD

⚠️ **Do NOT categorize as REGOLD if:**

- The change indicates a real bug (regression)
- Output quality decreased
- Correctness is compromised
- The change is unexpected and unexplained
- You haven't investigated the root cause

---

## Analysis Checklist

Before deciding REGOLD, complete this verification:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│              REGOLD VERIFICATION CHECKLIST                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ CHANGE UNDERSTANDING:                                                       │
│ □ I have read the COMPLETE diff.bak file                                    │
│ □ I understand WHAT changed (not just that something changed)               │
│ □ I can categorize the type of change (format/value/order/etc.)             │
│                                                                             │
│ VALIDITY CHECK:                                                             │
│ □ The new output is correct/valid                                           │
│ □ The change is expected OR beneficial                                      │
│ □ No functional regression occurred                                         │
│ □ The change doesn't hide a real problem                                    │
│                                                                             │
│ ROOT CAUSE:                                                                 │
│ □ I know WHY the output changed                                             │
│ □ The cause is legitimate (tool improvement, format update, etc.)           │
│                                                                             │
│ COUNTER-ARGUMENTS:                                                          │
│ □ I've considered if this could be a bug masquerading as improvement        │
│ □ I've verified the setup was correct (not setup issue)                     │
│ □ I've checked if this is actually a valid output                           │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│ If ANY box unchecked → Investigate more before categorizing as REGOLD.      │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Types of Valid REGOLD Changes

### 1. Format Changes
- Whitespace adjustments
- Column alignment changes
- Output formatting improvements

### 2. Ordering Changes
- Different but equivalent ordering of results
- Parallel execution causing different order
- Hash-based ordering differences

### 3. Version/Timestamp Changes
- Tool version strings updated
- Build timestamps different
- Date/time in output

### 4. Numeric Precision Changes
- Floating point representation differences
- Precision improvements
- Rounding changes within tolerance

### 5. Performance Metrics Changes
- Improved metrics (fewer violations, better coverage)
- Optimization results
- Resource usage changes

### 6. Expected Behavioral Changes
- Known tool updates documented in release notes
- Algorithm improvements
- Feature enhancements

---

## Next Steps After REGOLD Decision

### Step 1: Document the Change

```markdown
### REGOLD Justification

**Type of Change**: <Format / Ordering / Version / Metrics / Behavioral>

**What Changed**:
<Specific description of the diff>

**Why This is Valid**:
<Explanation of why new output is acceptable>

**Evidence**:
```
<Relevant portion of diff.bak>
```
```

### Step 2: Regold Procedure

```bash
# Navigate to testcase
cd <testcase_path>

# Identify the platform gold directory
ls golds.*/

# Backup current gold (recommended)
cp golds.<platform>/log_<command> golds.<platform>/log_<command>.backup

# Copy new output to gold
cp testresults/log_<command> golds.<platform>/log_<command>

# If status.log changed
cp testresults/status.log golds.<platform>/status.log

# Verify the copy
diff testresults/log_<command> golds.<platform>/log_<command>
# Should show no differences
```

### Step 3: Commit the Regold

```bash
# Add regolded files
git add golds.<platform>/

# Commit with descriptive message
git commit -m "Regold <testcase_name>: <brief description of change>

Reason: <why regold is appropriate>
Category: REGOLD
Diff type: <format/ordering/version/metrics/behavioral>"
```

---

## Output Format for REGOLD

```markdown
## Testcase Analysis Report

**Path**: <testcase_path>
**Status**: ❌ FAILED (Requires REGOLD)
**Category**: ✅ REGOLD

---

### Failure Analysis

**Failing Command**: <command that produced diff>
**Diff File**: <name of .diff.bak file>

---

### Change Analysis

**Type of Change**: <Format / Ordering / Version / Metrics / Behavioral>

**What Changed**:
<Detailed description>

**Diff Content**:
```
<Relevant portion of diff.bak showing the change>
```

---

### REGOLD Justification

**Why new output is valid/better**:
- <Reason 1>
- <Reason 2>

**Why this is NOT a bug**:
- <Evidence that this is expected/beneficial>

**Why this is NOT setup issue**:
- <Evidence setup was correct>

---

### Next Steps

1. Review the diff to confirm REGOLD is appropriate
2. Regold command:
   ```bash
   cp testresults/<file> golds.<platform>/<file>
   ```
3. Commit with message: "Regold: <brief reason>"

---

### Confidence: <HIGH/MEDIUM>
```

---

## Counter-Arguments to Consider

Before finalizing REGOLD:

1. **Is the new output actually worse?**
   - Check if metrics degraded
   - Verify no correctness issues

2. **Could this indicate a bug?**
   - Is the change unexpected?
   - Does it only happen in certain conditions?

3. **Is there a hidden problem?**
   - Could regolding mask a real issue?
   - Would a senior engineer approve this regold?

---

## Examples

### Example 1: Format Change

**Diff shows**:
```diff
-Coverage: 85.00%
+Coverage: 85.0%
```

**Analysis**: Simple format change - fewer decimal places displayed. Functionally equivalent.

**Verdict**: ✅ REGOLD - Format presentation change, no functional impact.

### Example 2: Improved Metrics

**Diff shows**:
```diff
-Violations found: 5
+Violations found: 3
```

**Analysis**: Fewer violations indicates improvement. Verify this is due to tool improvement, not missing checks.

**Verdict**: ✅ REGOLD - If tool release notes confirm improved violation detection.

### Example 3: Suspicious Change

**Diff shows**:
```diff
-Test patterns generated: 1000
+Test patterns generated: 500
```

**Analysis**: 50% fewer patterns could indicate a bug. Investigate before regolding.

**Verdict**: ❓ INVESTIGATE FURTHER - This could be a regression, not improvement.
