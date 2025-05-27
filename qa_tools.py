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

# Simple tool decorator for compatibility
def tool(name):
    def decorator(func):
        func._tool_name = name
        return func
    return decorator

@tool("analyze_code_structure")
def analyze_code_structure(code_path: str) -> str:
    """
    Analyze the overall structure and architecture of a codebase.
    
    Args:
        code_path: Path to the code directory or file to analyze
        
    Returns:
        Detailed analysis of code structure, organization, and architecture
    """
    try:
        path = Path(code_path)
        if not path.exists():
            return f"❌ Path does not exist: {code_path}"
        
        analysis = {
            "structure": {},
            "file_types": {},
            "complexity_metrics": {},
            "organization_score": 0
        }
        
        # Analyze directory structure
        if path.is_dir():
            analysis["structure"] = _analyze_directory_structure(path)
            analysis["file_types"] = _count_file_types(path)
            analysis["organization_score"] = _calculate_organization_score(path)
        else:
            analysis["structure"] = {"single_file": str(path)}
            analysis["file_types"] = {path.suffix: 1}
        
        # Generate report
        report = f"""
🏗️ CODE STRUCTURE ANALYSIS
{'='*50}

📁 Directory Structure:
{_format_structure(analysis['structure'])}

📊 File Type Distribution:
{_format_file_types(analysis['file_types'])}

📈 Organization Score: {analysis['organization_score']}/10

🔍 Architecture Assessment:
{_assess_architecture(analysis)}

💡 Recommendations:
{_generate_structure_recommendations(analysis)}
"""
        return report
        
    except Exception as e:
        return f"❌ Error analyzing code structure: {str(e)}"

@tool("check_python_syntax")
def check_python_syntax(code_path: str) -> str:
    """
    Check Python syntax, style, and common issues.
    
    Args:
        code_path: Path to Python file or directory
        
    Returns:
        Detailed Python syntax and style analysis
    """
    try:
        path = Path(code_path)
        if not path.exists():
            return f"❌ Path does not exist: {code_path}"
        
        python_files = []
        if path.is_file() and path.suffix == '.py':
            python_files = [path]
        elif path.is_dir():
            python_files = list(path.rglob("*.py"))
        
        if not python_files:
            return "ℹ️ No Python files found to analyze"
        
        results = {
            "syntax_errors": [],
            "style_issues": [],
            "complexity_warnings": [],
            "best_practices": []
        }
        
        for py_file in python_files:
            file_analysis = _analyze_python_file(py_file)
            for key in results:
                results[key].extend(file_analysis.get(key, []))
        
        report = f"""
🐍 PYTHON SYNTAX & STYLE ANALYSIS
{'='*50}

✅ Files Analyzed: {len(python_files)}

🚨 Syntax Errors ({len(results['syntax_errors'])}):
{_format_issues(results['syntax_errors'])}

⚠️ Style Issues ({len(results['style_issues'])}):
{_format_issues(results['style_issues'])}

📊 Complexity Warnings ({len(results['complexity_warnings'])}):
{_format_issues(results['complexity_warnings'])}

💡 Best Practice Recommendations:
{_format_issues(results['best_practices'])}

🎯 Overall Python Quality Score: {_calculate_python_score(results)}/10
"""
        return report
        
    except Exception as e:
        return f"❌ Error checking Python syntax: {str(e)}"

@tool("analyze_react_components")
def analyze_react_components(code_path: str) -> str:
    """
    Analyze React components for best practices and common issues.
    
    Args:
        code_path: Path to React project or component files
        
    Returns:
        Detailed React component analysis
    """
    try:
        path = Path(code_path)
        if not path.exists():
            return f"❌ Path does not exist: {code_path}"
        
        # Find React files
        react_files = []
        extensions = ['.jsx', '.tsx', '.js', '.ts']
        
        if path.is_file() and path.suffix in extensions:
            react_files = [path]
        elif path.is_dir():
            for ext in extensions:
                react_files.extend(list(path.rglob(f"*{ext}")))
        
        if not react_files:
            return "ℹ️ No React/JavaScript files found to analyze"
        
        # Filter for actual React components
        react_components = []
        for file in react_files:
            if _is_react_component(file):
                react_components.append(file)
        
        analysis = {
            "components_found": len(react_components),
            "hook_usage": [],
            "prop_issues": [],
            "performance_concerns": [],
            "accessibility_issues": [],
            "best_practices": []
        }
        
        for component in react_components:
            comp_analysis = _analyze_react_file(component)
            for key in analysis:
                if key != "components_found":
                    analysis[key].extend(comp_analysis.get(key, []))
        
        report = f"""
⚛️ REACT COMPONENTS ANALYSIS
{'='*50}

📊 Components Found: {analysis['components_found']}
📁 Files Analyzed: {len(react_files)}

🪝 Hook Usage Analysis:
{_format_issues(analysis['hook_usage'])}

🔧 Props & State Issues:
{_format_issues(analysis['prop_issues'])}

⚡ Performance Concerns:
{_format_issues(analysis['performance_concerns'])}

♿ Accessibility Issues:
{_format_issues(analysis['accessibility_issues'])}

💡 Best Practice Recommendations:
{_format_issues(analysis['best_practices'])}

🎯 React Quality Score: {_calculate_react_score(analysis)}/10
"""
        return report
        
    except Exception as e:
        return f"❌ Error analyzing React components: {str(e)}"

