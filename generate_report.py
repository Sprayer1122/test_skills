#!/usr/bin/env python3
"""
Generate HTML report from JSON analysis data.
Usage: python3 generate_report.py <json_file> [output_dir]
"""

import json
import sys
import os
from datetime import datetime
import html
import random
import string

def escape_html(text):
    """Escape HTML special characters."""
    if text is None:
        return ""
    return html.escape(str(text))

def generate_report_id():
    """Generate random 8-character report ID."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def get_status_class(status):
    """Get CSS class for status."""
    return "passed" if status.upper() == "PASSED" else "failed"

def get_category_class(category):
    """Get CSS class for category."""
    cat_lower = category.lower()
    if "regold" in cat_lower:
        return "regold"
    elif "setup" in cat_lower:
        return "setup"
    else:
        return "rnd"

def get_confidence_class(confidence):
    """Get CSS class for confidence."""
    conf_lower = confidence.lower()
    if "high" in conf_lower:
        return "high"
    elif "medium" in conf_lower:
        return "medium"
    else:
        return "low"

def generate_files_list(files):
    """Generate HTML list items for files."""
    if not files:
        return "<li>No files recorded</li>"
    return "\n".join(f"<li>{escape_html(f)}</li>" for f in files)

def generate_reasoning_chain(steps):
    """Generate HTML list items for reasoning chain."""
    if not steps:
        return "<li>No reasoning steps recorded</li>"
    return "\n".join(f"<li>{escape_html(step)}</li>" for step in steps)

def generate_evidence_rows(evidence):
    """Generate HTML table rows for evidence."""
    if not evidence:
        return "<tr><td colspan='4'>No evidence recorded</td></tr>"
    rows = []
    for i, e in enumerate(evidence, 1):
        rows.append(f"""<tr>
            <td>{i}</td>
            <td>{escape_html(e.get('source', 'N/A'))}</td>
            <td><code>{escape_html(e.get('content', 'N/A'))}</code></td>
            <td>{escape_html(e.get('proves', 'N/A'))}</td>
        </tr>""")
    return "\n".join(rows)

def generate_html(data):
    """Generate full HTML report from data dictionary."""
    
    # Set defaults
    report_id = generate_report_id()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Extract data with defaults
    testcase_name = data.get('testcase_name', 'Unknown')
    testcase_path = data.get('testcase_path', 'Unknown')
    status = data.get('status', 'FAILED')
    category = data.get('category', 'Unknown')
    confidence = data.get('confidence', 'LOW')
    rd_engineer = data.get('rd_engineer', 'N/A')
    bucket_owner = data.get('bucket_owner', 'N/A')
    purpose = data.get('purpose', 'N/A')
    test_targets = data.get('test_targets', 'N/A')
    testmodes = data.get('testmodes', 'N/A')
    failure_point = data.get('failure_point', 'N/A')
    error_type = data.get('error_type', 'N/A')
    failing_command = data.get('failing_command', 'N/A')
    exit_status = data.get('exit_status', 'N/A')
    expected_behavior = data.get('expected_behavior', 'N/A')
    actual_behavior = data.get('actual_behavior', 'N/A')
    key_evidence = data.get('key_evidence', 'No evidence recorded')
    root_cause = data.get('root_cause', 'N/A')
    execution_phase = data.get('execution_phase', 'N/A')
    reasoning_chain = data.get('reasoning_chain', [])
    files_examined = data.get('files_examined', [])
    evidence = data.get('evidence', [])
    next_steps = data.get('next_steps', 'N/A')
    iterations = data.get('iterations', '1')
    uncertainty = data.get('uncertainty', 'None')
    duration = data.get('duration', 'N/A')
    
    # Solution data (for SETUP ISSUE)
    solution = data.get('solution', {})
    incorrect_item = solution.get('item', 'N/A')
    incorrect_location = solution.get('location', 'N/A')
    current_value = solution.get('current_value', 'N/A')
    problem_desc = solution.get('problem', 'N/A')
    fix_command = solution.get('fix_command', 'N/A')
    fix_file = solution.get('fix_file', 'N/A')
    fix_line = solution.get('fix_line', 'N/A')
    old_value = solution.get('old_value', 'N/A')
    new_value = solution.get('new_value', 'N/A')
    fix_owner = solution.get('owner', 'N/A')
    fix_reason = solution.get('reason', 'N/A')
    
    # Determine visibility of solution section
    show_solution = "setup" in category.lower()
    solution_display = "" if show_solution else "display:none;"
    
    html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Testcase Analysis Report - {escape_html(testcase_name)}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f5f5; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: white; padding: 30px; border-radius: 10px 10px 0 0; }}
        .header h1 {{ font-size: 24px; margin-bottom: 10px; }}
        .header .meta {{ display: flex; gap: 20px; flex-wrap: wrap; font-size: 14px; opacity: 0.9; }}
        .status-badge {{ display: inline-block; padding: 5px 15px; border-radius: 20px; font-weight: bold; font-size: 14px; }}
        .status-passed {{ background: #00c853; color: white; }}
        .status-failed {{ background: #ff1744; color: white; }}
        .category-badge {{ display: inline-block; padding: 5px 15px; border-radius: 20px; font-weight: bold; font-size: 14px; margin-left: 10px; }}
        .category-regold {{ background: #4caf50; color: white; }}
        .category-setup {{ background: #ff9800; color: white; }}
        .category-rnd {{ background: #f44336; color: white; }}
        .content {{ background: white; padding: 30px; border-radius: 0 0 10px 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .section {{ margin-bottom: 30px; }}
        .section h2 {{ color: #1a1a2e; font-size: 18px; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 2px solid #e0e0e0; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
        th, td {{ padding: 12px 15px; text-align: left; border-bottom: 1px solid #e0e0e0; }}
        th {{ background: #f8f9fa; color: #1a1a2e; font-weight: 600; }}
        tr:hover {{ background: #f5f5f5; }}
        .evidence-box {{ background: #f8f9fa; border: 1px solid #e0e0e0; border-radius: 5px; padding: 15px; margin: 10px 0; font-family: 'Courier New', monospace; font-size: 13px; white-space: pre-wrap; overflow-x: auto; }}
        .solution-box {{ background: #e8f5e9; border: 1px solid #4caf50; border-radius: 5px; padding: 20px; margin: 10px 0; }}
        .solution-box h3 {{ color: #2e7d32; margin-bottom: 10px; }}
        .fix-code {{ background: #1a1a2e; color: #00ff00; padding: 15px; border-radius: 5px; font-family: 'Courier New', monospace; margin: 10px 0; white-space: pre-wrap; }}
        .confidence {{ display: inline-block; padding: 3px 10px; border-radius: 3px; font-weight: bold; }}
        .confidence-high {{ background: #c8e6c9; color: #2e7d32; }}
        .confidence-medium {{ background: #fff3e0; color: #e65100; }}
        .confidence-low {{ background: #ffcdd2; color: #c62828; }}
        .files-list {{ list-style: none; }}
        .files-list li {{ padding: 5px 0; border-bottom: 1px solid #eee; }}
        .files-list li:before {{ content: "📄 "; }}
        .reasoning-chain {{ background: #fff8e1; border-left: 4px solid #ffc107; padding: 15px; margin: 10px 0; }}
        .reasoning-chain ol {{ margin-left: 20px; }}
        .reasoning-chain li {{ margin: 8px 0; }}
        footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
        code {{ background: #f0f0f0; padding: 2px 6px; border-radius: 3px; font-family: 'Courier New', monospace; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📋 Testcase Analysis Report</h1>
            <div class="meta">
                <span>📅 Generated: {now}</span>
                <span>🔍 Analyzed by: Modus CLI Agent</span>
            </div>
        </div>
        
        <div class="content">
            <!-- Basic Info Section -->
            <div class="section">
                <h2>📌 Basic Information</h2>
                <table>
                    <tr><th style="width:200px">Testcase Name</th><td>{escape_html(testcase_name)}</td></tr>
                    <tr><th>Full Path</th><td><code>{escape_html(testcase_path)}</code></td></tr>
                    <tr><th>Status</th><td><span class="status-badge status-{get_status_class(status)}">{escape_html(status)}</span></td></tr>
                    <tr><th>Category</th><td><span class="category-badge category-{get_category_class(category)}">{escape_html(category)}</span></td></tr>
                    <tr><th>Confidence</th><td><span class="confidence confidence-{get_confidence_class(confidence)}">{escape_html(confidence)}</span></td></tr>
                    <tr><th>RD Engineer</th><td>{escape_html(rd_engineer)}</td></tr>
                    <tr><th>Bucket Owner</th><td>{escape_html(bucket_owner)}</td></tr>
                </table>
            </div>

            <!-- Testcase Overview Section -->
            <div class="section">
                <h2>📝 Testcase Overview</h2>
                <table>
                    <tr><th style="width:200px">Purpose</th><td>{escape_html(purpose)}</td></tr>
                    <tr><th>Commands Executed</th><td><code>{escape_html(test_targets)}</code></td></tr>
                    <tr><th>Testmodes/Features</th><td>{escape_html(testmodes)}</td></tr>
                </table>
            </div>

            <!-- Failure Analysis Section -->
            <div class="section">
                <h2>❌ Failure Analysis</h2>
                <table>
                    <tr><th style="width:200px">Failure Point</th><td>{escape_html(failure_point)}</td></tr>
                    <tr><th>Error Type</th><td>{escape_html(error_type)}</td></tr>
                    <tr><th>Failing Command</th><td><code>{escape_html(failing_command)}</code></td></tr>
                    <tr><th>Exit Status</th><td>{escape_html(exit_status)}</td></tr>
                </table>
                
                <h3 style="margin-top:20px; color:#666;">Expected vs Actual</h3>
                <table>
                    <tr><th style="width:100px">Expected</th><td>{escape_html(expected_behavior)}</td></tr>
                    <tr><th>Actual</th><td>{escape_html(actual_behavior)}</td></tr>
                </table>

                <h3 style="margin-top:20px; color:#666;">Key Evidence</h3>
                <div class="evidence-box">{escape_html(key_evidence)}</div>
            </div>

            <!-- Root Cause Section -->
            <div class="section">
                <h2>🔍 Root Cause Analysis</h2>
                <table>
                    <tr><th style="width:200px">Root Cause</th><td>{escape_html(root_cause)}</td></tr>
                    <tr><th>Execution Phase</th><td>{escape_html(execution_phase)}</td></tr>
                </table>
                
                <h3 style="margin-top:20px; color:#666;">Reasoning Chain</h3>
                <div class="reasoning-chain">
                    <ol>
                        {generate_reasoning_chain(reasoning_chain)}
                    </ol>
                </div>
            </div>

            <!-- Solution Section (For SETUP ISSUE) -->
            <div class="section" style="{solution_display}">
                <h2>🔧 Solution</h2>
                <div class="solution-box">
                    <h3>❌ What is Incorrect</h3>
                    <table>
                        <tr><th style="width:150px">Item</th><td>{escape_html(incorrect_item)}</td></tr>
                        <tr><th>Location</th><td><code>{escape_html(incorrect_location)}</code></td></tr>
                        <tr><th>Current Value</th><td><code>{escape_html(current_value)}</code></td></tr>
                        <tr><th>Problem</th><td>{escape_html(problem_desc)}</td></tr>
                    </table>
                    
                    <h3 style="margin-top:20px;">✅ What Needs to be Corrected</h3>
                    <div class="fix-code">{escape_html(fix_command)}</div>
                    
                    <h3 style="margin-top:20px;">📍 Where to Fix</h3>
                    <table>
                        <tr><th style="width:150px">File</th><td><code>{escape_html(fix_file)}</code></td></tr>
                        <tr><th>Line</th><td>{escape_html(fix_line)}</td></tr>
                        <tr><th>Change</th><td><code>{escape_html(old_value)}</code> → <code>{escape_html(new_value)}</code></td></tr>
                    </table>
                    
                    <h3 style="margin-top:20px;">👤 Who Should Fix</h3>
                    <table>
                        <tr><th style="width:150px">Owner</th><td>{escape_html(fix_owner)}</td></tr>
                        <tr><th>Reason</th><td>{escape_html(fix_reason)}</td></tr>
                    </table>
                </div>
            </div>

            <!-- Files Examined Section -->
            <div class="section">
                <h2>📁 Files Examined</h2>
                <ul class="files-list">
                    {generate_files_list(files_examined)}
                </ul>
            </div>

            <!-- Proof Section -->
            <div class="section">
                <h2>📋 Proof of Categorization</h2>
                <table>
                    <tr><th style="width:50px">#</th><th style="width:150px">Source</th><th>Evidence</th><th>What it Proves</th></tr>
                    {generate_evidence_rows(evidence)}
                </table>
            </div>

            <!-- Next Steps Section -->
            <div class="section">
                <h2>➡️ Next Steps</h2>
                <div class="evidence-box">{escape_html(next_steps)}</div>
            </div>

            <!-- Reflection Summary -->
            <div class="section">
                <h2>📊 Analysis Summary</h2>
                <table>
                    <tr><th style="width:200px">Confidence Level</th><td><span class="confidence confidence-{get_confidence_class(confidence)}">{escape_html(confidence)}</span></td></tr>
                    <tr><th>Iterations Performed</th><td>{escape_html(iterations)}</td></tr>
                    <tr><th>Remaining Uncertainty</th><td>{escape_html(uncertainty)}</td></tr>
                    <tr><th>Analysis Duration</th><td>{escape_html(duration)}</td></tr>
                </table>
            </div>
        </div>
        
        <footer>
            <p>Generated by Modus CLI Agent - Testcase Analysis Skill</p>
            <p>Report ID: {report_id} | {now}</p>
        </footer>
    </div>
</body>
</html>'''
    
    return html_template

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 generate_report.py <json_file> [output_dir]")
        print("\nExample JSON structure:")
        print(json.dumps({
            "testcase_name": "my_testcase",
            "testcase_path": "/path/to/testcase",
            "status": "FAILED",
            "category": "SETUP ISSUE",
            "confidence": "HIGH",
            "root_cause": "Typo in Makefile",
            "solution": {
                "item": "Makefile typo",
                "location": "Makefile:42",
                "fix_command": "sed -i 's/old/new/' Makefile"
            }
        }, indent=2))
        sys.exit(1)
    
    json_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(json_file)
    
    # Read JSON data
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        sys.exit(1)
    
    # Generate HTML
    html_content = generate_html(data)
    
    # Generate output filename
    testcase_name = data.get('testcase_name', 'unknown').replace('/', '_').replace(' ', '_')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"report_{testcase_name}_{timestamp}.html")
    
    # Write HTML file
    try:
        with open(output_file, 'w') as f:
            f.write(html_content)
        print(f"✅ Report generated: {output_file}")
    except Exception as e:
        print(f"Error writing HTML file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
