#!/grid/common/pkgs/python/v3.12.7/bin/python3
"""
Testcase Analysis Script

Analyzes a DFT PV testcase directory and extracts key information:
- Pass/Fail status
- Failure reason and failing command
- RD Engineer
- Bucket owner and reviewer
- CCR information
- Diff files
- Runtime statistics

Usage:
    python analyze_testcase.py <testcase_path>
    python analyze_testcase.py /lan/fed/etpv/release/261/lnx86/etautotest/sanity/...

Output: JSON format with all extracted testcase data
"""

import os
import sys
import re
import json
import subprocess
from datetime import datetime

#########################################
# Constants
#########################################
BUCKET_OWNERS_FILE = "/lan/fed/etpv/scripts/bucket_owners"

#########################################
# Test Data Extraction Functions
#########################################

def parse_test_out(testcase):
    """
    Parse test.out file to get pass/fail status and failure details.
    
    Returns dict with:
        - status: Pass/Fail/NOTRUN
        - failure_reason: Primary failure reason
        - failure_reason_2: Secondary failure reason
        - failing_command: Command that failed
        - rd_engineer: RD engineer name
        - version_line: Version info from test.out
    """
    result = {
        'status': 'NOTRUN',
        'failure_reason': 'NOTRUN',
        'failure_reason_2': 'NOTRUN',
        'failing_command': 'NOTRUN',
        'rd_engineer': 'Unknown',
        'version_line': None
    }
    
    test_out = os.path.join(testcase, 'test.out')
    
    if not os.path.isfile(test_out):
        return result
    
    with open(test_out, encoding='latin1') as f:
        lines = [line.strip() for line in f.readlines()]
    
    final_status = None
    
    # First pass: collect failure details and version
    for line in lines:
        # Extract version line
        version_match = re.search(r'(Version [\d\.\-\w]+, built \w+ \d+ \d+ \([^)]+\))', line, re.I)
        if version_match:
            result['version_line'] = version_match.group(1)
        
        # Parse failure reason: "reason in/by command...RD engineer: name"
        match = re.match(r'(.*) (in|by) (\w+).*RD engineer: (\w+)', line, re.M | re.I)
        if match and result['status'] == 'NOTRUN':
            match2 = re.search(r'(.*) (.*|diff)', match.group(1), re.M | re.I)
            if match2:
                result['status'] = 'Fail'
                result['failure_reason'] = match2.group(1)
                result['failure_reason_2'] = re.sub(r'core.*', 'core', match2.group(2))
                result['failing_command'] = match.group(3)
                result['rd_engineer'] = match.group(4)
    
    # Second pass: determine final status
    for line in lines:
        if re.match(r'Passed', line, re.I):
            final_status = 'Pass'
            break
        if re.match(r'Ignored', line, re.I):
            final_status = 'Pass'
            break
        if re.match(r'Failed', line, re.I):
            final_status = 'Fail'
            break
    
    # Apply final status
    if final_status == 'Pass':
        result['status'] = 'Pass'
        if result['failure_reason'] == 'NOTRUN':
            result['failure_reason'] = 'Pass'
            result['failure_reason_2'] = 'Pass'
            result['failing_command'] = 'Pass'
    elif final_status == 'Fail' and result['status'] == 'NOTRUN':
        diff_files = find_diff_bak_files(testcase)
        if diff_files:
            result['status'] = 'Fail'
            result['failure_reason'] = 'Other Diffs'
            result['failure_reason_2'] = 'Diff.Bak'
            result['failing_command'] = diff_files[0]
        else:
            log_status = parse_test_log(testcase)
            if log_status == 'Killed':
                result['status'] = 'Fail'
                result['failure_reason'] = 'Other Diffs'
                result['failure_reason_2'] = 'Interrupted-LSF' if check_makefile_for_lsf(testcase) else 'Interrupted'
                result['failing_command'] = 'Other Diffs'
            else:
                result['status'] = 'Fail'
                result['failure_reason'] = 'Other Diffs'
                result['failure_reason_2'] = 'Other Diffs'
                result['failing_command'] = 'Other Diffs'
    
    return result