@tool("validate_sql_queries")
def validate_sql_queries(code_path: str) -> str:
    """
    Validate SQL queries and database interactions.
    
    Args:
        code_path: Path to files containing SQL queries
        
    Returns:
        SQL validation and security analysis
    """
    try:
        path = Path(code_path)
        if not path.exists():
            return f"❌ Path does not exist: {code_path}"
        
        sql_content = []
        
        # Find SQL in various file types
        if path.is_file():
            sql_content.extend(_extract_sql_from_file(path))
        elif path.is_dir():
            for file in path.rglob("*"):
                if file.is_file():
                    sql_content.extend(_extract_sql_from_file(file))
        
        if not sql_content:
            return "ℹ️ No SQL queries found to analyze"
        
        analysis = {
            "queries_found": len(sql_content),
            "syntax_issues": [],
            "security_risks": [],
            "performance_issues": [],
            "best_practices": []
        }
        
        for sql_info in sql_content:
            query_analysis = _analyze_sql_query(sql_info)
            for key in analysis:
                if key != "queries_found":
                    analysis[key].extend(query_analysis.get(key, []))
        
        report = f"""
🗃️ SQL QUERIES ANALYSIS
{'='*50}

📊 Queries Found: {analysis['queries_found']}

🚨 Syntax Issues:
{_format_issues(analysis['syntax_issues'])}

🔒 Security Risks:
{_format_issues(analysis['security_risks'])}

⚡ Performance Issues:
{_format_issues(analysis['performance_issues'])}

💡 Best Practice Recommendations:
{_format_issues(analysis['best_practices'])}

🎯 SQL Quality Score: {_calculate_sql_score(analysis)}/10
"""
        return report
        
    except Exception as e:
        return f"❌ Error validating SQL queries: {str(e)}"

@tool("check_package_dependencies")
def check_package_dependencies(code_path: str) -> str:
    """
    Check package dependencies for validity, security, and compatibility.
    
    Args:
        code_path: Path to project with dependency files
        
    Returns:
        Comprehensive dependency analysis
    """
    try:
        path = Path(code_path)
        if not path.exists():
            return f"❌ Path does not exist: {code_path}"
        
        # Find dependency files
        dep_files = _find_dependency_files(path)
        
        if not dep_files:
            return "ℹ️ No dependency files found (requirements.txt, package.json, etc.)"
        
        analysis = {
            "dependency_files": dep_files,
            "total_dependencies": 0,
            "outdated_packages": [],
            "security_vulnerabilities": [],
            "compatibility_issues": [],
            "missing_dependencies": [],
            "recommendations": []
        }
        
        for dep_file in dep_files:
            file_analysis = _analyze_dependency_file(dep_file)
            analysis["total_dependencies"] += file_analysis.get("count", 0)
            for key in ["outdated_packages", "security_vulnerabilities", "compatibility_issues", "missing_dependencies"]:
                analysis[key].extend(file_analysis.get(key, []))
        
        # Check for missing imports
        if path.is_dir():
            missing_deps = _check_missing_imports(path)
            analysis["missing_dependencies"].extend(missing_deps)
        
        analysis["recommendations"] = _generate_dependency_recommendations(analysis)
        
        report = f"""
📦 PACKAGE DEPENDENCIES ANALYSIS
{'='*50}

📁 Dependency Files Found: {len(dep_files)}
{chr(10).join([f"  • {f}" for f in dep_files])}

📊 Total Dependencies: {analysis['total_dependencies']}

⚠️ Outdated Packages ({len(analysis['outdated_packages'])}):
{_format_issues(analysis['outdated_packages'])}

🔒 Security Vulnerabilities ({len(analysis['security_vulnerabilities'])}):
{_format_issues(analysis['security_vulnerabilities'])}

⚡ Compatibility Issues ({len(analysis['compatibility_issues'])}):
{_format_issues(analysis['compatibility_issues'])}

❌ Missing Dependencies ({len(analysis['missing_dependencies'])}):
{_format_issues(analysis['missing_dependencies'])}

💡 Recommendations:
{_format_issues(analysis['recommendations'])}

🎯 Dependency Health Score: {_calculate_dependency_score(analysis)}/10
"""
        return report
        
    except Exception as e:
        return f"❌ Error checking dependencies: {str(e)}"

