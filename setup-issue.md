# SETUP ISSUE - Analysis & Solution Guide

## Overview

A **SETUP ISSUE** occurs when the test failure is due to infrastructure, environment, or configuration problems - NOT the DFT tool's logic itself.

---

## When to Categorize as SETUP ISSUE

Use this category when:
- ❌ Missing files, wrong paths, permission issues
- ❌ License checkout failures
- ❌ Job killed/timeout by infrastructure (LSF, etc.)
- ❌ Missing or incorrect gold files
- ❌ Environment variable issues
- ❌ Network/disk/NFS problems
- ❌ Incorrect Makefile configuration
- ❌ Infrastructure script errors

---

## Proof Required

Before categorizing as SETUP ISSUE, you MUST provide:

1. **The specific infrastructure error** from logs
2. **Which execution phase failed** (Phase 1-4, 6, or 9)
3. **Confirmation** that DFT tool logic itself is NOT at fault
4. **Root cause trace** showing WHY the setup failed

---

## ⚠️ MANDATORY: Solution Identification

**When categorizing as SETUP ISSUE, you MUST provide:**

1. ✅ **What is incorrect** - The specific configuration/setup that is wrong
2. ✅ **What needs to be corrected** - The exact fix required
3. ✅ **Where to make the fix** - File path/location of the fix
4. ✅ **Who should fix it** - Infrastructure team, testcase owner, or environment admin

---

## Common Setup Issues & Solutions

### 1. Path/File Missing Issues

#### Symptoms
```
No such file or directory: /path/to/something
Cannot find file: xyz.tcl
```

#### Root Cause Investigation
```bash
# Check if path exists
ls -la /path/to/something

# Check parent directories
ls -la /path/to/
ls -la /path/

# Find where path is set
grep -r "/path/to/something" Makefile
grep -r "/path/to/something" *.tcl
```

#### Solution Template
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SOLUTION: PATH/FILE MISSING                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ ❌ WHAT IS INCORRECT:                                                       │
│    Path: <exact path that doesn't exist>                                    │
│    Referenced in: <file:line where path is used>                            │
│    Expected to contain: <what should be at that path>                       │
│                                                                             │
│ ✅ WHAT NEEDS TO BE CORRECTED:                                              │
│    Option A: Create missing path/file                                       │
│      - Command: mkdir -p /path/to/something                                 │
│      - OR: Copy required file from <source>                                 │
│                                                                             │
│    Option B: Update path reference to correct location                      │
│      - File to edit: <Makefile or script path>                              │
│      - Line number: <line>                                                  │
│      - Change from: <old path>                                              │
│      - Change to: <new correct path>                                        │
│                                                                             │
│ 🔧 WHO SHOULD FIX:                                                          │
│    [ ] Testcase owner - if testcase-specific path                           │
│    [ ] Infrastructure team - if common infrastructure path                  │
│    [ ] Environment admin - if machine/env specific                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### 2. Environment Variable Issues

#### Symptoms
```
Variable undefined: $MODUS_HOME
Wrong tool version loaded
Incorrect library path
```

#### Root Cause Investigation
```bash
# Check current value
echo $VARIABLE_NAME
env | grep VARIABLE

# Find where it should be set
grep -r "VARIABLE_NAME" Makefile
grep -r "VARIABLE_NAME" *.sh

# Check setup scripts
cat setup.sh | grep VARIABLE
```

#### Solution Template
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SOLUTION: ENVIRONMENT VARIABLE                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ ❌ WHAT IS INCORRECT:                                                       │
│    Variable: $VARIABLE_NAME                                                 │
│    Current value: <current value or "undefined">                            │
│    Expected value: <what it should be>                                      │
│    Used in: <file:line where variable is used>                              │
│                                                                             │
│ ✅ WHAT NEEDS TO BE CORRECTED:                                              │
│    Set correct value before running test:                                   │
│      export VARIABLE_NAME=<correct_value>                                   │
│                                                                             │
│    OR update setup script:                                                  │
│      File: <path to setup script>                                           │
│      Line: <line number>                                                    │
│      Change: <old assignment> → <new assignment>                            │
│                                                                             │
│ 🔧 WHO SHOULD FIX:                                                          │
│    [ ] Test submitter - set env before running                              │
│    [ ] Infrastructure team - update setup scripts                           │
│    [ ] Testcase owner - update testcase Makefile/scripts                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### 3. License Issues