def parse_test_log(testcase):
    """
    Parse test.log file to get test status.
    Returns: 'Pass', 'Fail', 'Killed', or 'No'
    """
    test_log = os.path.join(testcase, 'test.log')
    
    if not os.path.isfile(test_log):
        return 'No'
    
    with open(test_log, encoding='latin1') as f:
        lines = f.readlines()
        for line in reversed(lines):
            line = line.strip()
            if re.search(r'Testcase passed', line, re.I):
                return 'Pass'
            if re.search(r'Testcase Failed', line, re.I):
                return 'Fail'
            if re.search(r'Interrupted', line, re.I):
                return 'Killed'
    
    return 'No'


def parse_testcase_history(testcase):
    """
    Parse testcase.history file to get CCR info.
    Returns dict with ccr_number and already_ccr
    """
    result = {
        'ccr_number': 'No',
        'already_ccr': 'No'
    }
    
    testcase_history = os.path.join(testcase, 'testcase.history')
    
    if not os.path.isfile(testcase_history):
        return result
    
    with open(testcase_history, encoding='latin1') as f:
        lines = f.readlines()
        for line in reversed(lines):
            line = line.strip()
            line = re.sub('NOT-RUN', 'NOTRUN', line)
            
            # Get the most recent CCR info
            match = re.search(r'(\w+)\s+(\w+)\s+([\w,]+).*', line, re.I)
            if match:
                result['already_ccr'] = match.group(3)
                break
    
    if result['already_ccr'] == 'NA':
        result['already_ccr'] = 'No'
    
    return result


def get_bucket_owner(testcase):
    """
    Identify bucket owner and reviewer from testcase path.
    Returns dict with owner and reviewer
    """
    result = {
        'owner': 'Unknown',
        'reviewer': 'Unknown'
    }
    
    if not os.path.isfile(BUCKET_OWNERS_FILE):
        return result
    
    with open(BUCKET_OWNERS_FILE, encoding='latin1') as f:
        for line in f:
            line = line.strip()
            if not line or '|' not in line:
                continue
            
            parts = re.split(r"\|", line, 1)
            bucket = parts[0]
            owners = re.split(",", parts[1], 1)
            
            if re.search(f'etautotest/{bucket}', testcase, re.I):
                result['owner'] = owners[0]
                result['reviewer'] = owners[1] if len(owners) > 1 else owners[0]
                break
    
    return result


def find_diff_bak_files(testcase):
    """
    Find diff.bak files in testcase directory.
    Returns list of diff.bak filenames in order of priority.
    """
    diff_files = []
    
    if not os.path.isdir(testcase):
        return diff_files
    
    # Priority 1: status.diff.bak
    status_diff = os.path.join(testcase, 'status.diff.bak')
    if os.path.exists(status_diff):
        diff_files.append('status.diff.bak')
    
    # Priority 2: makefile execution order
    makefile_order = get_makefile_order(testcase)
    for filename in makefile_order:
        if filename.endswith('.diff.bak') and filename not in diff_files:
            diff_files.append(filename)
    
    # Priority 3: remaining diff.bak files (alphabetical)
    try:
        for filename in sorted(os.listdir(testcase)):
            if filename.endswith('.diff.bak') and filename not in diff_files:
                diff_files.append(filename)
    except Exception:
        pass
    
    return diff_files


def get_makefile_order(testcase):
    """
    Get testcase logs order from makefile execution.
    Returns list of filenames in execution order.
    """
    makefile_path = os.path.join(testcase, 'Makefile')
    if not os.path.exists(makefile_path):
        makefile_path = os.path.join(testcase, 'makefile')
    
    if not os.path.exists(makefile_path):
        return []
    
    try:
        original_cwd = os.getcwd()
        os.chdir(testcase)
        
        try:
            result = subprocess.run(['make', '-n'], 
                                    capture_output=True, 
                                    text=True, 
                                    timeout=30)
            
            if result.returncode != 0:
                return []
            
            ordered_files = []
            for line in result.stdout.split('\n'):
                line = line.strip()
                if ('testresults/logs' in line or 'testresults' in line) and line.endswith('>'):
                    for part in line.split():
                        if 'testresults/logs/' in part:
                            filename = part.replace('testresults/logs/', '').rstrip('>').strip()
                            if filename:
                                ordered_files.append(filename)
                                break
            
            return ordered_files
        finally:
            os.chdir(original_cwd)
    except Exception:
        return []