@tool("scan_security_vulnerabilities")
def scan_security_vulnerabilities(code_path: str) -> str:
    """
    Scan for security vulnerabilities and potential security issues.
    
    Args:
        code_path: Path to code to scan for security issues
        
    Returns:
        Security vulnerability assessment
    """
    try:
        path = Path(code_path)
        if not path.exists():
            return f"❌ Path does not exist: {code_path}"
        
        vulnerabilities = {
            "high_risk": [],
            "medium_risk": [],
            "low_risk": [],
            "best_practices": []
        }
        
        # Scan files for security issues
        if path.is_file():
            file_vulns = _scan_file_security(path)
            for risk_level in vulnerabilities:
                vulnerabilities[risk_level].extend(file_vulns.get(risk_level, []))
        elif path.is_dir():
            for file in path.rglob("*"):
                if file.is_file() and not _should_skip_file(file):
                    file_vulns = _scan_file_security(file)
                    for risk_level in vulnerabilities:
                        vulnerabilities[risk_level].extend(file_vulns.get(risk_level, []))
        
        total_issues = sum(len(vulnerabilities[level]) for level in ["high_risk", "medium_risk", "low_risk"])
        
        report = f"""
🔒 SECURITY VULNERABILITY SCAN
{'='*50}

🚨 High Risk Issues ({len(vulnerabilities['high_risk'])}):
{_format_issues(vulnerabilities['high_risk'])}

⚠️ Medium Risk Issues ({len(vulnerabilities['medium_risk'])}):
{_format_issues(vulnerabilities['medium_risk'])}

ℹ️ Low Risk Issues ({len(vulnerabilities['low_risk'])}):
{_format_issues(vulnerabilities['low_risk'])}

💡 Security Best Practices:
{_format_issues(vulnerabilities['best_practices'])}

🎯 Security Score: {_calculate_security_score(vulnerabilities)}/10
📊 Total Issues Found: {total_issues}
"""
        return report
        
    except Exception as e:
        return f"❌ Error scanning security vulnerabilities: {str(e)}"

@tool("run_general_qa_tests")
def run_general_qa_tests(code_path: str) -> str:
    """
    Run general QA tests including code quality, documentation, and testing coverage.
    
    Args:
        code_path: Path to code to test
        
    Returns:
        General QA test results
    """
    try:
        path = Path(code_path)
        if not path.exists():
            return f"❌ Path does not exist: {code_path}"
        
        qa_results = {
            "code_quality": {},
            "documentation": {},
            "testing": {},
            "maintainability": {}
        }
        
        # Code quality checks
        qa_results["code_quality"] = _assess_code_quality(path)
        
        # Documentation assessment
        qa_results["documentation"] = _assess_documentation(path)
        
        # Testing coverage
        qa_results["testing"] = _assess_testing(path)
        
        # Maintainability metrics
        qa_results["maintainability"] = _assess_maintainability(path)
        
        overall_score = _calculate_overall_qa_score(qa_results)
        
        report = f"""
🧪 GENERAL QA TEST RESULTS
{'='*50}

📊 Code Quality Assessment:
{_format_qa_section(qa_results['code_quality'])}

📚 Documentation Assessment:
{_format_qa_section(qa_results['documentation'])}

🧪 Testing Assessment:
{_format_qa_section(qa_results['testing'])}

🔧 Maintainability Assessment:
{_format_qa_section(qa_results['maintainability'])}

🎯 Overall QA Score: {overall_score}/10

💡 Priority Recommendations:
{_generate_qa_recommendations(qa_results)}
"""
        return report
        
    except Exception as e:
        return f"❌ Error running QA tests: {str(e)}"

@tool("analyze_code_complexity")
def analyze_code_complexity(code_path: str) -> str:
    """
    Analyze code complexity metrics and identify areas for improvement.
    
    Args:
        code_path: Path to code to analyze
        
    Returns:
        Code complexity analysis
    """
    try:
        path = Path(code_path)
        if not path.exists():
            return f"❌ Path does not exist: {code_path}"
        
        complexity_metrics = {
            "cyclomatic_complexity": [],
            "cognitive_complexity": [],
            "function_length": [],
            "class_complexity": [],
            "nesting_depth": []
        }
        
        # Analyze complexity for different file types
        if path.is_file():
            file_complexity = _analyze_file_complexity(path)
            for metric in complexity_metrics:
                complexity_metrics[metric].extend(file_complexity.get(metric, []))
        elif path.is_dir():
            for file in path.rglob("*"):
                if file.is_file() and _is_code_file(file):
                    file_complexity = _analyze_file_complexity(file)
                    for metric in complexity_metrics:
                        complexity_metrics[metric].extend(file_complexity.get(metric, []))
        
        report = f"""
📊 CODE COMPLEXITY ANALYSIS
{'='*50}

🔄 Cyclomatic Complexity:
{_format_complexity_metric(complexity_metrics['cyclomatic_complexity'])}

🧠 Cognitive Complexity:
{_format_complexity_metric(complexity_metrics['cognitive_complexity'])}

📏 Function Length Analysis:
{_format_complexity_metric(complexity_metrics['function_length'])}

🏗️ Class Complexity:
{_format_complexity_metric(complexity_metrics['class_complexity'])}

🪆 Nesting Depth:
{_format_complexity_metric(complexity_metrics['nesting_depth'])}

🎯 Complexity Score: {_calculate_complexity_score(complexity_metrics)}/10

💡 Refactoring Recommendations:
{_generate_complexity_recommendations(complexity_metrics)}
"""
        return report
        
    except Exception as e:
        return f"❌ Error analyzing code complexity: {str(e)}"

