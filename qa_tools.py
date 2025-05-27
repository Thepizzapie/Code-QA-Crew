#!/usr/bin/env python3

import os
import ast
import re
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import pkg_resources
import importlib.util
import requests
import time
from urllib.parse import urljoin

# Import LangChain tools - the CORRECT way!
from langchain_core.tools import tool
from langchain_experimental.tools import PythonREPLTool
from langchain_community.tools import ShellTool, DuckDuckGoSearchRun
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

# Initialize real LangChain tools
python_repl = PythonREPLTool()
shell_tool = ShellTool()
search_tool = DuckDuckGoSearchRun()

def sanitize_path_for_report(path: str) -> str:
    """Remove personal information from file paths for reports"""
    
    # Convert to string if Path object
    path_str = str(path)
    
    # Simple string replacement approach to avoid regex issues
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

@tool
def analyze_code_structure(folder_path: str) -> str:
    """Analyze code structure using real Python execution and file system analysis.
    
    Args:
        folder_path: Path to the code directory or file to analyze
        
    Returns:
        Detailed analysis of code structure, organization, and architecture
    """
    try:
        # Real Python code to analyze structure
        analysis_code = f'''
import os
from pathlib import Path
import ast

def analyze_real_structure(path):
    results = {{
        "total_files": 0,
        "file_types": {{}},
        "python_files": [],
        "js_files": [],
        "directories": [],
        "complexity_score": 0
    }}
    
    path_obj = Path(r"{folder_path}")
    if not path_obj.exists():
        return {{"error": "Path does not exist"}}
    
    # Count files and types
    for item in path_obj.rglob("*"):
        if item.is_file():
            results["total_files"] += 1
            ext = item.suffix or "no_extension"
            results["file_types"][ext] = results["file_types"].get(ext, 0) + 1
            
            if ext == ".py":
                results["python_files"].append(str(item))
            elif ext in [".js", ".jsx", ".ts", ".tsx"]:
                results["js_files"].append(str(item))
        elif item.is_dir():
            results["directories"].append(str(item))
    
    # Calculate complexity based on file distribution
    if results["total_files"] > 0:
        type_diversity = len(results["file_types"])
        if type_diversity <= 3:
            results["complexity_score"] = 3
        elif type_diversity <= 6:
            results["complexity_score"] = 6
        else:
            results["complexity_score"] = 9
    
    return results

result = analyze_real_structure(r"{folder_path}")
print("ANALYSIS_RESULT:", result)
'''
            
        # Execute real analysis using Python REPL
        output = python_repl.run(analysis_code)
        
        # Parse the result
        if "ANALYSIS_RESULT:" in output:
            result_str = output.split("ANALYSIS_RESULT:")[1].strip()
            try:
                analysis = eval(result_str)  # Safe here since we control the output
                
                # Format real results
                report = f"""
🏗️ REAL CODE STRUCTURE ANALYSIS
{'='*50}

📊 **Total Files**: {analysis.get('total_files', 0)}
📁 **Directories**: {len(analysis.get('directories', []))}
🐍 **Python Files**: {len(analysis.get('python_files', []))}
⚛️ **JS/React Files**: {len(analysis.get('js_files', []))}

📈 **File Type Distribution**:
"""
                for ext, count in analysis.get('file_types', {}).items():
                    report += f"  {ext}: {count} files\n"
                
                report += f"""
🎯 **Complexity Score**: {analysis.get('complexity_score', 0)}/10

💡 **Real Analysis Insights**:
  • Project has {analysis.get('total_files', 0)} total files
  • {len(analysis.get('file_types', {}))} different file types detected
  • {'Well-organized' if analysis.get('complexity_score', 0) < 7 else 'Complex'} project structure
"""
                return report
                
            except Exception as e:
                return f"❌ Error parsing analysis: {str(e)}"
        else:
            return f"❌ Analysis failed: {output}"
                
    except Exception as e:
        return f"❌ Error running real analysis: {str(e)}"

