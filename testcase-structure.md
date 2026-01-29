# DFT PV Testcase Infrastructure - Complete Reference

This document provides a comprehensive reference for the DFT PV (Design for Test Product Validation) testcase infrastructure, including all files, directories, scripts, and their purposes. Use this as the primary reference when analyzing testcase structures.

---

## Table of Contents

1. [Testcase Directory Structure](#testcase-directory-structure)
2. [Key Files and Their Purpose](#key-files-and-their-purpose)
3. [Infrastructure Scripts Reference](#infrastructure-scripts-reference)
4. [Filter System](#filter-system)
5. [Gold File System](#gold-file-system)
6. [Makefile Infrastructure](#makefile-infrastructure)
7. [Modus Command Categories](#modus-command-categories)
8. [Agent Guidance: File Lookup Table](#agent-guidance-file-lookup-table)
9. [Troubleshooting Guide](#troubleshooting-guide)

---

## Testcase Directory Structure

### Standard Testcase Layout

```
<testcase_directory>/                    Example: /779947/
│
├── 📄 Makefile                          ⭐ CRITICAL - Defines TEST_TARGETS, VERIFY_TARGETS, options
│
├── 🚫 Test Control Files (Optional)
│   ├── IGNORE                           Skip testcase entirely
│   ├── IGNORE.<FEATURE>                 Skip for specific feature (e.g., IGNORE.ATPG)
│   ├── SKIP_lnx86                       Skip on Linux x86 platform
│   ├── SKIP_sun4v                       Skip on Solaris platform
│   ├── ON_lnx86                         Run ONLY on Linux x86
│   └── ON_sun4v                         Run ONLY on Solaris
│
├── 📁 src/                              Source/input files
│   ├── *.v                              Verilog design files
│   ├── *.sdc                            Timing constraints
│   ├── *.txt                            Configuration/data files
│   ├── *.sdf                            Standard delay format
│   ├── *.bsdl                           BSDL boundary scan files
│   └── hierModel*, *.lib                Technology/cell libraries
│
├── 📁 tbdata/                           ⭐ Test bench data (runtime generated)
│   ├── model/                           Compiled model data
│   ├── globalData/                      Global data store
│   └── <testmode>/                      Testmode-specific data
│
├── 📁 tbdata.org/                       Original tbdata backup (optional)
│
├── 📁 testresults/                      ⭐ All test outputs
│   ├── 📄 seq.<testmode>                Sequence output files
│   ├── 📄 TestPointInsertion.*          Test point insertion data
│   │
│   └── 📁 logs/                         ⭐ Command execution logs
│       ├── log_build_model              Output from build_model
│       ├── log_build_testmode           Output from build_testmode
│       ├── log_analyze_vectors_*        Output from analyze_vectors
│       └── log_<command>                (One log per executed command)
│
├── 📁 golds.linux24/                    Gold reference files (Linux 2.4 kernel)
│   ├── status.log                       Expected exit statuses
│   ├── license_report.log               Expected license checkout info
│   ├── readme.tsf                       Testcase specification file
│   ├── log_buildversion                 Build version info
│   └── (command logs for comparison)
│
├── 📁 golds.linux26/                    Gold files for Linux 2.6 kernel
│   └── (same structure as golds.linux24)
│
├── 📁 golds.linux26_64/                 ⭐ Gold files for 64-bit Linux (most common)
│   └── (same structure as golds.linux24)
│
├── 📁 golds.sun4v/                      Gold files for Solaris
│   └── (same structure as golds.linux24)
│
├── 📁 temp/                             Temporary working directory
│
├── 📁 extracted_defects/                Cell-aware defect data (cell_aware tests)
│
├── 📄 test.log                          ⭐ Complete execution log with timestamps
├── 📄 test.out                          ⭐ Pass/Fail status with failure details
├── 📄 status.log                        ⭐ Exit codes for all commands
├── 📄 autoTest.log                      Framework execution summary
├── 📄 runtime_statistics                Timing stats per command
├── 📄 testcase.history                  Historical pass/fail records
├── 📄 tch                               Testcase history (short form)
├── 📄 runme.tcl                         ⭐ TCL script to reproduce test (minimal)
├── 📄 runme0.tcl                        ⭐ Full TCL reproduction script
├── 📄 readme.tsf                        Testcase specification file
├── 📄 etresults                         Results file for etresults.tcl
├── 📄 run_etresults                     Etresults execution script
├── 📄 report                            Diff summary report
├── 📄 DEBUGFILE                         Debug information (parsing info)
├── 📄 license_key                       License key file (license tests)
├── 📄 lic.debug.log                     License debug log
├── 📄 license_debug_*.log               License debug per mode (diag, test, vdt)
├── 📄 license_report.log                License checkout report
│
├── 📄 *.diff.bak                        ⭐ Diff backup files (actual failures)
│   ├── status.diff.bak                  Exit status differences
│   ├── build_model.diff.bak             build_model output differences
│   └── <command>.diff.bak               Command-specific differences
│
└── 📄 abc                               Marker file (test execution marker)
```

### Release-Level Structure (Parent Directory)

```
<release_root>/etautotest/              e.g., /lan/fed/etpv/release/<ver>/lnx86/etautotest/
├── 📁 ett/                              Extended Test Targets
│   ├── 📁 <bucket_name>/                Test bucket (e.g., cell_aware_atpg, bscan)
│   │   ├── 📁 <testcase>/               Individual testcase directories
│   │   ├── 📄 bucket_owners             Maps buckets to owners
│   │   └── 📄 BUCKET.INFO               Bucket configuration
│   └── ...
│
├── 📁 misc/                             Miscellaneous tests
│   └── 📁 <category>/                   Test categories (e.g., License_Testing)
│
├── 📁 tools/                            Infrastructure tools (or $TOP)
│   ├── 📄 Makefile_root                 ⭐ Master makefile (117K+ lines)
│   ├── 📄 Makefile_root_cui             CUI mode variant
│   │
│   ├── 📁 bin/                          ⭐ 180+ executable scripts
│   │   ├── 📄 etautotest                Main test driver
│   │   ├── 📄 cdsDiff.pl                Diff engine
│   │   ├── 📄 check_tolerance.pl        Tolerance checker
│   │   └── ...
│   │
│   ├── 📁 filter/                       ⭐ 500+ filter scripts
│   │   ├── 📄 global_filter             Universal log filter
│   │   ├── 📄 modus.cmd                 TCL init script
│   │   └── 📄 <command>                 Command-specific filters
│   │
│   └── 📁 etresults/                    Results analysis system
│       ├── 📄 etresults.tcl             Main analysis engine
│       ├── 📄 call_etresults            Shell wrapper
│       └── 📁 create_html/              HTML report generation
```

---

## Key Files and Their Purpose

### 1. Status & Result Files

| File | Location | Purpose | Agent Action |
|------|----------|---------|--------------|
| **test.log** | testcase root | Complete execution log with start/end timestamps | Check for command sequence and timing |
| **test.out** | testcase root | Final PASSED/FAILED status with details | Primary source for failure categorization |
| **status.log** | testcase root | Exit codes for each command (format: `EXIT STATUS for <cmd> is <code>`) | Verify which command failed and with what code |
| **autoTest.log** | testcase root | Framework summary (Modus version, hostname, pass/fail counts) | Debug test harness/framework issues |
| **runtime_statistics** | testcase root | Build-by-build timing and status history | Check historical trends and performance |
| **testcase.history** | testcase root | Long-term historical pass/fail records with regold info | Check patterns - previously passing? |
| **tch** | testcase root | Same as testcase.history (short form) | Alternative history file |
| **runme.tcl** | testcase root | Minimal TCL script to set workdir | Starting point for reproduction |
| **runme0.tcl** | testcase root | ⭐ FULL TCL reproduction script with all commands | Use to reproduce entire test flow in modus |
| **etresults** | testcase root | Path to testcase for etresults processing | Used by results analysis system |
| **run_etresults** | testcase root | Results script output | Check results processing |
| **report** | testcase root | Human-readable diff summary report | Quick overview of differences |
| **DEBUGFILE** | testcase root | Debug info (parsed TEST_TARGETS, partdir) | Check testcase parsing issues |
| **abc** | testcase root | Test execution marker file | Indicates test was run |
| **lic.debug.log** | testcase root | Full license debugging information | Debug license-related failures |
| **license_debug_*.log** | testcase root | License debug per preference mode | Debug specific license modes |
| **license_report.log** | testcase root | License checkout sequence report | Verify license checkout order |
| **readme.tsf** | testcase root/golds | ⭐ Testcase Specification File (TSF) | Key metadata: author, testmodes, characteristics |

### 2. Diff Files (*.diff / *.diff.bak)

| File Pattern | Purpose | Agent Action |
|--------------|---------|--------------|
| **status.diff.bak** | Exit status differences | ⭐ Check FIRST - most critical |
| **<command>.diff.bak** | Output differences for specific command | Compare expected vs actual |
| **<command>.diff** | Filtered diff (noise removed) | Use for cleaner comparison |

**Diff File Format:**
```
< old_value (from .gold)
---
> new_value (actual output)
```

**Diff Priority Order** when multiple exist:
1. `status.diff.bak` - Most critical (exit status changed)
2. Files in Makefile execution order
3. Alphabetically

### 3. Log Files (testresults/logs/)

| File | Purpose | Agent Action |
|------|---------|--------------|
| **log_build_model** | Model building output | Check for design parsing errors |
| **log_build_faultmodel** | Fault model creation | Check fault injection issues |
| **log_create_logic_tests** | ATPG output | Check pattern generation |
| **log_verify_test_structures** | Structure verification | Check scan chain issues |
| **log_simulate_vectors** | Simulation results | Check simulation failures |
| **log_<command>** | Any Modus command output | General command debugging |

### 4. Gold Reference Files (golds.*/)

| Directory | Platform | When Used |
|-----------|----------|-----------|
| **golds.linux24/** | Linux 2.4 kernel (32-bit) | Legacy Linux systems |
| **golds.linux26/** | Linux 2.6+ kernel (32-bit) | Older modern Linux |
| **golds.linux26_64/** | Linux 2.6+ kernel (64-bit) | ⭐ Most common - modern Linux |
| **golds.sun4v/** | Solaris | Sun/Oracle systems |

**Gold Selection Logic:**
- Determined by `$GOLD` variable from `bin/try.pl`
- Platform auto-detected during execution based on `uname`
- 64-bit systems typically use `golds.linux26_64/`

**Gold Directory Contents:**
```
golds.linux26_64/
├── status.log              Expected exit statuses (command exit codes)
├── readme.tsf              Testcase specification with metadata
├── log_buildversion        Build version info
├── license_report.log      Expected license checkout sequence (license tests)
└── log_<command>           Expected command outputs (at root level, not in logs/)
```

**Note:** Unlike testresults/ where logs are in a `logs/` subdirectory, gold files are typically at the root of the golds directory.

### 5. Control Files

| File | Purpose | Agent Action |
|------|---------|--------------|
| **Makefile** | Test execution definition | Check TEST_TARGETS, VERIFY_TARGETS, LOCAL_*_OPTIONS |
| **IGNORE** | Skip testcase | Read contents for skip reason |
| **IGNORE.<FEATURE>** | Skip for feature | Check what feature is disabled |
| **SKIP_lnx86** | Skip on Linux | Platform-specific skip |
| **ON_lnx86** | Run only on Linux | Platform restriction |

### 6. Testcase Specification File (readme.tsf)

The `readme.tsf` file contains comprehensive metadata about each testcase:

```
# Key Fields (Example)
Testcase_Path=etautotest/<bucket>/<testcase_name>
Author=<username>
Create_date=<YYYY-MM-DD>
Top_module=<top_module_name>
Technology=<technology_name>
Customer_Testcase=yes|no
Customer=<customer_name>|na
First_Modus_Command=build_model

# Design Statistics (values are testcase-specific)
Flops=<number>
Latches=<number>
Nodes=<number>
Runtime_in_hhmmss=<HH:MM:SS>
Memory_in_GB=<float>
Max_runtime_command=<command_name>
Max_memory_command=<command_name>

# Testmodes (testcase may have 1 or more)
Testmode_1=<MODE_NAME>::Compressor=<type>,Decompressor=<type>,Masking_Type=<type>,ModeDef=<modedef>
Testmode_2=<MODE_NAME>::Compressor=na,Decompressor=na,Masking_Type=na,ModeDef=<modedef>
Compression_Ratio=<number>|na

# Characteristics (yes/no flags)
Characteristics:LSSD=no
Characteristics:1500_Wrapper=no
Characteristics:LBIST=no
Characteristics:MBIST=no
Characteristics:SDF=yes
Characteristics:Xcelium=no

# Modus Commands Used
Modus_command:build_model=yes
Modus_command:build_testmode=yes
Modus_command:create_logic_tests=yes
```

**Agent Use:** The readme.tsf provides quick insight into:
- What commands the test exercises
- Design complexity (Flops, Nodes)
- Expected runtime and memory
- Key characteristics being tested

---

## Infrastructure Scripts Reference

### Core Orchestration Scripts (bin/)

| Script | Purpose | When to Check |
|--------|---------|---------------|
| **etautotest** | Main test driver (Perl) - orchestrates entire execution | Framework issues, invocation problems |
| **try.pl** | Platform detection (lnx86/sun4v/ibmrs) | Platform mismatch issues |
| **try.sh** | Platform shell wrapper | Environment setup issues |

### License Management (bin/)

| Script | Purpose | When to Check |
|--------|---------|---------------|
| **lic_validate** | License validation | License checkout failures |
| **license_test.pl** | License testing | License availability issues |
| **license_co_sequence.pl** | License checkout sequencing | License sequencing problems |

### Verification & Diff Scripts (bin/)

| Script | Purpose | When to Check |
|--------|---------|---------------|
| **cdsDiff.pl** | ⭐ Main diff engine | Understanding diff logic, tolerance issues |
| **cdsDiff_for_modus_log.pl** | Modus log specific diff | Modus output comparison |
| **check_tolerance.pl** | ⭐ Tolerance checker | Numeric tolerance issues (default ±5%) |
| **parm_tolerance_value** | Tolerance definitions | Adjusting tolerance thresholds |
| **remove_diff.pl** | Diff cleaning | Noise removal issues |

### Reporting Scripts (bin/)

| Script | Purpose | When to Check |
|--------|---------|---------------|
| **analyze_regression** | Result analysis | Regression-level reporting |
| **cvs_Regression_report_mailer** | Email reports | Report distribution |
| **create_report.pl** | Report generation | Report formatting |
| **failureSummary.pl** | Failure summary | Quick failure overview |

### Gold Management (bin/)

| Script | Purpose | When to Check |
|--------|---------|---------------|
| **update_golds.pl** | Update gold files | Regolding process |
| **regold_testcase** | Regold testcase | Creating new baselines |

### Error Handling (bin/)

| Script | Purpose | When to Check |
|--------|---------|---------------|
| **error_core_terminate.pl** | Core dump handler | Tool crash analysis |
| **msg_help.pl** | Message help/explanation | Understanding error messages |
| **et_help.pl** | ET infrastructure help | General help |

---

## Filter System

### What Filters Do

Filters remove **non-deterministic noise** from logs before comparison:
- Timestamps and dates
- Process IDs (PIDs)
- Memory addresses
- Hostname/path variations
- Runtime statistics (if within tolerance)
- Build-specific information

### Filter Files (filter/)

| Filter | Purpose | Applied To |
|--------|---------|------------|
| **global_filter** | ⭐ Universal filter for all logs | Default for all commands |
| **global_filter_for_modus_log** | Modus-specific filtering | Modus command outputs |
| **modus.cmd** | TCL init script | Command initialization |
| **<command>** | Command-specific | Specific command outputs (500+ individual filters) |
| **gui_filter** | GUI playback | GUI-related logs |
| **license_filter** | License messages | License-related output |
| **hotspot_filter** | Hotspot analysis | Hotspot outputs |

### Filter Application Order

1. Check if `filter/<command>` exists → Use it
2. Otherwise → Use `filter/global_filter`
3. Apply to both gold and current output
4. Then run `cdsDiff.pl` comparison

---

## Gold File System

### Gold Directory Selection

```
Platform Detection: bin/try.pl
        │
        ├── Linux 2.4 kernel → golds.linux24/
        ├── Linux 2.6+ kernel → golds.linux26/
        └── Solaris → golds.sun4v/
```

### Gold File Contents

Each gold directory mirrors `testresults/`:
```
golds.linux26/
├── status.log              Expected exit statuses
└── logs/
    ├── log_build_model     Expected build_model output
    ├── log_edit_model      Expected edit_model output
    └── log_<command>       Expected command outputs
```

### Comparison Process

```
Current Output                    Gold Reference
testresults/logs/log_build_model  golds.linux26/logs/log_build_model
         │                                  │
         └──────────┬──────────────────────┘
                    │
              Apply Filter
              (global_filter or command-specific)
                    │
              cdsDiff.pl
              + check_tolerance.pl
                    │
                    ▼
              <command>.diff
              (Empty = PASS, Content = FAIL)
```

---

## Makefile Infrastructure

### Makefile_root (117K+ lines, 500+ targets)

The master makefile defines all Modus DFT command targets with standardized patterns.

#### Option Hierarchy (3 Levels)

```makefile
# Level 1: Universal options (all commands)
GLOBAL_NEWCMD_OPTIONS = log=no messagecounteach=10

# Level 2: Command-specific defaults (in Makefile_root)
GLOBAL_BUILD_MODEL_OPTIONS = messagecounteach=10 autotechlibcells=no

# Level 3: Testcase-specific overrides (in testcase/Makefile)
LOCAL_BUILD_MODEL_OPTIONS = workdir=${WORKDIR} cell=WRAPPER ...
```

**Final Command = GLOBAL_NEWCMD + LOCAL_<CMD> + GLOBAL_<CMD>**

#### Standard Target Pattern

```makefile
<command>:
    -<command> $(GLOBAL_NEWCMD_OPTIONS) \
               $(LOCAL_<COMMAND>_OPTIONS) \
               $(GLOBAL_<COMMAND>_OPTIONS) \
               > $(OUTDIR)/testresults/logs/log_<command> 2>&1 ; \
    sh -c "echo EXIT STATUS for <command> is $$? " >> $(OUTDIR)/status.log

<command>_diff:
    @$(ETDIFF) -gold $(OUTDIR)/golds.$(GOLD)/logs/log_<command> \
               -current $(OUTDIR)/testresults/logs/log_<command> \
               -filter $(FILTER) \
               -output $(OUTDIR)/<command>.diff
```

### Testcase Makefile Structure

```makefile
# Required variables
TEST_TARGETS = build_model edit_model build_faultmodel create_logic_tests
VERIFY_TARGETS = status_diff build_model_diff edit_model_diff

# Optional: Local option overrides
LOCAL_BUILD_MODEL_OPTIONS = workdir=${WORKDIR} cell=TOP ...
LOCAL_CREATE_LOGIC_TESTS_OPTIONS = faultmodel=all ...

# Include master infrastructure
include $(TOP)/Makefile_root
```

---

## Modus Command Categories

### Model Building Commands (50+)

```
build_model                    # Parse design, create model database
build_flatmodel                # Flatten hierarchical design
build_library_model            # Build technology library model
build_faultmodel               # Build stuck-at fault model
build_bridge_faultmodel        # Build bridge fault model
build_delaymodel               # Build delay fault model
build_testmode                 # Build testmode configuration
build_compression_macro        # Build compression macro
build_1500_wrapper             # Build IEEE 1500 wrapper
```

### Test Generation Commands (100+)

```
create_logic_tests             # Create combinational logic tests
create_logic_delay_tests       # Create logic delay tests (At-Speed)
create_sequential_tests        # Create sequential tests
create_path_delay_tests        # Create path delay tests
create_scanchain_tests         # Create scanchain tests
create_bridge_tests            # Create bridge tests
create_iddq_tests              # Create IDDQ tests
create_lbist_tests             # Create LBIST tests
create_diag_tests_*            # Various diagnostic test types
```

### Verification Commands (30+)

```
verify_test_structures         # Verify scan structures integrity
verify_sequences               # Verify test sequences
verify_clock_constraints       # Verify clock constraints
verify_core_isolation          # Verify core isolation
```

### Report Commands (100+)

```
report_model_statistics        # Report model statistics
report_scanchains              # Report scanchain information
report_faults                  # Report faults
report_fault_statistics        # Report fault statistics
report_vectors                 # Report vectors
```

### Diagnostic Commands (20+)

```
diagnose_failures              # Diagnose failures
diagnose_failset_logic         # Diagnose failset logic
diagnose_failset_scanchain     # Diagnose failset scanchain
analyze_diagnostics_db         # Analyze diagnostics database
```

---

## Agent Guidance: File Lookup Table

### Quick Reference: What to Check When

| Situation | Check These Files First | Then Check |
|-----------|------------------------|------------|
| **Is testcase passing?** | `test.out` | `autoTest.log` |
| **What type of failure?** | `test.out` → `*.diff.bak` files | `status.log` |
| **What command failed?** | `test.out` → Look for `Exit status diff in` or `Diff in` | `status.log` for codes |
| **What's the expected output?** | `golds.linux26_64/log_<cmd>` | Compare with `testresults/logs/log_<cmd>` |
| **What changed?** | `<command>.diff.bak` | Golden vs actual diff |
| **Did tool crash?** | Look for `core.*` files | Check logs for SIGSEGV |
| **Performance issue?** | `runtime_statistics` | Compare with gold runtime |
| **License issue?** | `lic.debug.log`, `license_report.log` | Check `license_debug_*.log` |
| **Platform issue?** | Check `SKIP_*` / `ON_*` files | Verify `$PLATFORM` value |
| **Understanding test flow?** | `Makefile` → `TEST_TARGETS` | Check command order |
| **How to reproduce?** | `runme0.tcl` | Run with `modus -f runme0.tcl` |
| **Historical status?** | `testcase.history` | Look for "PASSED AFTER REGOLD" patterns |
| **Test characteristics?** | `readme.tsf` | Testmodes, commands, design stats |

### test.out Format Reference

The `test.out` file is the primary source for understanding failures:

**PASSED Format:**
```
PASSED
```

**FAILED Formats:**

1. **Exit Status Diff** (exit code changed from gold):
```
Exit status diff in <command> (<Makefile_target>) (RD engineer: <OWNER>)
```
Example: `Exit status diff in build_model (build_model) (RD engineer: UNKNOWN)`

2. **Output Diff** (output content differs):
```
Diff in <command> (<Makefile_target>) (RD engineer: <OWNER>)
```
Example: `Diff in create_logic_tests (create_logic_tests) (RD engineer: UNKNOWN)`

3. **Core Dump**:
```
Core Dump in <command> (<Makefile_target>) (RD engineer: <OWNER>)
```

4. **Multiple Failures** (one line per failure):
```
Exit status diff in build_model (build_model) (RD engineer: UNKNOWN)
Diff in build_testmode (build_testmode) (RD engineer: UNKNOWN)
Exit status diff in verify_test_structures (verify_test_structures) (RD engineer: UNKNOWN)
```

### autoTest.log Format Reference

The `autoTest.log` provides execution summary:

```
Cadence(R) Modus(TM) DFT Software Solution, Version <version>, built <date> (<platform>)
Running directory                                                     <testcase_path>
Username                                                              <username>   
Hostname                                                              <hostname> 
PLATFORM                                                              <platform>       
Starting time                                                         <timestamp>

TESTCASE                                                        TIME            STATUS    
************************************************************************************************
.                                                               <time>          PASSED|FAILED:Due to diffs or certain target /failed

Finishing time                                                        <timestamp>
PASSED|FAILED

 Passed:    <N>
 Failed:    <N>
Ignored:    <N>
  Total:    <N>
```

### runtime_statistics Format Reference

```
      Build                     Status         MODUS Runtime  Simulation Runtime    Total Runtime     tbdata size (MB)  testresults size (MB)  Testcase size (MB)
-                               FAILED             00:00:00           NA                 00:00:00           0.0                0.0                <size>   
<version>,<date>                PASSED             <HH:MM:SS>         NA                 <HH:MM:SS>         <size>             <size>             <size>   
<version>,<date>                FAILED             <HH:MM:SS>         NA                 <HH:MM:SS>         <size>             <size>             <size>   
```

**Note:** Each row represents a different build/run. The file accumulates history over multiple runs.

### testcase.history Format Reference

```
# Format: Build           Status          SimStatus       GoldBuild               Notes
<YY.MM.MmmDD>             PASSED          NA              <YY.MM.MmmDD>           PASSED AFTER REGOLD
<YY.MM.MmmDD>             FAILED          NA              <YY.MM.MmmDD>           NO-RESPONSE
<YY.MM.MmmDD>             PASSED          NA              <YY.MM.MmmDD>           PASSED AFTER REGOLD
<YY.MM.MmmDD>             NOT-RUN         NA              <YY.MM.MmmDD>           (skipped)
```

**Example:** `21.10.Mar24` means year 2021, major version 10, March 24th.

**Key patterns:**
- `PASSED AFTER REGOLD` - Test passed after gold update (expected change)
- `NO-RESPONSE` - Test didn't complete (timeout/infrastructure issue)
- `FAILED` - Test failed comparison
- `NOT-RUN` - Test was skipped

### Exit Status Reference

| Code | Meaning | Typical Cause |
|------|---------|---------------|
| **0** | Success | Command completed normally |
| **1-4** | Warning | Non-fatal issues detected |
| **5** | Error | Explicit error in tool (most common error code) |
| **6-127** | Various errors | Tool-specific error codes |
| **128+** | Signal/Crash | Tool crashed (128+signal_number) |
| **139** | SIGSEGV (128+11) | Segmentation fault - core dump |

**Important:** Exit status 5 is very common for Modus commands. A change from 5 to 0 (or vice versa) usually indicates a significant behavioral change.

### Agent Commands for Analysis

```bash
# 1. Quick status check
cat test.out

# 2. Get framework summary
cat autoTest.log

# 3. List diff files (ordered by importance)
ls -la *.diff.bak

# 4. Check specific command exit status
cat status.log | grep <command>

# 5. Compare gold vs actual (check gold location first)
ls golds.linux*  # Find correct gold directory
diff golds.linux26_64/log_<cmd> testresults/logs/log_<cmd>

# 6. Check for core dumps
ls -la core.* 2>/dev/null

# 7. Get execution flow
grep TEST_TARGETS Makefile

# 8. Get testcase metadata
cat readme.tsf | head -30

# 9. Check historical status
tail -20 testcase.history

# 10. View diff backup content
cat <command>.diff.bak

# 11. Reproduce in modus
modus -f runme0.tcl
```

---

## Troubleshooting Guide

### Common Issues and Resolution

| Issue | Symptoms | Files to Check | Resolution |
|-------|----------|----------------|------------|
| **Core Dump** | `core.*` file exists, test.out shows "Core Dump" | `test.out`, `core.*`, failing log | REPORT TO RnD - tool crash |
| **Exit Status Change** | `status.diff.bak` shows code change | `status.log`, `test.out` | Check if expected behavior change |
| **Output Mismatch** | `<cmd>.diff.bak` has content | Gold vs actual logs | Determine if REGOLD or issue |
| **License Failure** | "License" in logs | `lic.debug.log`, `autoTest.log` | SETUP ISSUE - retry or check license server |
| **Timeout** | `test.log` shows "Interrupted" | `runtime_statistics` | SETUP ISSUE - check if LSF killed job |
| **Platform Skip** | Test skipped unexpectedly | `SKIP_*`, `ON_*` files | Verify platform requirements |
| **Missing Gold** | "No Gold" error | `golds.linux26/` directory | SETUP ISSUE - gold files missing |

### Categorization Decision Matrix

| Finding | Category | Action |
|---------|----------|--------|
| Output improved (better coverage, fewer warnings) | **REGOLD** | Update gold files |
| Output format changed (same correctness) | **REGOLD** | Update gold files |
| Missing files, wrong paths | **SETUP ISSUE** | Fix configuration |
| Permission/environment issues | **SETUP ISSUE** | Fix environment |
| Tool crashed with valid input | **REPORT TO RnD** | File bug report |
| Incorrect computation results | **REPORT TO RnD** | File bug report |
| Regression from working behavior | **REPORT TO RnD** | File bug report |

---

## Summary Tables

### File Type Quick Reference

| Extension/Pattern | Type | Purpose |
|-------------------|------|---------|
| `*.log` | Log | Command execution output |
| `*.diff` | Diff | Filtered comparison result |
| `*.diff.bak` | Diff Backup | Original comparison result |
| `*.gold` | Gold | Expected reference output |
| `*.db` | Database | Modus working data |
| `*.dofile` | Script | Modus command script |
| `*.tcl` | Config | TCL configuration |
| `core.*` | Core Dump | Tool crash dump |

### Critical Paths Summary

| What | Path |
|------|------|
| **Test Status** | `test.log`, `test.out` |
| **Command Logs** | `testresults/logs/log_<command>` |
| **Exit Codes** | `testresults/status.log` |
| **Diff Results** | `testresults/<command>.diff`, `*.diff.bak` |
| **Gold Reference** | `golds.linux26/logs/log_<command>` |
| **Test Definition** | `Makefile` (TEST_TARGETS, VERIFY_TARGETS) |
| **Infrastructure** | `Makefile_root`, `bin/*`, `filter/*` |