#### Symptoms
```
License checkout failed
Cannot obtain license for feature X
License server not responding
```

#### Root Cause Investigation
```bash
# Check license configuration
echo $LM_LICENSE_FILE
cat lic.debug.log

# Check license server connectivity
ping <license_server>

# Check available licenses
lmstat -a -c $LM_LICENSE_FILE
```

#### Solution Template
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SOLUTION: LICENSE ISSUE                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ ❌ WHAT IS INCORRECT:                                                       │
│    License variable: $LM_LICENSE_FILE                                       │
│    Current value: <current value>                                           │
│    License server status: <reachable/unreachable>                           │
│    Feature requested: <feature name>                                        │
│    Error from lic.debug.log: <specific error>                               │
│                                                                             │
│ ✅ WHAT NEEDS TO BE CORRECTED:                                              │
│    If wrong license path:                                                   │
│      export LM_LICENSE_FILE=<correct_license_path>                          │
│                                                                             │
│    If server unreachable:                                                   │
│      - Check network connectivity to license server                         │
│      - Contact IT to verify server status                                   │
│      - Use alternate license server if available                            │
│                                                                             │
│    If no licenses available:                                                │
│      - Wait for licenses to free up                                         │
│      - Request additional licenses from IT                                  │
│                                                                             │
│ 🔧 WHO SHOULD FIX:                                                          │
│    [ ] Test submitter - if personal env setup wrong                         │
│    [ ] IT/License admin - if server issue                                   │
│    [ ] Infrastructure team - if common setup wrong                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### 4. Makefile Configuration Issues

#### Symptoms
```
Make target not found
Wrong options passed to tool
Incorrect TEST_TARGETS configuration
```

#### Root Cause Investigation
```bash
# Read the Makefile
cat Makefile

# Check included files
grep "include" Makefile
cat <included_makefile>

# Check variable definitions
grep "TEST_TARGETS\|VERIFY_TARGETS\|LOCAL_" Makefile
```

#### Solution Template
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SOLUTION: MAKEFILE CONFIGURATION                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ ❌ WHAT IS INCORRECT:                                                       │
│    File: <path to Makefile>                                                 │
│    Line: <line number>                                                      │
│    Current content: <current problematic content>                           │
│    Problem: <description of what's wrong>                                   │
│                                                                             │
│ ✅ WHAT NEEDS TO BE CORRECTED:                                              │
│    Edit file: <path to Makefile>                                            │
│    Line: <line number>                                                      │
│    Change from:                                                             │
│      <current content>                                                      │
│    Change to:                                                               │
│      <corrected content>                                                    │
│                                                                             │
│    Explanation: <why this change fixes the issue>                           │
│                                                                             │
│ 🔧 WHO SHOULD FIX:                                                          │
│    [ ] Testcase owner - owns the testcase Makefile                          │
│    [ ] Infrastructure team - if common Makefile template                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### 5. Permission Issues

#### Symptoms
```
Permission denied
Cannot write to directory
Cannot execute file
```

#### Root Cause Investigation
```bash
# Check file permissions
ls -la /path/to/file

# Check directory permissions
ls -la /path/to/directory/

# Check current user
id
groups
```

#### Solution Template
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SOLUTION: PERMISSION ISSUE                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ ❌ WHAT IS INCORRECT:                                                       │
│    Path: <path to file/directory>                                           │
│    Current permissions: <ls -la output>                                     │
│    Current owner/group: <owner:group>                                       │
│    Required permission: <read/write/execute>                                │
│    Current user: <user running the test>                                    │
│                                                                             │
│ ✅ WHAT NEEDS TO BE CORRECTED:                                              │
│    Option A: Change permissions                                             │
│      chmod <permissions> /path/to/file                                      │
│      Example: chmod 755 /path/to/script.sh                                  │
│                                                                             │
│    Option B: Change ownership                                               │
│      chown <user>:<group> /path/to/file                                     │
│                                                                             │
│    Option C: Add user to required group                                     │
│      Contact admin to add user to group <group>                             │
│                                                                             │
│ 🔧 WHO SHOULD FIX:                                                          │
│    [ ] File owner - if they own the file                                    │
│    [ ] System admin - if system-level permission                            │
│    [ ] Infrastructure team - if test infrastructure                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### 6. Gold File Issues

#### Symptoms
```
Gold file not found
Gold file empty
Gold file mismatch for platform
```

