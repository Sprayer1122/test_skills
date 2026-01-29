# Core Dump Failure Analysis

## What is a Core Dump?

A core dump occurs when a tool crashes and generates a `core.*` file. This indicates a serious tool crash that typically needs to be reported to RnD.

## Identification

- **Reason**: `Core Dump`
- **Reason 2**: `core`
- Look for `core.*` files in the testcase directory

## Analysis Steps

1. **Locate the core file**:
   ```bash
   ls -la core.*
   ```

2. **Identify which tool crashed**:
   - Check the `Failing Command` from script output
   - Look in `test.out` for the crash line

3. **Get stack trace** (if gdb available):
   ```bash
   gdb <tool_binary> core.* -ex "bt" -ex "quit"
   ```

4. **Check tool logs**:
   - Look for the corresponding `.log` file for the crashed tool
   - Search for error messages before the crash

## Common Causes

- Memory corruption
- Null pointer dereference
- Stack overflow
- Segmentation fault

## Categorization

Core dumps are almost always **REPORT TO RnD** unless:
- The core dump is due to a known infrastructure issue (Setup Issue)
- The testcase itself is misconfigured causing invalid input to the tool

## Information to Collect for RnD

1. Core file location
2. Stack trace (if available)
3. Tool version
4. Input files that caused the crash
5. Reproduction steps