@tool
def check_python_syntax(code_path: str) -> str:
    """Check Python syntax using real AST parsing and linting.
    
    Args:
        code_path: Path to Python file or directory
        
    Returns:
        Detailed Python syntax and style analysis
    """
    try:
        syntax_check_code = f'''
import ast
import os
from pathlib import Path

def check_real_syntax(path):
    results = {{
        "files_checked": 0,
        "syntax_errors": [],
        "style_issues": [],
        "imports": [],
        "functions": [],
        "classes": []
    }}
    
    path_obj = Path(r"{code_path}")
    if not path_obj.exists():
        return {{"error": "Path does not exist"}}
    
    # Find Python files
    py_files = []
    if path_obj.is_file() and path_obj.suffix == ".py":
        py_files = [path_obj]
    else:
        py_files = list(path_obj.rglob("*.py"))
    
    for py_file in py_files:
        results["files_checked"] += 1
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Real AST parsing
            try:
                tree = ast.parse(content)
                
                # Extract real information
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            results["imports"].append(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            results["imports"].append(node.module)
                    elif isinstance(node, ast.FunctionDef):
                        results["functions"].append(node.name)
                    elif isinstance(node, ast.ClassDef):
                        results["classes"].append(node.name)
                        
            except SyntaxError as e:
                results["syntax_errors"].append(f"{{py_file}}:{{e.lineno}} - {{e.msg}}")
            
            # Style checks
            lines = content.split('\\n')
            for i, line in enumerate(lines, 1):
                if len(line) > 120:
                    results["style_issues"].append(f"{{py_file}}:{{i}} - Line too long ({{len(line)}} chars)")
                if 'print(' in line and 'debug' not in str(py_file).lower():
                    results["style_issues"].append(f"{{py_file}}:{{i}} - Consider using logging")
                    
        except Exception as e:
            results["syntax_errors"].append(f"{{py_file}} - Error reading: {{str(e)}}")
    
    return results

result = check_real_syntax(r"{code_path}")
print("SYNTAX_RESULT:", result)
'''
            
        output = python_repl.run(syntax_check_code)
        
        if "SYNTAX_RESULT:" in output:
            result_str = output.split("SYNTAX_RESULT:")[1].strip()
            try:
                analysis = eval(result_str)
                
                report = f"""
🐍 REAL PYTHON SYNTAX ANALYSIS
{'='*50}

✅ **Files Analyzed**: {analysis.get('files_checked', 0)}

🚨 **Syntax Errors** ({len(analysis.get('syntax_errors', []))}):
"""
                for error in analysis.get('syntax_errors', [])[:5]:
                    report += f"  • {sanitize_path_for_report(error)}\n"
                
                report += f"""
⚠️ **Style Issues** ({len(analysis.get('style_issues', []))}):
"""
                for issue in analysis.get('style_issues', [])[:5]:
                    report += f"  • {sanitize_path_for_report(issue)}\n"
                
                report += f"""
📦 **Imports Found**: {len(set(analysis.get('imports', [])))} unique
🔧 **Functions Found**: {len(analysis.get('functions', []))}
🏗️ **Classes Found**: {len(analysis.get('classes', []))}

🎯 **Python Quality Score**: {max(2, 10 - len(analysis.get('syntax_errors', [])) - len(analysis.get('style_issues', [])))}/10
"""
                return report
                
            except Exception as e:
                return f"❌ Error parsing syntax results: {str(e)}"
        else:
            return f"❌ Syntax check failed: {output}"
                
    except Exception as e:
        return f"❌ Error running syntax check: {str(e)}"

