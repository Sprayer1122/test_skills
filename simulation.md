# Simulation Failure Analysis

## What is a Simulation Failure?

A simulation failure occurs when there's an issue in the simulation part of the testcase. This typically involves logic simulation, fault simulation, or pattern verification.

## Identification

- **Reason**: `Simulation`
- **Reason 2**: `diff`
- Look for simulation-related logs and outputs

## Analysis Steps

1. **Identify the simulation type**:
   - Logic simulation
   - Fault simulation
   - Pattern simulation
   - ATPG simulation

2. **Find simulation logs**:
   ```bash
   ls -la *sim*.log *fault*.log
   ```

3. **Examine the diff.bak file**:
   - What simulation output differs?
   - Coverage numbers?
   - Pattern results?
   - Fault detection?

4. **Check simulation inputs**:
   - Verify netlist is correct
   - Check pattern files
   - Verify fault list

5. **Compare results**:
   - What was expected?
   - What was produced?
   - Quantify the difference

## Common Causes

- Netlist changes affecting simulation
- Pattern changes
- Fault model updates
- Algorithm improvements
- Timing/noise variations

## Categorization Decision Tree

1. **Are simulation differences within tolerance?** → REGOLD
   - Minor coverage variations (noise)
   - Improved fault detection
   - Expected algorithm changes

2. **Is simulation failing due to setup?** → SETUP ISSUE
   - Missing input files
   - Wrong configuration
   - Environment issues

3. **Are simulation results incorrect?** → REPORT TO RnD
   - Wrong fault detection
   - Incorrect coverage calculation
   - Simulation crash/hang

## Key Metrics to Compare

| Metric | Check For |
|--------|-----------|
| Fault Coverage | Small variations may be REGOLD |
| Pattern Count | Changes may be intentional |
| Test Coverage | Should not decrease unexpectedly |
| CPU Time | Large changes may indicate issues |

## Information to Collect

1. Simulation type
2. Expected vs actual metrics
3. Input files used
4. Any error/warning messages
5. Coverage report comparison
