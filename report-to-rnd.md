# REPORT TO RnD - Analysis & Bug Report Guide

## Overview

**REPORT TO RnD** is the category for genuine bugs or issues in the DFT tool that require developer investigation.

---

## When to Categorize as REPORT TO RnD

Use this category when:
- 🐛 Tool crashed (core dump) with valid inputs
- 🐛 Incorrect computational results
- 🐛 Missing expected outputs that should exist
- 🐛 Regression from previously working functionality
- 🐛 Behavior violates DFT correctness requirements
- 🐛 Tool produces wrong/corrupted output
- 🐛 Algorithm error causing incorrect results

---

## Proof Required

Before categorizing as REPORT TO RnD, you MUST:

1. **Verify setup is correct** - This is NOT a setup issue
2. **Verify output is wrong** - This is NOT a regold candidate
3. **Show exact failure evidence** - Core dump, wrong output, missing data
4. **Provide reproduction steps** - How to recreate the issue

---

## Critical Pre-Check

⚠️ **Before reporting to RnD, VERIFY:**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│              PRE-REPORT VERIFICATION                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ SETUP VERIFICATION:                                                         │
│ □ All paths exist and are correct                                           │
│ □ Environment variables are set correctly                                   │
│ □ Licenses are available                                                    │
│ □ Input files are valid and not corrupted                                   │
│ □ Gold files exist for this platform                                        │
│ □ Makefile configuration is correct                                         │
│                                                                             │
│ INPUT VERIFICATION:                                                         │
│ □ Design files are syntactically correct                                    │
│ □ Configuration files are valid                                             │
│ □ No missing dependencies                                                   │
│                                                                             │
│ NOT A REGOLD:                                                               │
│ □ The output is genuinely WRONG, not just different                         │
│ □ This is not an expected behavioral change                                 │
│ □ This is not a format/ordering change                                      │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│ If ANY setup issue found → Categorize as SETUP ISSUE instead.               │
│ If output is valid but different → Categorize as REGOLD instead.            │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Types of RnD Issues

### 1. Core Dump / Crash
Tool crashes and generates core file.

**Evidence needed**:
- Core file location
- Stack trace if available
- What inputs triggered crash

### 2. Incorrect Results
Tool produces wrong output values.

**Evidence needed**:
- Expected value vs actual value
- Why expected value is correct
- Source of expected value

### 3. Missing Output
Tool fails to produce expected output.

**Evidence needed**:
- What output is missing
- Why it should exist
- Similar cases where it works

### 4. Regression
Previously working functionality now fails.

**Evidence needed**:
- When it last worked
- What changed (tool version, inputs)
- Comparison with working version

### 5. Correctness Violation
Tool violates DFT correctness requirements.

**Evidence needed**:
- Which requirement is violated
- How tool output violates it
- Expected correct behavior

---

## Analysis Checklist

```
┌─────────────────────────────────────────────────────────────────────────────┐
│              REPORT TO RnD VERIFICATION                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ BUG IDENTIFICATION:                                                         │
│ □ I can clearly describe WHAT is wrong                                      │
│ □ I know WHAT the correct behavior should be                                │
│ □ I have evidence the tool (not setup) is at fault                          │
│                                                                             │
│ SETUP RULED OUT:                                                            │
│ □ I verified all paths/files exist                                          │
│ □ I verified environment is correct                                         │
│ □ I verified inputs are valid                                               │
│ □ The same setup works in other cases                                       │
│                                                                             │
│ REGOLD RULED OUT:                                                           │
│ □ The new output is genuinely WRONG                                         │
│ □ This is NOT an improvement or expected change                             │
│ □ Accepting this would hide a real problem                                  │
│                                                                             │
│ REPRODUCTION:                                                               │
│ □ I can describe how to reproduce this                                      │
│ □ I know the minimal inputs to trigger this                                 │
│ □ I know if this is deterministic or intermittent                           │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│ If ANY doubt about setup/regold → Investigate more first.                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Bug Report Format

When reporting to RnD, provide this information:

```markdown
## Bug Report: <Brief Title>

### Summary
<One sentence description of the bug>

### Testcase Information
- **Path**: <testcase path>
- **Failing Command**: <command that failed>
- **Tool Version**: <if known>
- **Platform**: <linux24/linux26_64/etc>