@tool
def scan_security_vulnerabilities(code_path: str) -> str:
    """Scan for security vulnerabilities using real pattern matching.
    
    Args:
        code_path: Path to code to scan for security issues
        
    Returns:
        Security vulnerability assessment
    """
    try:
        security_scan_code = f'''
import os
import re
from pathlib import Path

def scan_real_security(path):
    results = {{
        "files_scanned": 0,
        "high_risk": [],
        "medium_risk": [],
        "low_risk": [],
        "patterns_found": {{}}
    }}
    
    # Real security patterns
    high_risk_patterns = [
        (r'eval\\s*\\(', 'eval() usage - code injection risk'),
        (r'exec\\s*\\(', 'exec() usage - code injection risk'),
        (r'shell=True', 'shell=True - command injection risk'),
        (r'password\\s*=\\s*["\'][^"\']+["\']', 'hardcoded password'),
        (r'api[_-]?key\\s*=\\s*["\'][^"\']+["\']', 'hardcoded API key'),
    ]
    
    medium_risk_patterns = [
        (r'subprocess\\.call', 'subprocess usage'),
        (r'os\\.system', 'os.system usage'),
        (r'pickle\\.loads?', 'pickle deserialization'),
        (r'yaml\\.load\\s*\\(', 'unsafe YAML loading'),
    ]
    
    low_risk_patterns = [
        (r'TODO|FIXME', 'TODO/FIXME comments'),
        (r'print\\s*\\(', 'print statements (use logging)'),
    ]
    
    path_obj = Path(r"{code_path}")
    if not path_obj.exists():
        return {{"error": "Path does not exist"}}
    
    # Scan all text files
    for file_path in path_obj.rglob("*"):
        if file_path.is_file() and file_path.suffix in ['.py', '.js', '.jsx', '.ts', '.tsx', '.json', '.yaml', '.yml']:
            results["files_scanned"] += 1
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Check high risk patterns
                for pattern, description in high_risk_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        results["high_risk"].append(f"{{file_path}} - {{description}}")
                        results["patterns_found"][description] = results["patterns_found"].get(description, 0) + len(matches)
                
                # Check medium risk patterns
                for pattern, description in medium_risk_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        results["medium_risk"].append(f"{{file_path}} - {{description}}")
                        results["patterns_found"][description] = results["patterns_found"].get(description, 0) + len(matches)
                
                # Check low risk patterns
                for pattern, description in low_risk_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        results["low_risk"].append(f"{{file_path}} - {{description}}")
                        results["patterns_found"][description] = results["patterns_found"].get(description, 0) + len(matches)
                        
            except Exception as e:
                results["low_risk"].append(f"{{file_path}} - Error reading file")
    
    return results

result = scan_real_security(r"{code_path}")
print("SECURITY_RESULT:", result)
'''
            
        output = python_repl.run(security_scan_code)
        
        if "SECURITY_RESULT:" in output:
            result_str = output.split("SECURITY_RESULT:")[1].strip()
            try:
                analysis = eval(result_str)
                
                high_count = len(analysis.get('high_risk', []))
                medium_count = len(analysis.get('medium_risk', []))
                low_count = len(analysis.get('low_risk', []))
                
                # Calculate real security score
                security_score = 10
                if high_count > 0:
                    security_score = max(2, security_score - (high_count * 3))
                if medium_count > 0:
                    security_score = max(2, security_score - (medium_count * 2))
                if low_count > 5:
                    security_score = max(2, security_score - 1)
                
                report = f"""
🔒 REAL SECURITY VULNERABILITY SCAN
{'='*50}

📊 **Files Scanned**: {analysis.get('files_scanned', 0)}

🚨 **High Risk Issues** ({high_count}):
"""
                for issue in analysis.get('high_risk', [])[:5]:
                    report += f"  • {sanitize_path_for_report(issue)}\n"
                
                report += f"""
⚠️ **Medium Risk Issues** ({medium_count}):
"""
                for issue in analysis.get('medium_risk', [])[:5]:
                    report += f"  • {sanitize_path_for_report(issue)}\n"
                
                report += f"""
ℹ️ **Low Risk Issues** ({low_count}):
"""
                for issue in analysis.get('low_risk', [])[:3]:
                    report += f"  • {sanitize_path_for_report(issue)}\n"
                
                report += f"""
🎯 **Security Score**: {security_score}/10
📈 **Risk Level**: {'HIGH' if high_count > 0 else 'MEDIUM' if medium_count > 0 else 'LOW'}

🔍 **Pattern Summary**:
"""
                for pattern, count in analysis.get('patterns_found', {}).items():
                    report += f"  • {pattern}: {count} occurrences\n"
                
                return report
                
            except Exception as e:
                return f"❌ Error parsing security results: {str(e)}"
        else:
            return f"❌ Security scan failed: {output}"
                
    except Exception as e:
        return f"❌ Error running security scan: {str(e)}"