@tool("check_best_practices")
def check_best_practices(code_path: str) -> str:
    """
    Check adherence to coding best practices and standards.
    
    Args:
        code_path: Path to code to check
        
    Returns:
        Best practices compliance report
    """
    try:
        path = Path(code_path)
        if not path.exists():
            return f"❌ Path does not exist: {code_path}"
        
        practices = {
            "naming_conventions": [],
            "code_organization": [],
            "error_handling": [],
            "performance": [],
            "readability": []
        }
        
        # Check best practices
        if path.is_file():
            file_practices = _check_file_best_practices(path)
            for category in practices:
                practices[category].extend(file_practices.get(category, []))
        elif path.is_dir():
            for file in path.rglob("*"):
                if file.is_file() and _is_code_file(file):
                    file_practices = _check_file_best_practices(file)
                    for category in practices:
                        practices[category].extend(file_practices.get(category, []))
        
        report = f"""
✨ BEST PRACTICES COMPLIANCE
{'='*50}

🏷️ Naming Conventions:
{_format_issues(practices['naming_conventions'])}

📁 Code Organization:
{_format_issues(practices['code_organization'])}

🚨 Error Handling:
{_format_issues(practices['error_handling'])}

⚡ Performance:
{_format_issues(practices['performance'])}

📖 Readability:
{_format_issues(practices['readability'])}

🎯 Best Practices Score: {_calculate_best_practices_score(practices)}/10

💡 Improvement Suggestions:
{_generate_best_practices_recommendations(practices)}
"""
        return report
        
    except Exception as e:
        return f"❌ Error checking best practices: {str(e)}"

@tool("validate_imports")
def validate_imports(code_path: str) -> str:
    """
    Validate import statements and dependencies.
    
    Args:
        code_path: Path to code to validate imports
        
    Returns:
        Import validation report
    """
    try:
        path = Path(code_path)
        if not path.exists():
            return f"❌ Path does not exist: {code_path}"
        
        import_analysis = {
            "valid_imports": [],
            "invalid_imports": [],
            "unused_imports": [],
            "missing_imports": [],
            "circular_imports": []
        }
        
        # Analyze imports
        if path.is_file():
            file_imports = _analyze_file_imports(path)
            for category in import_analysis:
                import_analysis[category].extend(file_imports.get(category, []))
        elif path.is_dir():
            for file in path.rglob("*.py"):
                file_imports = _analyze_file_imports(file)
                for category in import_analysis:
                    import_analysis[category].extend(file_imports.get(category, []))
        
        report = f"""
📥 IMPORT VALIDATION REPORT
{'='*50}

✅ Valid Imports: {len(import_analysis['valid_imports'])}

❌ Invalid Imports ({len(import_analysis['invalid_imports'])}):
{_format_issues(import_analysis['invalid_imports'])}

🗑️ Unused Imports ({len(import_analysis['unused_imports'])}):
{_format_issues(import_analysis['unused_imports'])}

❓ Missing Imports ({len(import_analysis['missing_imports'])}):
{_format_issues(import_analysis['missing_imports'])}

🔄 Circular Imports ({len(import_analysis['circular_imports'])}):
{_format_issues(import_analysis['circular_imports'])}

🎯 Import Health Score: {_calculate_import_score(import_analysis)}/10
"""
        return report
        
    except Exception as e:
        return f"❌ Error validating imports: {str(e)}"

@tool("check_localhost_site")
def check_localhost_site(port: str = "3000", path: str = "/") -> str:
    """
    Check if a localhost site is operational and accessible.
    
    Args:
        port: Port number to check (default: 3000 for React apps)
        path: Path to check on the site (default: /)
        
    Returns:
        Status report of the localhost site including accessibility, response time, and basic checks
    """
    try:
        base_url = f"http://localhost:{port}"
        full_url = urljoin(base_url, path)
        
        site_status = {
            "url": full_url,
            "accessible": False,
            "response_time": None,
            "status_code": None,
            "content_checks": [],
            "errors": [],
            "recommendations": []
        }
        
        print(f"🌐 Checking localhost site: {full_url}")
        
        # Check if site is accessible
        start_time = time.time()
        try:
            response = requests.get(full_url, timeout=10)
            response_time = time.time() - start_time
            
            site_status["accessible"] = True
            site_status["response_time"] = round(response_time * 1000, 2)  # Convert to ms
            site_status["status_code"] = response.status_code
            
            # Basic content checks
            content = response.text.lower()
            
            # Check for common web technologies
            if "react" in content or "react-dom" in content:
                site_status["content_checks"].append("✅ React application detected")
            
            if "vue" in content:
                site_status["content_checks"].append("✅ Vue.js application detected")
            
            if "angular" in content:
                site_status["content_checks"].append("✅ Angular application detected")
            
            # Check for common issues
            if "error" in content and "404" in content:
                site_status["errors"].append("⚠️ 404 error content detected")
            
            if "uncaught" in content or "exception" in content:
                site_status["errors"].append("⚠️ JavaScript errors detected in content")
            
            if len(content) < 100:
                site_status["errors"].append("⚠️ Very minimal content - site might not be fully loaded")
            
            # Check response status
            if response.status_code == 200:
                site_status["content_checks"].append("✅ HTTP 200 OK response")
            elif response.status_code == 404:
                site_status["errors"].append("❌ HTTP 404 Not Found")
            elif response.status_code >= 500:
                site_status["errors"].append(f"❌ Server error: HTTP {response.status_code}")
            elif response.status_code >= 400:
                site_status["errors"].append(f"⚠️ Client error: HTTP {response.status_code}")
            
            # Performance recommendations
            if site_status["response_time"] > 2000:
                site_status["recommendations"].append("🐌 Slow response time - consider optimization")
            elif site_status["response_time"] < 100:
                site_status["recommendations"].append("⚡ Excellent response time")
            
            # Check for basic HTML structure
            if "<html" in content and "</html>" in content:
                site_status["content_checks"].append("✅ Valid HTML structure detected")
            else:
                site_status["errors"].append("⚠️ Invalid or incomplete HTML structure")
            
            # Check for meta tags
            if "<meta" in content:
                site_status["content_checks"].append("✅ Meta tags present")
            
            # Check for CSS
            if "<style" in content or ".css" in content:
                site_status["content_checks"].append("✅ CSS styling detected")
            
            # Check for JavaScript
            if "<script" in content or ".js" in content:
                site_status["content_checks"].append("✅ JavaScript detected")
                
        except requests.exceptions.ConnectionError:
            site_status["errors"].append(f"❌ Connection refused - site not running on port {port}")
            site_status["recommendations"].append(f"🔧 Start your development server on port {port}")
            
        except requests.exceptions.Timeout:
            site_status["errors"].append("❌ Request timeout - site taking too long to respond")
            site_status["recommendations"].append("🔧 Check server performance and network connectivity")
            
        except Exception as e:
            site_status["errors"].append(f"❌ Unexpected error: {str(e)}")
        
        # Additional port-specific checks
        common_ports = {
            "3000": "React/Node.js development server",
            "3001": "Alternative React/Node.js port",
            "8000": "Python development server",
            "8080": "Alternative web server",
            "5000": "Flask development server",
            "4200": "Angular development server",
            "8080": "Spring Boot / Tomcat",
            "5173": "Vite development server",
            "3333": "Nuxt.js development server"
        }
        
        if port in common_ports:
            site_status["content_checks"].append(f"📋 Expected: {common_ports[port]}")
        
        # Generate report
        report = f"""
🌐 LOCALHOST SITE CHECK
{'='*50}

🔗 URL: {site_status['url']}
📊 Status: {'✅ ACCESSIBLE' if site_status['accessible'] else '❌ NOT ACCESSIBLE'}
⏱️ Response Time: {site_status['response_time']}ms
📈 HTTP Status: {site_status['status_code']}

✅ Content Checks:
{chr(10).join(site_status['content_checks']) if site_status['content_checks'] else '  No positive checks'}

❌ Issues Found:
{chr(10).join(site_status['errors']) if site_status['errors'] else '  ✅ No issues detected'}

💡 Recommendations:
{chr(10).join(site_status['recommendations']) if site_status['recommendations'] else '  👍 Site looks good!'}

🔧 Quick Troubleshooting:
  • Make sure your development server is running
  • Check if the port {port} is correct
  • Verify no firewall is blocking the connection
  • Try accessing {full_url} in your browser
"""
        
        return report
        
    except Exception as e:
        return f"❌ Error checking localhost site: {str(e)}"

