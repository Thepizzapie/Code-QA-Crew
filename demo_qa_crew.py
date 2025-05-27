#!/usr/bin/env python3

"""
Demo QA Crew - Simplified version for demonstration
Includes localhost checking and basic QA functionality
"""

import os
import re
from decouple import config
from qa_tools import (
    analyze_code_structure,
    check_python_syntax,
    check_package_dependencies,
    scan_security_vulnerabilities,
    run_general_qa_tests,
    check_localhost_site
)

def sanitize_path(path: str) -> str:
    """Remove personal information from file paths for reports"""
    
    # Simple string replacement approach to avoid regex issues
    path_str = str(path)
    
    # Replace specific user path
    if 'C:\\Users\\adria\\' in path_str:
        path_str = path_str.replace('C:\\Users\\adria\\', 'C:\\Users\\[USER]\\')
    
    # Remove common personal directories
    path_str = path_str.replace('OneDrive\\Desktop\\', '')
    path_str = path_str.replace('Documents\\', '')
    path_str = path_str.replace('Downloads\\', '')
    
    # Shorten very long paths
    if len(path_str) > 60:
        parts = path_str.split('\\')
        if len(parts) > 3:
            path_str = '...\\' + '\\'.join(parts[-2:])
    
    return path_str

# Load environment variables
try:
    openai_api_key = config('OPENAI_API_KEY')
    os.environ['OPENAI_API_KEY'] = openai_api_key
    print("✅ OpenAI API Key loaded successfully")
except Exception as e:
    print(f"⚠️ Warning: Could not load OPENAI_API_KEY from .env file: {e}")