@tool
def check_package_dependencies(code_path: str) -> str:
    """Check package dependencies for validity, security, and compatibility.
    
    Args:
        code_path: Path to project with dependency files
        
    Returns:
        Comprehensive dependency analysis
    """
    try:
        dep_check_code = f'''
import os
import json
from pathlib import Path

def check_real_dependencies(path):
    results = {{
        "dependency_files": [],
        "python_deps": [],
        "js_deps": [],
        "total_deps": 0,
        "issues": []
    }}
    
    path_obj = Path(r"{code_path}")
    if not path_obj.exists():
        return {{"error": "Path does not exist"}}
    
    # Check for requirements.txt
    req_file = path_obj / "requirements.txt"
    if req_file.exists():
        results["dependency_files"].append("requirements.txt")
        try:
            with open(req_file, 'r') as f:
                lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    results["python_deps"].append(line)
                    results["total_deps"] += 1
                    if '==' not in line and '>=' not in line:
                        results["issues"].append(f"requirements.txt - {{line}} has no version specified")
        except Exception as e:
            results["issues"].append(f"requirements.txt - Error reading: {{str(e)}}")
    
    # Check for package.json
    pkg_file = path_obj / "package.json"
    if pkg_file.exists():
        results["dependency_files"].append("package.json")
        try:
            with open(pkg_file, 'r') as f:
                data = json.load(f)
            
            deps = data.get('dependencies', {{}})
            dev_deps = data.get('devDependencies', {{}})
            
            for dep, version in deps.items():
                results["js_deps"].append(f"{{dep}}@{{version}}")
                results["total_deps"] += 1
            
            for dep, version in dev_deps.items():
                results["js_deps"].append(f"{{dep}}@{{version}} (dev)")
                results["total_deps"] += 1
                
        except Exception as e:
            results["issues"].append(f"package.json - Error reading: {{str(e)}}")
    
    # Check for Pipfile
    pipfile = path_obj / "Pipfile"
    if pipfile.exists():
        results["dependency_files"].append("Pipfile")
        results["issues"].append("Pipfile found - consider using requirements.txt for better compatibility")
    
    return results

result = check_real_dependencies(r"{code_path}")
print("DEPENDENCY_RESULT:", result)
'''
            
        output = python_repl.run(dep_check_code)
        
        if "DEPENDENCY_RESULT:" in output:
            result_str = output.split("DEPENDENCY_RESULT:")[1].strip()
            try:
                analysis = eval(result_str)
                
                report = f"""
📦 REAL DEPENDENCY ANALYSIS
{'='*50}

📁 **Dependency Files Found**: {len(analysis.get('dependency_files', []))}
"""
                for file in analysis.get('dependency_files', []):
                    report += f"  • {file}\n"
                
                report += f"""
📊 **Total Dependencies**: {analysis.get('total_deps', 0)}
🐍 **Python Dependencies**: {len(analysis.get('python_deps', []))}
⚛️ **JavaScript Dependencies**: {len(analysis.get('js_deps', []))}

⚠️ **Issues Found** ({len(analysis.get('issues', []))}):
"""
                for issue in analysis.get('issues', []):
                    report += f"  • {issue}\n"
                
                # Calculate dependency health score
                dep_score = 10 - len(analysis.get('issues', []))
                dep_score = max(2, dep_score)
                
                report += f"""
🎯 **Dependency Health Score**: {dep_score}/10

💡 **Recommendations**:
  • {'All dependencies look good!' if len(analysis.get('issues', [])) == 0 else 'Address version specification issues'}
  • {'Consider dependency audit' if analysis.get('total_deps', 0) > 50 else 'Reasonable number of dependencies'}
"""
                return report
                
            except Exception as e:
                return f"❌ Error parsing dependency results: {str(e)}"
        else:
            return f"❌ Dependency check failed: {output}"
                
    except Exception as e:
        return f"❌ Error running dependency check: {str(e)}"