def check_makefile_for_lsf(testcase):
    """
    Check if Makefile contains LSF or subprocess keywords.
    """
    makefile_path = os.path.join(testcase, 'Makefile')
    if not os.path.exists(makefile_path):
        makefile_path = os.path.join(testcase, 'makefile')
    
    if not os.path.exists(makefile_path):
        return False
    
    try:
        with open(makefile_path, 'r') as f:
            content = f.read().lower()
            return 'lsf' in content or 'subprocess' in content
    except Exception:
        return False


def get_gold_runtime(testcase):
    """
    Parse runtime_statistics file to get gold runtime.
    Returns runtime string (HH:MM:SS)
    """
    file_path = os.path.join(testcase, 'runtime_statistics')
    
    if not os.path.isfile(file_path):
        return '00:00:00'
    
    try:
        with open(file_path) as f:
            lines = f.readlines()
            if len(lines) < 2:
                return '00:00:00'
            
            target_line = lines[1]
            for line in lines:
                if re.search(r'PASSED', line, re.I):
                    target_line = line
            
            parts = re.split(r"\s+", target_line.strip())
            return parts[4] if len(parts) > 4 else '00:00:00'
    except Exception:
        return '00:00:00'


def list_key_files(testcase):
    """
    List important files in the testcase directory for analysis.
    """
    key_files = {
        'exists': [],
        'diff_bak_files': [],
        'log_files': [],
        'gold_files': []
    }
    
    if not os.path.isdir(testcase):
        return key_files
    
    try:
        for filename in os.listdir(testcase):
            filepath = os.path.join(testcase, filename)
            
            if filename in ['test.out', 'test.log', 'Makefile', 'makefile', 
                           'testcase.history', 'runtime_statistics']:
                key_files['exists'].append(filename)
            elif filename.endswith('.diff.bak'):
                key_files['diff_bak_files'].append(filename)
            elif filename.endswith('.log'):
                key_files['log_files'].append(filename)
            elif filename.endswith('.gold') or filename.endswith('.gld'):
                key_files['gold_files'].append(filename)
    except Exception:
        pass
    
    return key_files


def analyze_testcase(testcase_path):
    """
    Main function to analyze a testcase and return all extracted data.
    """
    # Normalize path
    testcase_path = os.path.abspath(testcase_path)
    
    # Check if path exists
    if not os.path.isdir(testcase_path):
        return {
            'error': f'Testcase directory does not exist: {testcase_path}',
            'testcase_path': testcase_path
        }
    
    # Extract all data
    test_out_data = parse_test_out(testcase_path)
    test_log_status = parse_test_log(testcase_path)
    history_data = parse_testcase_history(testcase_path)
    owner_data = get_bucket_owner(testcase_path)
    diff_files = find_diff_bak_files(testcase_path)
    gold_runtime = get_gold_runtime(testcase_path)
    key_files = list_key_files(testcase_path)
    
    # Handle killed status
    if test_log_status == 'Killed':
        test_out_data['status'] = 'Killed'
        test_out_data['failure_reason'] = 'Killed'
        test_out_data['failure_reason_2'] = 'Interrupted'
        test_out_data['failing_command'] = 'Killed'
    
    # Build result
    result = {
        'testcase_path': testcase_path,
        'testcase_name': os.path.basename(testcase_path),
        'bucket': extract_bucket(testcase_path),
        'analysis_time': datetime.now().isoformat(),
        
        # Status info
        'status': test_out_data['status'],
        'test_log_status': test_log_status,
        
        # Failure details
        'failure_reason': test_out_data['failure_reason'],
        'failure_reason_2': test_out_data['failure_reason_2'],
        'failing_command': test_out_data['failing_command'],
        
        # People
        'rd_engineer': test_out_data['rd_engineer'],
        'owner': owner_data['owner'],
        'reviewer': owner_data['reviewer'],
        
        # Version and runtime
        'version_line': test_out_data['version_line'],
        'gold_runtime': gold_runtime,
        
        # CCR info
        'ccr_number': history_data['ccr_number'],
        'already_ccr': history_data['already_ccr'],
        
        # Files
        'diff_bak_files': diff_files,
        'key_files': key_files
    }
    
    return result