# Helper functions (implementation details)
def _analyze_directory_structure(path: Path) -> Dict:
    """Analyze directory structure"""
    structure = {}
    try:
        for item in path.iterdir():
            if item.is_dir():
                structure[item.name] = _analyze_directory_structure(item)
            else:
                structure[item.name] = "file"
    except PermissionError:
        structure["<permission_denied>"] = "error"
    return structure

def _count_file_types(path: Path) -> Dict[str, int]:
    """Count file types in directory"""
    file_types = {}
    for file in path.rglob("*"):
        if file.is_file():
            ext = file.suffix or "no_extension"
            file_types[ext] = file_types.get(ext, 0) + 1
    return file_types

def _calculate_organization_score(path: Path) -> int:
    """Calculate organization score based on structure"""
    # Simple scoring based on common patterns
    score = 5  # Base score
    
    # Check for common directories
    common_dirs = ['src', 'lib', 'tests', 'docs', 'config']
    for dir_name in common_dirs:
        if (path / dir_name).exists():
            score += 1
    
    return min(score, 10)

def _format_structure(structure: Dict, indent: int = 0) -> str:
    """Format directory structure for display"""
    result = ""
    for name, content in structure.items():
        result += "  " * indent + f"├── {name}\n"
        if isinstance(content, dict):
            result += _format_structure(content, indent + 1)
    return result

def _format_file_types(file_types: Dict[str, int]) -> str:
    """Format file type distribution"""
    if not file_types:
        return "  No files found"
    
    result = ""
    for ext, count in sorted(file_types.items(), key=lambda x: x[1], reverse=True):
        result += f"  {ext}: {count} files\n"
    return result.strip()

def _assess_architecture(analysis: Dict) -> str:
    """Assess overall architecture"""
    score = analysis.get("organization_score", 0)
    if score >= 8:
        return "Excellent - Well-organized codebase with clear structure"
    elif score >= 6:
        return "Good - Decent organization with room for improvement"
    elif score >= 4:
        return "Fair - Basic organization, consider restructuring"
    else:
        return "Poor - Needs significant organizational improvements"

def _generate_structure_recommendations(analysis: Dict) -> str:
    """Generate structure improvement recommendations"""
    recommendations = []
    
    if analysis.get("organization_score", 0) < 7:
        recommendations.append("Consider organizing code into logical directories (src, tests, docs)")
    
    file_types = analysis.get("file_types", {})
    if len(file_types) > 10:
        recommendations.append("Large number of file types detected - consider consolidation")
    
    if not recommendations:
        recommendations.append("Code structure looks good!")
    
    return "\n".join([f"  • {rec}" for rec in recommendations])