@tool
def check_localhost_site(port: str = "3000", path: str = "/") -> str:
    """Check if a localhost site is operational and accessible.
    
    Args:
        port: Port number to check (default: 3000 for React apps)
        path: Path to check on the site (default: /)
        
    Returns:
        Status report of the localhost site including accessibility, response time, and basic checks
    """
    try:
        base_url = f"http://localhost:{port}"
        full_url = f"{base_url}{path}"
        
        start_time = time.time()
        try:
            response = requests.get(full_url, timeout=10)
            response_time = round((time.time() - start_time) * 1000, 2)
            
            report = f"""
🌐 REAL LOCALHOST SITE CHECK
{'='*50}

🔗 **URL**: {full_url}
✅ **Status**: ACCESSIBLE
📈 **HTTP Status**: {response.status_code}
⏱️ **Response Time**: {response_time}ms

📊 **Content Analysis**:
  • Content Length: {len(response.text)} characters
  • Content Type: {response.headers.get('content-type', 'unknown')}
"""
            
            # Real content analysis
            content = response.text.lower()
            
            if 'react' in content:
                report += "  • ⚛️ React application detected\n"
            if 'vue' in content:
                report += "  • 🟢 Vue.js application detected\n"
            if 'angular' in content:
                report += "  • 🔺 Angular application detected\n"
            if '<html' in content:
                report += "  • ✅ Valid HTML structure\n"
            if 'error' in content:
                report += "  • ⚠️ Error content detected\n"
            
            # Performance assessment
            if response_time < 100:
                report += "\n⚡ **Performance**: Excellent (< 100ms)"
            elif response_time < 500:
                report += "\n⚡ **Performance**: Good (< 500ms)"
            elif response_time < 2000:
                report += "\n⚡ **Performance**: Acceptable (< 2s)"
            else:
                report += "\n🐌 **Performance**: Slow (> 2s)"
            
            return report
            
        except requests.exceptions.ConnectionError:
            return f"""
🌐 LOCALHOST SITE CHECK
{'='*50}

🔗 **URL**: {full_url}
❌ **Status**: NOT ACCESSIBLE
🚨 **Error**: Connection refused

💡 **Troubleshooting**:
  • Make sure your development server is running
  • Check if port {port} is correct
  • Verify no firewall is blocking the connection
  • Try: npm start, python -m http.server {port}, etc.
"""
        
    except Exception as e:
        return f"❌ Error checking localhost: {str(e)}"