def extract_bucket(testcase_path):
    """Extract bucket name from testcase path."""
    match = re.search(r'etautotest/([^/]+)', testcase_path)
    return match.group(1) if match else 'Unknown'


def print_summary(data):
    """Print a human-readable summary of the analysis."""
    print("=" * 70)
    print("TESTCASE ANALYSIS SUMMARY")
    print("=" * 70)
    print(f"Path: {data['testcase_path']}")
    print(f"Name: {data['testcase_name']}")
    print(f"Bucket: {data['bucket']}")
    print("-" * 70)
    
    status = data['status']
    if status == 'Pass':
        print(f"Status: ✅ PASSED")
    elif status == 'Fail':
        print(f"Status: ❌ FAILED")
    elif status == 'Killed':
        print(f"Status: ⚠️  KILLED/INTERRUPTED")
    else:
        print(f"Status: ❓ {status}")
    
    print(f"Test Log Status: {data['test_log_status']}")
    print("-" * 70)
    
    if status != 'Pass':
        print("FAILURE DETAILS:")
        print(f"  Reason: {data['failure_reason']}")
        print(f"  Reason 2: {data['failure_reason_2']}")
        print(f"  Failing Command: {data['failing_command']}")
        print("-" * 70)
    
    print("OWNERSHIP:")
    print(f"  RD Engineer: {data['rd_engineer']}")
    print(f"  Bucket Owner: {data['owner']}")
    print(f"  Reviewer: {data['reviewer']}")
    print("-" * 70)
    
    print("BUILD INFO:")
    print(f"  Version: {data['version_line'] or 'Not found'}")
    print(f"  Gold Runtime: {data['gold_runtime']}")
    print("-" * 70)
    
    print("CCR INFO:")
    print(f"  Already CCR: {data['already_ccr']}")
    print(f"  CCR Number: {data['ccr_number']}")
    print("-" * 70)
    
    print("FILES:")
    print(f"  Key Files: {', '.join(data['key_files']['exists']) or 'None'}")
    print(f"  Diff.bak Files: {', '.join(data['diff_bak_files']) or 'None'}")
    print(f"  Log Files: {', '.join(data['key_files']['log_files'][:5]) or 'None'}")
    if len(data['key_files']['log_files']) > 5:
        print(f"    ... and {len(data['key_files']['log_files']) - 5} more")
    print("=" * 70)


#########################################
# MAIN
#########################################
def main():
    if len(sys.argv) < 2:
        print("Usage: analyze_testcase.py <testcase_path> [--json]")
        print("")
        print("Arguments:")
        print("  testcase_path  Path to the testcase directory")
        print("  --json         Output in JSON format (default: human-readable)")
        print("")
        print("Example:")
        print("  python analyze_testcase.py /lan/fed/etpv/release/261/lnx86/etautotest/sanity/...")
        sys.exit(1)
    
    testcase_path = sys.argv[1]
    json_output = '--json' in sys.argv
    
    result = analyze_testcase(testcase_path)
    
    if 'error' in result:
        print(f"❌ ERROR: {result['error']}")
        sys.exit(1)
    
    if json_output:
        print(json.dumps(result, indent=2, default=str))
    else:
        print_summary(result)
        print("\nFor JSON output, use: --json flag")


if __name__ == "__main__":
    main()
