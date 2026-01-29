# Severe Warning Failure Analysis

## What is a Severe Warning?

A severe warning (Sev Warning) occurs when a new severe-level warning is detected in the tool output that wasn't present in the golden files.

## Identification

- **Reason**: `Sev Warning`
- **Reason 2**: `diff`
- Look for "Sev Warning" or "Severe Warning" in diff.bak files

## Analysis Steps

1. **Find the severe warning**:
   ```bash
   grep -i "sev.*warn\|severe.*warn" *.log test.out
   ```

2. **Examine the diff.bak file**:
   - Identify the exact warning message
   - Note the line number and context

3. **Understand the warning**:
   - What is the warning about?
   - Is it a new check that was added?
   - Is it detecting a real issue?

4. **Check if warning is valid**:
   - Does the warning indicate a real problem?
   - Is this a new tool feature catching issues?

## Common Causes

- New validation checks added to tool
- Design rule violations detected
- Constraint violations
- Potential issues the tool now catches

## Categorization Decision Tree

1. **Is the warning a new valid check?** → REGOLD
   - Tool added new validation
   - Warning is informational and correct
   - Output is still functionally correct

2. **Is the warning due to testcase setup?** → SETUP ISSUE
   - Input files have issues
   - Configuration causes warning

3. **Is the warning indicating a tool bug?** → REPORT TO RnD
   - False positive warning
   - Warning message is incorrect
   - Tool shouldn't warn for this case

## Information to Collect

1. Exact warning message
2. File/line causing the warning
3. Whether the warning is valid
4. Tool version that introduced this warning