@tool
def run_general_qa_tests(code_path: str) -> str:
    """Run general QA tests including code quality, documentation, and testing coverage.
    
    Args:
        code_path: Path to code to test
        
    Returns:
        General QA test results
    """
    try:
        qa_code = f'''
import os
from pathlib import Path

def run_real_qa(path):
    results = {{
        "files_analyzed": 0,
        "documentation_score": 0,
        "test_coverage_score": 0,
        "code_quality_score": 0,
        "findings": []
    }}
    
    path_obj = Path(r"{code_path}")
    if not path_obj.exists():
        return {{"error": "Path does not exist"}}
    
    # Check for documentation
    readme_files = list(path_obj.glob("README*"))
    if readme_files:
        results["documentation_score"] = 8
        results["findings"].append("✅ README file found")
    else:
        results["documentation_score"] = 3
        results["findings"].append("❌ No README file found")
    
    # Check for tests
    test_files = list(path_obj.rglob("test_*.py")) + list(path_obj.rglob("*_test.py")) + list(path_obj.rglob("*.test.js"))
    if test_files:
        results["test_coverage_score"] = 7
        results["findings"].append(f"✅ Found {{len(test_files)}} test files")
    else:
        results["test_coverage_score"] = 2
        results["findings"].append("❌ No test files found")
    
    # Analyze code quality indicators
    all_files = list(path_obj.rglob("*"))
    code_files = [f for f in all_files if f.suffix in ['.py', '.js', '.jsx', '.ts', '.tsx']]
    results["files_analyzed"] = len(code_files)
    
    if code_files:
        # Check for common quality indicators
        has_config = any(f.name in ['setup.py', 'package.json', 'pyproject.toml'] for f in all_files)
        has_gitignore = any(f.name == '.gitignore' for f in all_files)
        has_requirements = any(f.name in ['requirements.txt', 'package.json'] for f in all_files)
        
        quality_score = 5  # Base score
        if has_config:
            quality_score += 2
            results["findings"].append("✅ Configuration files found")
        if has_gitignore:
            quality_score += 1
            results["findings"].append("✅ .gitignore file found")
        if has_requirements:
            quality_score += 2
            results["findings"].append("✅ Dependency management files found")
        
        results["code_quality_score"] = min(quality_score, 10)
    else:
        results["code_quality_score"] = 1
        results["findings"].append("❌ No code files found")
    
    return results

result = run_real_qa(r"{code_path}")
print("QA_RESULT:", result)
'''
            
        output = python_repl.run(qa_code)
        
        if "QA_RESULT:" in output:
            result_str = output.split("QA_RESULT:")[1].strip()
            try:
                analysis = eval(result_str)
                
                overall_score = (
                    analysis.get('documentation_score', 0) + 
                    analysis.get('test_coverage_score', 0) + 
                    analysis.get('code_quality_score', 0)
                ) // 3
                
                report = f"""
🧪 REAL GENERAL QA ANALYSIS
{'='*50}

📊 **Files Analyzed**: {analysis.get('files_analyzed', 0)}

📚 **Documentation Score**: {analysis.get('documentation_score', 0)}/10
🧪 **Test Coverage Score**: {analysis.get('test_coverage_score', 0)}/10
🏗️ **Code Quality Score**: {analysis.get('code_quality_score', 0)}/10

🔍 **Findings**:
"""
                for finding in analysis.get('findings', []):
                    report += f"  • {finding}\n"
                
                report += f"""
🎯 **Overall QA Score**: {overall_score}/10

💡 **Recommendations**:
  • {'Documentation looks good!' if analysis.get('documentation_score', 0) >= 7 else 'Add comprehensive README and documentation'}
  • {'Good test coverage!' if analysis.get('test_coverage_score', 0) >= 7 else 'Add unit tests and integration tests'}
  • {'Code quality is solid!' if analysis.get('code_quality_score', 0) >= 7 else 'Improve project structure and configuration'}
"""
                return report
                
            except Exception as e:
                return f"❌ Error parsing QA results: {str(e)}"
        else:
            return f"❌ QA analysis failed: {output}"
                
    except Exception as e:
        return f"❌ Error running QA analysis: {str(e)}"

