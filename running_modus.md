# Invoke Modus using setmodus

**Full path**: `/home/et/tools/setmodus`

Executes Modus from various locations and builds.

## Syntax

```bash
setmodus [<release>] [<build>] [<type>] [<options>]
```

## Parameters

### Release (`-r###`)

Specifies the Modus release version:
- `-r201`
- `-r211`
- `-r261`
- etc.

### Build Type

| Flag | Description |
|------|-------------|
| `-base` | First production |
| `-daily` | Current day's build |
| `-etprod` | Latest production |
| `-isr` | Latest production (ISR) |
| `-isrtest` | Latest integration (passed RMS) |
| `-live` | Frequent incremental (~every 6 hours) |
| `-integ` | Latest integration |
| `-testlib` | Test library build |

### Dated Builds

Use `-dt` option to invoke date-specific builds:
```bash
-dtYYYYMMDD
```

### Debug/Analysis Type

| Flag | Description |
|------|-------------|
| `-debug` | Debug build |
| `-purify` | Purify build |
| `-purecov` | Purecov build |
| `-quantify` | Quantify build |

### Options

| Flag | Description |
|------|-------------|
| `-c` | Create modus shell environment for command invocation |
| `-go` | No prompt prior to execution |
| `-pathonly` | Print path to modus only |
| `-h` | Show help and additional options |

## Common Examples

### Latest ISR Test Build (Command Line)
```bash
setmodus -r211 -isrtest -c -go
```

### Latest Test Library Build
```bash
setmodus -r211 -testlib -c -go
```

### Latest Daily Build
```bash
setmodus -r211 -daily -c -go
```

### Specific Date Daily Build (Jan 05, 2022)
```bash
setmodus -r211 -daily -dt20220105 -c -go
```

### Just Get the Path
```bash
setmodus -r261 -isrtest -pathonly
```

## Quick Reference

Most common invocation for testcase analysis:
```bash
setmodus -r261 -isrtest -c -go
```

This sets up the environment for:
- Release 261
- ISR test build
- Command line mode (`-c`)
- No prompts (`-go`)