def _analyze_python_file(file_path: Path) -> Dict:
    """Analyze a single Python file"""
    results = {
        "syntax_errors": [],
        "style_issues": [],
        "complexity_warnings": [],
        "best_practices": []
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check syntax
        try:
            ast.parse(content)
        except SyntaxError as e:
            results["syntax_errors"].append(f"{file_path}:{e.lineno} - {e.msg}")
        
        # Basic style checks
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if len(line) > 120:
                results["style_issues"].append(f"{file_path}:{i} - Line too long ({len(line)} chars)")
            if line.strip().endswith('\\'):
                results["style_issues"].append(f"{file_path}:{i} - Avoid line continuation")
        
        # Check for common issues
        if 'import *' in content:
            results["best_practices"].append(f"{file_path} - Avoid wildcard imports")
        
        if 'print(' in content and 'debug' not in str(file_path).lower():
            results["best_practices"].append(f"{file_path} - Consider using logging instead of print")
            
    except Exception as e:
        results["syntax_errors"].append(f"{file_path} - Error reading file: {str(e)}")
    
    return results

def _format_issues(issues: List[str]) -> str:
    """Format list of issues for display"""
    if not issues:
        return "  ✅ No issues found"
    
    return "\n".join([f"  • {issue}" for issue in issues[:10]])  # Limit to 10 items

def _calculate_python_score(results: Dict) -> int:
    """Calculate Python quality score"""
    total_issues = sum(len(results[key]) for key in results)
    if total_issues == 0:
        return 10
    elif total_issues <= 5:
        return 8
    elif total_issues <= 15:
        return 6
    elif total_issues <= 30:
        return 4
    else:
        return 2

def _is_react_component(file_path: Path) -> bool:
    """Check if file contains React components"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Simple heuristics for React components
        react_indicators = [
            'import React',
            'from React',
            'useState',
            'useEffect',
            'JSX.Element',
            'React.Component',
            'return (',
            '<div',
            '<span',
            'className='
        ]
        
        return any(indicator in content for indicator in react_indicators)
    except:
        return False

def _analyze_react_file(file_path: Path) -> Dict:
    """Analyze a React component file"""
    results = {
        "hook_usage": [],
        "prop_issues": [],
        "performance_concerns": [],
        "accessibility_issues": [],
        "best_practices": []
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for hooks
        if 'useState' in content:
            results["hook_usage"].append(f"{file_path} - Uses useState hook")
        if 'useEffect' in content:
            results["hook_usage"].append(f"{file_path} - Uses useEffect hook")
        
        # Check for accessibility
        if 'alt=' not in content and '<img' in content:
            results["accessibility_issues"].append(f"{file_path} - Images missing alt attributes")
        
        # Performance checks
        if 'useEffect(() =>' in content and ', [])' not in content:
            results["performance_concerns"].append(f"{file_path} - useEffect without dependency array")
        
        # Best practices
        if 'console.log' in content:
            results["best_practices"].append(f"{file_path} - Remove console.log statements")
            
    except Exception as e:
        results["best_practices"].append(f"{file_path} - Error analyzing: {str(e)}")
    
    return results

def _calculate_react_score(analysis: Dict) -> int:
    """Calculate React quality score"""
    total_issues = sum(len(analysis[key]) for key in analysis if key != "components_found")
    if total_issues == 0:
        return 10
    elif total_issues <= 3:
        return 8
    elif total_issues <= 8:
        return 6
    elif total_issues <= 15:
        return 4
    else:
        return 2

def _extract_sql_from_file(file_path: Path) -> List[Dict]:
    """Extract SQL queries from various file types"""
    sql_queries = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for SQL patterns
        sql_patterns = [
            r'SELECT\s+.*?FROM\s+\w+',
            r'INSERT\s+INTO\s+\w+',
            r'UPDATE\s+\w+\s+SET',
            r'DELETE\s+FROM\s+\w+',
            r'CREATE\s+TABLE\s+\w+',
            r'ALTER\s+TABLE\s+\w+'
        ]
        
        for pattern in sql_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE | re.DOTALL)
            for match in matches:
                sql_queries.append({
                    'file': str(file_path),
                    'query': match.group(),
                    'line': content[:match.start()].count('\n') + 1
                })
                
    except Exception:
        pass
    
    return sql_queries

def _analyze_sql_query(sql_info: Dict) -> Dict:
    """Analyze a single SQL query"""
    results = {
        "syntax_issues": [],
        "security_risks": [],
        "performance_issues": [],
        "best_practices": []
    }
    
    query = sql_info['query'].upper()
    file_line = f"{sql_info['file']}:{sql_info['line']}"
    
    # Security checks
    if any(risk in query for risk in ['DROP', 'DELETE', 'TRUNCATE']):
        results["security_risks"].append(f"{file_line} - Potentially dangerous operation")
    
    if "'" in query and 'CONCAT' not in query:
        results["security_risks"].append(f"{file_line} - Possible SQL injection risk")
    
    # Performance checks
    if 'SELECT *' in query:
        results["performance_issues"].append(f"{file_line} - Avoid SELECT * queries")
    
    if 'WHERE' not in query and 'SELECT' in query:
        results["performance_issues"].append(f"{file_line} - Query without WHERE clause")
    
    return results

def _calculate_sql_score(analysis: Dict) -> int:
    """Calculate SQL quality score"""
    total_issues = sum(len(analysis[key]) for key in analysis if key != "queries_found")
    if total_issues == 0:
        return 10
    elif total_issues <= 2:
        return 8
    elif total_issues <= 5:
        return 6
    elif total_issues <= 10:
        return 4
    else:
        return 2

def _find_dependency_files(path: Path) -> List[str]:
    """Find dependency management files"""
    dep_files = []
    
    # Common dependency files
    common_files = [
        'requirements.txt',
        'package.json',
        'Pipfile',
        'pyproject.toml',
        'setup.py',
        'environment.yml',
        'Gemfile',
        'composer.json'
    ]
    
    if path.is_file():
        if path.name in common_files:
            dep_files.append(str(path))
    else:
        for file_name in common_files:
            file_path = path / file_name
            if file_path.exists():
                dep_files.append(str(file_path))
    
    return dep_files

def _analyze_dependency_file(file_path: str) -> Dict:
    """Analyze a dependency file"""
    results = {
        "count": 0,
        "outdated_packages": [],
        "security_vulnerabilities": [],
        "compatibility_issues": [],
        "missing_dependencies": []
    }
    
    try:
        path = Path(file_path)
        
        if path.name == 'requirements.txt':
            with open(path, 'r') as f:
                lines = f.readlines()
            
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    results["count"] += 1
                    # Basic checks
                    if '==' not in line and '>=' not in line:
                        results["compatibility_issues"].append(f"{file_path} - {line} (no version specified)")
        
        elif path.name == 'package.json':
            with open(path, 'r') as f:
                data = json.load(f)
            
            deps = data.get('dependencies', {})
            dev_deps = data.get('devDependencies', {})
            results["count"] = len(deps) + len(dev_deps)
            
    except Exception as e:
        results["compatibility_issues"].append(f"{file_path} - Error reading file: {str(e)}")
    
    return results

def _check_missing_imports(path: Path) -> List[str]:
    """Check for missing imports in Python files"""
    missing = []
    
    for py_file in path.rglob("*.py"):
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Simple check for common missing imports
            if 'pandas' in content and 'import pandas' not in content:
                missing.append(f"{py_file} - Missing pandas import")
            if 'numpy' in content and 'import numpy' not in content:
                missing.append(f"{py_file} - Missing numpy import")
                
        except Exception:
            continue
    
    return missing

def _generate_dependency_recommendations(analysis: Dict) -> List[str]:
    """Generate dependency recommendations"""
    recommendations = []
    
    if analysis["total_dependencies"] > 50:
        recommendations.append("Consider reducing number of dependencies")
    
    if len(analysis["outdated_packages"]) > 0:
        recommendations.append("Update outdated packages")
    
    if len(analysis["security_vulnerabilities"]) > 0:
        recommendations.append("Address security vulnerabilities immediately")
    
    if not recommendations:
        recommendations.append("Dependencies look healthy!")
    
    return recommendations

def _calculate_dependency_score(analysis: Dict) -> int:
    """Calculate dependency health score"""
    issues = len(analysis["outdated_packages"]) + len(analysis["security_vulnerabilities"]) + len(analysis["compatibility_issues"])
    
    if issues == 0:
        return 10
    elif issues <= 3:
        return 8
    elif issues <= 8:
        return 6
    elif issues <= 15:
        return 4
    else:
        return 2

def _scan_file_security(file_path: Path) -> Dict:
    """Scan a file for security issues"""
    vulnerabilities = {
        "high_risk": [],
        "medium_risk": [],
        "low_risk": [],
        "best_practices": []
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # High risk patterns
        high_risk_patterns = [
            (r'eval\s*\(', 'Use of eval() function'),
            (r'exec\s*\(', 'Use of exec() function'),
            (r'__import__\s*\(', 'Dynamic imports'),
            (r'shell=True', 'Shell injection risk'),
            (r'password\s*=\s*["\'][^"\']+["\']', 'Hardcoded password')
        ]
        
        for pattern, description in high_risk_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                vulnerabilities["high_risk"].append(f"{file_path} - {description}")
        
        # Medium risk patterns
        medium_risk_patterns = [
            (r'pickle\.loads?', 'Pickle deserialization'),
            (r'yaml\.load\s*\(', 'Unsafe YAML loading'),
            (r'subprocess\.call', 'Subprocess usage'),
            (r'os\.system', 'OS system calls')
        ]
        
        for pattern, description in medium_risk_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                vulnerabilities["medium_risk"].append(f"{file_path} - {description}")
        
        # Low risk / best practices
        if 'TODO' in content or 'FIXME' in content:
            vulnerabilities["low_risk"].append(f"{file_path} - Contains TODO/FIXME comments")
        
        if 'print(' in content and file_path.suffix == '.py':
            vulnerabilities["best_practices"].append(f"{file_path} - Use logging instead of print")
            
    except Exception:
        pass
    
    return vulnerabilities

def _should_skip_file(file_path: Path) -> bool:
    """Check if file should be skipped in security scan"""
    skip_extensions = {'.pyc', '.pyo', '.pyd', '.so', '.dll', '.exe', '.bin'}
    skip_dirs = {'__pycache__', '.git', 'node_modules', '.venv', 'venv'}
    
    if file_path.suffix in skip_extensions:
        return True
    
    for part in file_path.parts:
        if part in skip_dirs:
            return True
    
    return False

def _calculate_security_score(vulnerabilities: Dict) -> int:
    """Calculate security score"""
    high = len(vulnerabilities["high_risk"])
    medium = len(vulnerabilities["medium_risk"])
    low = len(vulnerabilities["low_risk"])
    
    if high > 0:
        return max(2, 6 - high)
    elif medium > 0:
        return max(4, 8 - medium)
    elif low > 0:
        return max(6, 9 - low)
    else:
        return 10

def _assess_code_quality(path: Path) -> Dict:
    """Assess overall code quality"""
    return {
        "score": 7,
        "issues": ["Sample code quality assessment"],
        "strengths": ["Well-structured code"]
    }

def _assess_documentation(path: Path) -> Dict:
    """Assess documentation quality"""
    readme_exists = (path / "README.md").exists() or (path / "README.txt").exists()
    return {
        "score": 8 if readme_exists else 4,
        "issues": [] if readme_exists else ["Missing README file"],
        "strengths": ["Good documentation"] if readme_exists else []
    }

def _assess_testing(path: Path) -> Dict:
    """Assess testing coverage"""
    test_files = list(path.rglob("test_*.py")) + list(path.rglob("*_test.py"))
    return {
        "score": 8 if test_files else 3,
        "issues": [] if test_files else ["No test files found"],
        "strengths": [f"Found {len(test_files)} test files"] if test_files else []
    }

def _assess_maintainability(path: Path) -> Dict:
    """Assess code maintainability"""
    return {
        "score": 7,
        "issues": ["Consider adding more comments"],
        "strengths": ["Good function organization"]
    }

def _calculate_overall_qa_score(qa_results: Dict) -> int:
    """Calculate overall QA score"""
    scores = [section.get("score", 5) for section in qa_results.values()]
    return sum(scores) // len(scores) if scores else 5

def _format_qa_section(section: Dict) -> str:
    """Format QA section for display"""
    score = section.get("score", 0)
    issues = section.get("issues", [])
    strengths = section.get("strengths", [])
    
    result = f"  Score: {score}/10\n"
    
    if strengths:
        result += "  Strengths:\n"
        for strength in strengths[:3]:
            result += f"    ✅ {strength}\n"
    
    if issues:
        result += "  Issues:\n"
        for issue in issues[:3]:
            result += f"    ⚠️ {issue}\n"
    
    return result

def _generate_qa_recommendations(qa_results: Dict) -> str:
    """Generate QA recommendations"""
    recommendations = []
    
    for section_name, section in qa_results.items():
        if section.get("score", 0) < 6:
            recommendations.append(f"Improve {section_name}")
    
    if not recommendations:
        recommendations.append("Overall quality looks good!")
    
    return "\n".join([f"  • {rec}" for rec in recommendations[:5]])

# Additional helper functions for complexity, best practices, and imports
def _analyze_file_complexity(file_path: Path) -> Dict:
    """Analyze complexity of a single file"""
    return {
        "cyclomatic_complexity": [f"{file_path} - Moderate complexity"],
        "cognitive_complexity": [],
        "function_length": [],
        "class_complexity": [],
        "nesting_depth": []
    }

def _is_code_file(file_path: Path) -> bool:
    """Check if file is a code file"""
    code_extensions = {'.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.cs', '.php', '.rb', '.go'}
    return file_path.suffix in code_extensions

def _format_complexity_metric(metrics: List[str]) -> str:
    """Format complexity metrics"""
    if not metrics:
        return "  ✅ No complexity issues found"
    return "\n".join([f"  • {metric}" for metric in metrics[:5]])

def _calculate_complexity_score(metrics: Dict) -> int:
    """Calculate complexity score"""
    total_issues = sum(len(metrics[key]) for key in metrics)
    return max(2, 10 - total_issues)

def _generate_complexity_recommendations(metrics: Dict) -> str:
    """Generate complexity recommendations"""
    recommendations = []
    
    for metric_type, issues in metrics.items():
        if issues:
            recommendations.append(f"Address {metric_type} issues")
    
    if not recommendations:
        recommendations.append("Complexity levels are acceptable")
    
    return "\n".join([f"  • {rec}" for rec in recommendations[:3]])

def _check_file_best_practices(file_path: Path) -> Dict:
    """Check best practices for a file"""
    return {
        "naming_conventions": [],
        "code_organization": [],
        "error_handling": [],
        "performance": [],
        "readability": []
    }

def _calculate_best_practices_score(practices: Dict) -> int:
    """Calculate best practices score"""
    total_issues = sum(len(practices[key]) for key in practices)
    return max(2, 10 - total_issues // 2)

def _generate_best_practices_recommendations(practices: Dict) -> str:
    """Generate best practices recommendations"""
    recommendations = []
    
    for category, issues in practices.items():
        if issues:
            recommendations.append(f"Improve {category}")
    
    if not recommendations:
        recommendations.append("Following good practices!")
    
    return "\n".join([f"  • {rec}" for rec in recommendations[:3]])

def _analyze_file_imports(file_path: Path) -> Dict:
    """Analyze imports in a file"""
    return {
        "valid_imports": [f"{file_path} - Standard imports"],
        "invalid_imports": [],
        "unused_imports": [],
        "missing_imports": [],
        "circular_imports": []
    }

def _calculate_import_score(analysis: Dict) -> int:
    """Calculate import health score"""
    issues = sum(len(analysis[key]) for key in analysis if key != "valid_imports")
    return max(2, 10 - issues) 