#### Root Cause Investigation
```bash
# Check gold directories
ls -la golds.*/

# Check specific gold file
ls -la golds.linux*/log_<command>
cat golds.linux*/log_<command>

# Check platform detection
uname -a
```

#### Solution Template
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SOLUTION: GOLD FILE ISSUE                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ ❌ WHAT IS INCORRECT:                                                       │
│    Expected gold: <path to expected gold file>                              │
│    Status: <missing / empty / wrong platform>                               │
│    Platform: <linux24/linux26_64/etc>                                       │
│    Command: <command whose gold is affected>                                │
│                                                                             │
│ ✅ WHAT NEEDS TO BE CORRECTED:                                              │
│    If gold file missing:                                                    │
│      - Create gold directory: mkdir -p golds.<platform>/                    │
│      - Generate gold file by running test with correct baseline             │
│      - Copy gold from another platform if applicable                        │
│                                                                             │
│    If gold file empty:                                                      │
│      - Regenerate gold file from known-good run                             │
│      - Check if empty gold is intentional (some commands have no output)    │
│                                                                             │
│    If wrong platform:                                                       │
│      - Create platform-specific gold: golds.<correct_platform>/             │
│      - Copy and adjust from nearest platform gold                           │
│                                                                             │
│ 🔧 WHO SHOULD FIX:                                                          │
│    [ ] Testcase owner - owns gold files                                     │
│    [ ] Bucket owner - if shared testcase                                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### 7. Infrastructure Script Issues

#### Symptoms
```
Setup script failed
Wrapper script error
Pre-test hook failed
```

#### Root Cause Investigation
```bash
# Find the failing script from logs
grep -E "(\.sh|\.pl|\.tcl)" test.log

# Read the script
cat /path/to/failing_script.sh

# Check script dependencies
head -50 /path/to/script.sh | grep -E "(source|include|require)"
```

#### Solution Template
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SOLUTION: INFRASTRUCTURE SCRIPT                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ ❌ WHAT IS INCORRECT:                                                       │
│    Script: <path to failing script>                                         │
│    Line: <line number where error occurs>                                   │
│    Error: <specific error message>                                          │
│    Cause: <why the script is failing>                                       │
│                                                                             │
│ ✅ WHAT NEEDS TO BE CORRECTED:                                              │
│    If script bug:                                                           │
│      File: <script path>                                                    │
│      Line: <line>                                                           │
│      Change: <old code> → <new code>                                        │
│                                                                             │
│    If dependency missing:                                                   │
│      Install: <what to install>                                             │
│      Or set path: export PATH=<correct_path>:$PATH                          │
│                                                                             │
│    If configuration issue:                                                  │
│      Update config file: <path>                                             │
│      Change: <what to change>                                               │
│                                                                             │
│ 🔧 WHO SHOULD FIX:                                                          │
│    [ ] Infrastructure team - owns infrastructure scripts                    │
│    [ ] Testcase owner - if testcase-specific script                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### 8. Job/Resource Issues (LSF, Timeout, Memory)

#### Symptoms
```
Job killed by LSF
Out of memory
Timeout exceeded
Resource limit hit
```

#### Root Cause Investigation
```bash
# Check for killed signals
grep -i "killed\|timeout\|memory\|resource" test.log

# Check LSF logs if applicable
cat lsf.log

# Check system limits
ulimit -a
```

#### Solution Template
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SOLUTION: RESOURCE/JOB ISSUE                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ ❌ WHAT IS INCORRECT:                                                       │
│    Issue type: <timeout / memory / killed>                                  │
│    Resource limit: <current limit>                                          │
│    Resource needed: <estimated requirement>                                 │
│    Where configured: <Makefile / LSF config / system>                       │
│                                                                             │
│ ✅ WHAT NEEDS TO BE CORRECTED:                                              │
│    If timeout:                                                              │
│      - Increase timeout in Makefile/job config                              │
│      - Current: <current timeout>                                           │
│      - Recommended: <new timeout>                                           │
│                                                                             │
│    If memory:                                                               │
│      - Request more memory in LSF: #BSUB -M <memory>                        │
│      - Or optimize testcase to use less memory                              │
│                                                                             │
│    If killed by admin:                                                      │
│      - Check with IT why job was killed                                     │
│      - May need to run in different queue/time                              │
│                                                                             │
│ 🔧 WHO SHOULD FIX:                                                          │
│    [ ] Testcase owner - adjust resource requests                            │
│    [ ] IT admin - if system limit too restrictive                           │
│    [ ] Infrastructure team - if common config issue                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Output Format for SETUP ISSUE