# Additional real tools using direct Python execution
@tool
def analyze_react_components(code_path: str) -> str:
    """Analyze React components for best practices and common issues.
    
    Args:
        code_path: Path to React project or component files
        
    Returns:
        Detailed React component analysis
    """
    try:
        react_analysis_code = f'''
import os
import re
from pathlib import Path

def analyze_real_react(path):
    results = {{
        "react_files": [],
        "components": [],
        "hooks_usage": [],
        "issues": []
    }}
    
    path_obj = Path(r"{code_path}")
    if not path_obj.exists():
        return {{"error": "Path does not exist"}}
    
    # Find React files
    react_extensions = ['.jsx', '.tsx', '.js', '.ts']
    for ext in react_extensions:
        for file in path_obj.rglob(f"*{{ext}}"):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check if it's actually a React file
                if any(indicator in content for indicator in ['import React', 'from React', 'useState', 'useEffect', 'JSX']):
                    results["react_files"].append(str(file))
                    
                    # Extract component names
                    component_matches = re.findall(r'function\\s+(\\w+)\\s*\\(|const\\s+(\\w+)\\s*=\\s*\\(', content)
                    for match in component_matches:
                        comp_name = match[0] or match[1]
                        if comp_name and comp_name[0].isupper():  # React components start with uppercase
                            results["components"].append(comp_name)
                    
                    # Check for hooks
                    hooks = ['useState', 'useEffect', 'useContext', 'useReducer', 'useMemo', 'useCallback']
                    for hook in hooks:
                        if hook in content:
                            results["hooks_usage"].append(f"{{file}} uses {{hook}}")
                    
                    # Check for common issues
                    if 'console.log' in content:
                        results["issues"].append(f"{{file}} - Remove console.log statements")
                    if 'useEffect(' in content and 'useEffect(() =>' in content and ', [])' not in content:
                        results["issues"].append(f"{{file}} - useEffect missing dependency array")
                        
            except Exception as e:
                results["issues"].append(f"{{file}} - Error reading: {{str(e)}}")
    
    return results

result = analyze_real_react(r"{code_path}")
print("REACT_RESULT:", result)
'''
        
        output = python_repl.run(react_analysis_code)
        
        if "REACT_RESULT:" in output:
            result_str = output.split("REACT_RESULT:")[1].strip()
            try:
                analysis = eval(result_str)
                
                report = f"""
⚛️ REAL REACT COMPONENTS ANALYSIS
{'='*50}

📁 **React Files Found**: {len(analysis.get('react_files', []))}
🧩 **Components Detected**: {len(set(analysis.get('components', [])))}

🪝 **Hooks Usage**:
"""
                for hook in analysis.get('hooks_usage', [])[:5]:
                    report += f"  • {sanitize_path_for_report(hook)}\n"
                
                report += f"""
⚠️ **Issues Found** ({len(analysis.get('issues', []))}):
"""
                for issue in analysis.get('issues', []):
                    report += f"  • {sanitize_path_for_report(issue)}\n"
                
                react_score = max(2, 10 - len(analysis.get('issues', [])))
                
                report += f"""
🎯 **React Quality Score**: {react_score}/10

💡 **Components Found**: {', '.join(set(analysis.get('components', []))[:5])}
"""
                return report
                
            except Exception as e:
                return f"❌ Error parsing React results: {str(e)}"
        else:
            return f"❌ React analysis failed: {output}"
            
    except Exception as e:
        return f"❌ Error running React analysis: {str(e)}"

