# ERROR Failure Analysis

## What is an ERROR?

An ERROR occurs when a command's status becomes 5 (error status). This indicates an explicit error was detected during tool execution.

## Identification

- **Reason**: `ERROR`
- **Reason 2**: `diff` (typically)
- Check `test.out` for lines containing "ERROR"

## Analysis Steps

1. **Find the error in test.out**:
   ```bash
   grep -i "error" test.out
   ```

2. **Identify the failing command**:
   - Check `Failing Command` from script output
   - Look at corresponding log file: `<command>.log`

3. **Examine the diff.bak file**:
   - Compare expected vs actual output
   - Look for what changed to cause error status

4. **Check input files**:
   - Verify input files are correct
   - Check for any corrupted or missing inputs

## Common Causes

- Invalid input data
- Tool detected a constraint violation
- Configuration error
- License issues
- Resource limitations

## Categorization Decision Tree

1. **Is the error due to environment/config?** → SETUP ISSUE
   - Missing files, wrong paths, permission issues

2. **Is the error expected due to valid changes?** → REGOLD
   - Tool behavior intentionally changed
   - Error threshold changed

3. **Is the error a genuine tool bug?** → REPORT TO RnD
   - Tool should not have errored with valid input
   - Regression from previous behavior

## Information to Collect

1. Exact error message
2. Input files that triggered the error
3. Tool version
4. Expected vs actual behavior