When reporting a SETUP ISSUE, use this enhanced format:

```markdown
## Testcase Analysis Report

**Path**: <testcase_path>
**Status**: ❌ FAILED
**Category**: ⚙️ SETUP ISSUE

---

### Failure Analysis

**Failure Point**: <Specific command/phase that failed>
**Error Type**: <Path missing / Env var / License / Makefile / Permission / etc.>

**Key Evidence**:
```
<Relevant error from logs>
```

---

### Root Cause

<Detailed explanation of WHY this is a setup issue>

**Root cause chain**:
1. <First link in chain>
2. <Second link>
3. <Final cause>

---

### 🔧 SOLUTION

#### ❌ What is Incorrect
<Specific item that is wrong - path, variable, config, etc.>

- **Location**: <File path and line number if applicable>
- **Current value**: <What it currently is>
- **Problem**: <Why this is wrong>

#### ✅ What Needs to be Corrected

**Fix Option 1** (Recommended):
```bash
<Exact command or change needed>
```

**Fix Option 2** (Alternative):
```bash
<Alternative fix if applicable>
```

#### 📍 Where to Make the Fix
- **File**: <Exact file path>
- **Line**: <Line number if applicable>
- **Change from**: <Current content>
- **Change to**: <New content>

#### 👤 Who Should Fix
- **Primary**: <Who owns this - testcase owner / infra team / IT>
- **Reason**: <Why they are responsible>

---

### Proof of Categorization

**Why this is SETUP ISSUE (not RnD bug)**:
- <Reason 1 - e.g., "The tool never got valid inputs">
- <Reason 2 - e.g., "Error is in environment, not tool logic">

**Why this is NOT REGOLD**:
- <The failure is not a valid output change>

---

### Confidence: HIGH (95%)
```

---

## Counter-Argument Checklist

Before finalizing SETUP ISSUE, verify:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│              SETUP ISSUE VERIFICATION                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ □ I have identified the SPECIFIC infrastructure/config problem              │
│ □ I have traced the problem to its SOURCE (not just symptom)                │
│ □ I have verified the DFT tool itself is NOT at fault                       │
│ □ I can explain WHAT is incorrect and WHY                                   │
│ □ I have provided a SPECIFIC fix (not just "fix the config")                │
│ □ I have identified WHO should make the fix                                 │
│                                                                             │
│ COUNTER-ARGUMENTS CONSIDERED:                                               │
│ □ Could this be a tool bug that looks like setup issue?                     │
│ □ Did the infrastructure actually work and tool mishandled it?              │
│ □ Would this work in a different environment (indicating tool issue)?       │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│ If ANY box unchecked → Investigate more before categorizing.                │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Examples

### Example 1: Missing Python Path

**Situation**: Test fails with "python: command not found"

**Analysis**:
```
❌ WHAT IS INCORRECT:
   - Makefile line 15: PYTHON = /grid/common/pkgs/python/v3.8/bin/python
   - This path does not exist on this machine
   - Available: /grid/common/pkgs/python/v3.9/bin/python

✅ WHAT NEEDS TO BE CORRECTED:
   - Edit: Makefile
   - Line 15
   - Change: PYTHON = /grid/common/pkgs/python/v3.8/bin/python
   - To: PYTHON = /grid/common/pkgs/python/v3.9/bin/python

👤 WHO SHOULD FIX: Testcase owner (hardcoded path in testcase Makefile)
```

### Example 2: Wrong Environment Variable

**Situation**: Test fails because tool can't find library

**Analysis**:
```
❌ WHAT IS INCORRECT:
   - $MODUS_HOME is set to /tools/modus/old_version
   - But tool expects libraries in /tools/modus/2024.1/lib
   - Cause: setup.sh line 42 hardcodes old version

✅ WHAT NEEDS TO BE CORRECTED:
   - Option A: Set before running test:
     export MODUS_HOME=/tools/modus/2024.1
   - Option B: Update setup.sh line 42:
     From: export MODUS_HOME=/tools/modus/old_version
     To: export MODUS_HOME=/tools/modus/2024.1

👤 WHO SHOULD FIX: Infrastructure team (common setup script)
```
