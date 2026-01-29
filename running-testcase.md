# Running a Testcase

Rules and requirements for running/rerunning a testcase.

## Pre-Run Checklist

### 1. Verify Build is Invoked

**Always check if the Modus build is invoked before running.**

Run `tbver` to verify:

```bash
tbver
```

Expected output:
```
Cadence(R) Modus(TM) DFT Software Solution, Version 26.10-d351_1, built Jan 27 2026 (linux26_64)
```

If `tbver` fails or shows no output, the build is NOT invoked. See [running_modus.md](running_modus.md) to invoke the build first.

### 2. Verify User

**Always run testcases as user `etadmin`.**

Check current user:
```bash
whoami
```

If not `etadmin`, switch user before proceeding.

## Running Methods

### Full Testcase Run

Use the etautotest script:
```bash
/lan/fed/etpv/src/tools/bin/etautotest
```

### Partial Run (From Middle)

Use `tbdata` with command targets to run specific parts of the testcase flow.

This is useful when:
- Debugging a specific step
- Rerunning after fixing an issue
- Skipping already-completed steps

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `tbver` not found | Build not invoked | Run `setmodus` first |
| Permission denied | Wrong user | Switch to `etadmin` |
| Testcase hangs | Various | Check logs, verify setup |