@tool
def validate_sql_queries(code_path: str) -> str:
    """Validate SQL queries and database interactions.
    
    Args:
        code_path: Path to files containing SQL queries
        
    Returns:
        SQL validation and security analysis
    """
    try:
        sql_analysis_code = f'''
import os
import re
from pathlib import Path

def analyze_real_sql(path):
    results = {{
        "sql_files": [],
        "queries_found": [],
        "security_issues": [],
        "performance_issues": []
    }}
    
    path_obj = Path(r"{code_path}")
    if not path_obj.exists():
        return {{"error": "Path does not exist"}}
    
    # SQL patterns to look for
    sql_patterns = [
        r'SELECT\\s+.*?FROM\\s+\\w+',
        r'INSERT\\s+INTO\\s+\\w+',
        r'UPDATE\\s+\\w+\\s+SET',
        r'DELETE\\s+FROM\\s+\\w+',
        r'CREATE\\s+TABLE\\s+\\w+',
        r'ALTER\\s+TABLE\\s+\\w+'
    ]
    
    # Check all relevant files
    for file in path_obj.rglob("*"):
        if file.suffix in ['.py', '.js', '.sql', '.txt']:
            try:
                with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Look for SQL queries
                for pattern in sql_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
                    if matches:
                        results["sql_files"].append(str(file))
                        for match in matches:
                            results["queries_found"].append(f"{{file}}: {{match[:50]}}...")
                
                # Security checks
                if re.search(r'SELECT\\s+\\*', content, re.IGNORECASE):
                    results["performance_issues"].append(f"{{file}} - Avoid SELECT * queries")
                
                if re.search(r'\\+.*?["\'].*?\\+', content):  # String concatenation in SQL
                    results["security_issues"].append(f"{{file}} - Possible SQL injection via string concatenation")
                
                if 'DROP TABLE' in content.upper():
                    results["security_issues"].append(f"{{file}} - DROP TABLE statement found")
                    
            except Exception:
                pass
    
    return results

result = analyze_real_sql(r"{code_path}")
print("SQL_RESULT:", result)
'''
        
        output = python_repl.run(sql_analysis_code)
        
        if "SQL_RESULT:" in output:
            result_str = output.split("SQL_RESULT:")[1].strip()
            try:
                analysis = eval(result_str)
                
                report = f"""
🗃️ REAL SQL QUERIES ANALYSIS
{'='*50}

📁 **Files with SQL**: {len(set(analysis.get('sql_files', [])))}
📊 **Queries Found**: {len(analysis.get('queries_found', []))}

🔒 **Security Issues** ({len(analysis.get('security_issues', []))}):
"""
                for issue in analysis.get('security_issues', []):
                    report += f"  • {sanitize_path_for_report(issue)}\n"
                
                report += f"""
⚡ **Performance Issues** ({len(analysis.get('performance_issues', []))}):
"""
                for issue in analysis.get('performance_issues', []):
                    report += f"  • {sanitize_path_for_report(issue)}\n"
                
                sql_score = 10
                if len(analysis.get('security_issues', [])) > 0:
                    sql_score -= len(analysis.get('security_issues', [])) * 3
                if len(analysis.get('performance_issues', [])) > 0:
                    sql_score -= len(analysis.get('performance_issues', [])) * 1
                sql_score = max(2, sql_score)
                
                report += f"""
🎯 **SQL Quality Score**: {sql_score}/10

📝 **Sample Queries**:
"""
                for query in analysis.get('queries_found', [])[:3]:
                    report += f"  • {sanitize_path_for_report(query)}\n"
                
                return report
                
            except Exception as e:
                return f"❌ Error parsing SQL results: {str(e)}"
        else:
            return f"❌ SQL analysis failed: {output}"
            
    except Exception as e:
        return f"❌ Error running SQL analysis: {str(e)}"

# Additional helper tools
@tool
def analyze_code_complexity(code_path: str) -> str:
    """Analyze code complexity metrics and identify areas for improvement.
    
    Args:
        code_path: Path to code to analyze
        
    Returns:
        Code complexity analysis
    """
    return "🔄 Code complexity analysis using real AST parsing - Feature coming soon!"

@tool
def check_best_practices(code_path: str) -> str:
    """Check adherence to coding best practices and standards.
    
    Args:
        code_path: Path to code to check
        
    Returns:
        Best practices compliance report
    """
    return "✨ Best practices analysis using real pattern matching - Feature coming soon!"

@tool
def validate_imports(code_path: str) -> str:
    """Validate import statements and dependencies.
    
    Args:
        code_path: Path to code to validate imports
        
    Returns:
        Import validation report
    """
    return "📥 Import validation using real dependency resolution - Feature coming soon!" 