### Bug Type
<Core Dump / Incorrect Results / Missing Output / Regression / Correctness Violation>

---

### Expected Behavior
<What SHOULD happen>

**Evidence of expected behavior**:
<Gold file content, documentation, similar working case>

### Actual Behavior
<What ACTUALLY happens>

**Error/output**:
```
<Relevant error message or incorrect output>
```

---

### Reproduction Steps

1. Navigate to: `<testcase_path>`
2. Run: `<command to run>`
3. Observe: `<what to look for>`

**Minimal reproduction** (if possible):
<Smallest input that triggers the bug>

---

### Evidence That This Is NOT Setup Issue

<List evidence that setup is correct>
- Path X exists: `ls -la <path>`
- Env var Y is correct: `echo $Y`
- Input files are valid: <how you verified>

### Evidence That This Is NOT Regold

<List evidence that output is genuinely wrong>
- Expected: <value>
- Actual: <value>
- Why expected is correct: <reason>

---

### Additional Information

**Related logs**:
```
<Relevant log excerpts>
```

**Core dump location** (if applicable):
`<path to core file>`

**Possibly related issues**:
<Any known similar issues>

---

### Priority Assessment
- **Severity**: <Critical / High / Medium / Low>
- **Frequency**: <Always / Sometimes / Rare>
- **Workaround**: <Available / Not available>
```

---

## Output Format for REPORT TO RnD

```markdown
## Testcase Analysis Report

**Path**: <testcase_path>
**Status**: ❌ FAILED
**Category**: 🐛 REPORT TO RnD

---

### Failure Analysis

**Failure Point**: <Specific command/phase>
**Bug Type**: <Core Dump / Incorrect Results / Missing Output / Regression>

---

### Bug Description

**What went wrong**:
<Clear description of the bug>

**Expected behavior**:
<What should have happened>

**Actual behavior**:
<What actually happened>

---

### Evidence

**Key evidence**:
```
<Error message, incorrect output, diff content>
```

**Setup verification**:
- ✅ Paths verified: <evidence>
- ✅ Environment verified: <evidence>
- ✅ Inputs verified: <evidence>

**Why this is NOT regold**:
<Why the output is wrong, not just different>

---

### Reproduction

**Steps**:
1. cd <testcase_path>
2. <run command>
3. <observe error>

**Minimal case**:
<If identified>

---

### Recommended Action

Report to RnD team with:
- Testcase path
- Full error log
- Core file (if applicable)
- This analysis report

**Priority**: <Critical / High / Medium / Low>
**Assignee**: <RD engineer from test.out if available>

---

### Confidence: HIGH (95%)
```

---

## Counter-Arguments to Consider

Before finalizing REPORT TO RnD:

1. **Could this be a setup issue in disguise?**
   - Did you verify ALL paths and files?
   - Is the environment truly correct?
   - Could a missing dependency cause this?

2. **Could this be a valid regold?**
   - Is the output actually wrong, or just different?
   - Could this be an expected tool change?
   - Is the "expected" output actually correct?

3. **Do you have enough evidence?**
   - Can you prove the setup is correct?
   - Can you demonstrate the output is wrong?
   - Can you explain how to reproduce?

---

## Examples

### Example 1: Core Dump

**Situation**: Tool crashes with segmentation fault

**Analysis**:
```
Bug Type: Core Dump
Evidence: core.12345 file in testcase directory
Command: build_model
Setup verified: Yes - same inputs work on other testcases
Inputs verified: Yes - design files are valid

Root cause: Tool crashes on specific input pattern
Reproduction: Run build_model on src/design.v
```

### Example 2: Incorrect Results

**Situation**: Tool reports wrong coverage value

**Analysis**:
```
Bug Type: Incorrect Results
Expected: Coverage should be 85% (based on manual count)
Actual: Tool reports 45%
Setup verified: Yes - all files correct
Not regold: 45% is wrong, not an improvement

Root cause: Tool miscounting coverage points
Reproduction: Run coverage analysis on design.v
```

### Example 3: Missing Output

**Situation**: Tool doesn't generate expected report

**Analysis**:
```
Bug Type: Missing Output
Expected: patterns.rpt file should be created
Actual: File not created, no error message
Setup verified: Yes - all inputs present
Not regold: Missing file is error, not format change

Root cause: Tool silently fails to generate report
Reproduction: Run create_patterns command
```