def run_demo_qa_analysis(code_path: str, project_type: str = "python", check_localhost: bool = False, port: str = "3000"):
    """
    Run a comprehensive QA analysis including optional localhost checking
    
    Args:
        code_path: Path to code to analyze
        project_type: Type of project (python, react, sql, mixed)
        check_localhost: Whether to check localhost site
        port: Port to check for localhost (default: 3000)
    """
    
    print("🔍 DEMO QA ANALYSIS STARTING")
    print("=" * 60)
    print(f"📁 Analyzing: {code_path}")
    print(f"🏷️ Project Type: {project_type}")
    if check_localhost:
        print(f"🌐 Will check localhost:{port}")
    print()
    
    # Sanitize path for report (remove personal info)
    sanitized_path = sanitize_path(code_path)
    
    report = f"""# Demo QA Analysis Report

## Project Information
- **Path**: {sanitized_path}
- **Type**: {project_type}
- **Analysis Date**: {os.popen('date /t').read().strip() if os.name == 'nt' else 'N/A'}

## Analysis Results

"""
    
    # 1. Code Structure Analysis
    print("1️⃣ Analyzing code structure...")
    try:
        structure_result = analyze_code_structure.invoke({"folder_path": code_path})
        report += f"""### 📁 Code Structure Analysis
✅ **Status**: Completed
{structure_result}

"""
        print("   ✅ Code structure analysis completed")
    except Exception as e:
        report += f"""### 📁 Code Structure Analysis
❌ **Status**: Failed - {str(e)}

"""
        print(f"   ❌ Code structure analysis failed: {e}")
    
    # 2. Python Syntax Check (if applicable)
    if project_type in ["python", "mixed"]:
        print("2️⃣ Checking Python syntax...")
        try:
            if os.path.isfile(code_path) and code_path.endswith('.py'):
                syntax_result = check_python_syntax.invoke({"code_path": code_path})
            else:
                # Find Python files in directory
                python_files = []
                if os.path.isdir(code_path):
                    for root, dirs, files in os.walk(code_path):
                        for file in files:
                            if file.endswith('.py'):
                                python_files.append(os.path.join(root, file))
                
                if python_files:
                    syntax_result = check_python_syntax.invoke({"code_path": python_files[0]})  # Check first Python file
                else:
                    syntax_result = "No Python files found to analyze"
            
            report += f"""### 🐍 Python Syntax Analysis
✅ **Status**: Completed
{syntax_result}

"""
            print("   ✅ Python syntax check completed")
        except Exception as e:
            report += f"""### 🐍 Python Syntax Analysis
❌ **Status**: Failed - {str(e)}

"""
            print(f"   ❌ Python syntax check failed: {e}")
    
    # 3. Security Scan
    print("3️⃣ Running security scan...")
    try:
        security_result = scan_security_vulnerabilities.invoke({"code_path": code_path})
        report += f"""### 🔒 Security Analysis
✅ **Status**: Completed
{security_result}

"""
        print("   ✅ Security scan completed")
    except Exception as e:
        report += f"""### 🔒 Security Analysis
❌ **Status**: Failed - {str(e)}

"""
        print(f"   ❌ Security scan failed: {e}")
    
    # 4. Package Dependencies
    print("4️⃣ Checking package dependencies...")
    try:
        deps_result = check_package_dependencies.invoke({"code_path": code_path})
        report += f"""### 📦 Dependencies Analysis
✅ **Status**: Completed
{deps_result}

"""
        print("   ✅ Dependencies check completed")
    except Exception as e:
        report += f"""### 📦 Dependencies Analysis
❌ **Status**: Failed - {str(e)}

"""
        print(f"   ❌ Dependencies check failed: {e}")
    
    # 5. General QA
    print("5️⃣ Running general QA tests...")
    try:
        qa_result = run_general_qa_tests.invoke({"code_path": code_path})
        report += f"""### 🧪 General QA Analysis
✅ **Status**: Completed
{qa_result}

"""
        print("   ✅ General QA tests completed")
    except Exception as e:
        report += f"""### 🧪 General QA Analysis
❌ **Status**: Failed - {str(e)}

"""
        print(f"   ❌ General QA tests failed: {e}")
    
    # 6. Localhost Check (if requested)
    if check_localhost:
        print(f"6️⃣ Checking localhost:{port}...")
        try:
            localhost_result = check_localhost_site.invoke({"port": port, "path": "/"})
            report += f"""### 🌐 Localhost Site Check
✅ **Status**: Completed
{localhost_result}

"""
            print(f"   ✅ Localhost:{port} check completed")
        except Exception as e:
            report += f"""### 🌐 Localhost Site Check
❌ **Status**: Failed - {str(e)}

"""
            print(f"   ❌ Localhost:{port} check failed: {e}")
    
    # Summary
    report += f"""## 📊 Summary

This analysis provides a comprehensive overview of your {project_type} project.
All available QA tools have been executed to assess code quality, security, and structure.

"""
    
    if check_localhost:
        report += f"""### 🌐 Demo Site Status
Your demo site on port {port} has been checked for accessibility and performance.

"""
    
    report += """### 💡 Next Steps
1. Review the detailed analysis results above
2. Address any security or quality issues identified
3. Consider implementing recommended improvements
4. Use this analysis for code review and quality assurance

---
*Generated by Demo QA Crew - Code Quality Analysis System*
"""
    
    print("\n📊 ANALYSIS COMPLETE!")
    print("=" * 60)
    
    # Save report
    report_filename = f"demo_qa_report_{project_type}.md"
    with open(report_filename, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"📄 Report saved to: {report_filename}")
    
    return report

def demo_localhost_check(port: str = "3000"):
    """Quick demo of localhost checking"""
    
    print(f"🌐 DEMO: Checking localhost:{port}")
    print("=" * 40)
    
    try:
        result = check_localhost_site.invoke({"port": port, "path": "/"})
        print(result)
        return result
    except Exception as e:
        error_msg = f"❌ Failed to check localhost:{port} - {str(e)}"
        print(error_msg)
        return error_msg

if __name__ == "__main__":
    print("🚀 DEMO QA CREW - READY FOR TESTING!")
    print("=" * 60)
    
    # Demo: Analyze current project
    print("\n🔍 DEMO: Project Analysis")
    current_dir = os.getcwd()
    run_demo_qa_analysis(current_dir, "python", check_localhost=False, port="3000")
    
    print("\n✅ DEMO COMPLETE!")
    print("🎯 Your QA system is ready for demonstration!") 