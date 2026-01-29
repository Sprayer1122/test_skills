# Exit Status Failure Analysis

## What is an Exit Status Failure?

An exit status failure occurs when a command's exit code changed from expected value (e.g., from 2 to 5). This indicates the tool returned a different status than what was recorded in the golden files.

## Identification

- **Reason**: `Exit status`
- **Reason 2**: `diff`
- Check `test.out` for exit status mismatch

## Analysis Steps

1. **Find the status change**:
   - Look in the diff.bak file for status differences
   - Check `test.out` for the command that changed status

2. **Understand the status codes**:
   | Code | Typical Meaning |
   |------|-----------------|
   | 0 | Success |
   | 1 | General error |
   | 2 | Warning/Minor issue |
   | 5 | Error status |

3. **Check the command's log file**:
   - Look for what caused the different exit status
   - Search for errors or warnings

4. **Compare with golden**:
   - What was the expected exit status?
   - What is the new exit status?
   - Why did it change?

## Common Causes

- Tool behavior change (intended or bug)
- New warnings/errors detected
- Input data changes
- Environment differences

## Categorization Decision Tree

1. **Did exit status change due to valid improvement?** → REGOLD
   - Tool now catches more issues (higher status)
   - Tool fixed an issue (lower status)

2. **Did exit status change due to environment?** → SETUP ISSUE
   - Missing dependencies
   - Wrong configuration

3. **Is the status change unexpected/incorrect?** → REPORT TO RnD
   - Tool regression
   - Incorrect behavior

## Information to Collect

1. Previous exit status (from golden)
2. New exit status
3. What the tool output shows for this status change
4. Whether any warnings/errors appeared
