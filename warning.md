# Warning Failure Analysis

## What is a Warning Failure?

A warning failure occurs when a new warning is detected in the tool output that wasn't present in the golden files.

## Identification

- **Reason**: `Warning`
- **Reason 2**: `diff`
- Look for new warning messages in diff.bak files

## Analysis Steps

1. **Find the warning**:
   ```bash
   grep -i "warning" *.log test.out
   ```

2. **Examine the diff.bak file**:
   - Identify the exact warning message
   - Check if warning is new or modified

3. **Understand the warning context**:
   - What is the warning about?
   - Which tool generated it?
   - What input triggered it?

4. **Assess warning validity**:
   - Is this a legitimate warning?
   - Is it a new tool feature?
   - Does it affect correctness?

## Common Causes

- New tool checks added
- Input data triggers new warnings
- Tool behavior changes
- Threshold changes

## Categorization Decision Tree

1. **Is the warning expected and valid?** → REGOLD
   - New tool feature
   - Improved detection
   - Cosmetic/informational changes

2. **Is the warning due to setup?** → SETUP ISSUE
   - Environment issues
   - Configuration problems
   - Missing/wrong files

3. **Is the warning a bug?** → REPORT TO RnD
   - False positive
   - Incorrect warning message
   - Regression

## Difference from Sev Warning

- **Warning**: Lower severity, often informational
- **Sev Warning**: Higher severity, indicates potential issues

Warnings are more commonly candidates for REGOLD as they often represent tool improvements or informational messages.

## Information to Collect

1. Exact warning text
2. Tool that generated warning
3. Comparison with golden output
4. Whether warning affects functionality
