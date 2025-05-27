# AI Agent Guide: Code QA Crew

This document provides instructions for AI agents on how to use the Code QA Crew system for automated code quality analysis.

## 🤖 Quick Start for AI Agents

### Primary Usage Method
```python
# Simple analysis - recommended for most use cases
python run_qa.py

# Or programmatically:
from run_qa import run_qa_analysis
run_qa_analysis("path/to/target/project")
```

### Alternative Methods
```bash
# CLI interface
python qa_cli.py --path ./project --type mixed

# Demo version (no port checking)
python demo_qa_crew.py --path ./project --type python
```

## 🔧 Core QA Tools Available

### 1. Code Structure Analysis
```python
from qa_tools import analyze_code_structure
result = analyze_code_structure.invoke({"folder_path": "path/to/project"})
```
**Purpose**: Analyzes project structure, file counts, complexity
**Returns**: File statistics, directory structure, complexity score

### 2. Python Syntax Check
```python
from qa_tools import check_python_syntax
result = check_python_syntax.invoke({"code_path": "path/to/file_or_folder"})
```
**Purpose**: Validates Python syntax, style (PEP 8), imports
**Returns**: Syntax errors, style issues, quality score

### 3. Security Vulnerability Scan
```python
from qa_tools import scan_security_vulnerabilities
result = scan_security_vulnerabilities.invoke({"code_path": "path/to/project"})
```
**Purpose**: Detects security vulnerabilities, hardcoded secrets
**Returns**: Security issues categorized by risk level

### 4. Package Dependencies Check
```python
from qa_tools import check_package_dependencies
result = check_package_dependencies.invoke({"code_path": "path/to/project"})
```
**Purpose**: Analyzes dependencies for security and compatibility
**Returns**: Dependency health score, vulnerability report

### 5. General QA Tests
```python
from qa_tools import run_general_qa_tests
result = run_general_qa_tests.invoke({"code_path": "path/to/project"})
```
**Purpose**: Overall code quality, documentation, test coverage
**Returns**: Quality metrics, recommendations

## 📊 Understanding QA Results

### Quality Scores (1-10 scale)
- **10/10**: Production ready, excellent quality
- **8-9/10**: Minor improvements needed
- **6-7/10**: Some issues to address
- **4-5/10**: Significant improvements needed
- **1-3/10**: Major refactoring required

### Security Risk Levels
- **High Risk**: Immediate attention (SQL injection, eval/exec)
- **Medium Risk**: Should be addressed (subprocess, pickle)
- **Low Risk**: Best practice improvements

## 🎯 Project Type Detection

The system automatically detects project types:
- **python**: Pure Python projects
- **react**: React/JavaScript projects  
- **mixed**: Full-stack projects with multiple languages
- **sql**: Database-focused projects

## 🚀 Integration Examples

### Example 1: Basic Quality Check
```python
def check_code_quality(project_path):
    from run_qa import run_qa_analysis
    
    print(f"🔍 Analyzing: {project_path}")
    run_qa_analysis(project_path)
    print("✅ Analysis complete!")
```

### Example 2: Programmatic Analysis
```python
from qa_tools import (
    analyze_code_structure,
    check_python_syntax,
    scan_security_vulnerabilities
)

def comprehensive_analysis(path):
    results = {}
    
    # Structure analysis
    results['structure'] = analyze_code_structure.invoke({"folder_path": path})
    
    # Python syntax check
    results['syntax'] = check_python_syntax.invoke({"code_path": path})
    
    # Security scan
    results['security'] = scan_security_vulnerabilities.invoke({"code_path": path})
    
    return results
```

### Example 3: Conditional Analysis
```python
import os

def smart_qa_analysis(project_path):
    if not os.path.exists(project_path):
        return "❌ Path does not exist"
    
    # Check if it's a Python project
    if any(f.endswith('.py') for f in os.listdir(project_path)):
        from run_qa import run_qa_analysis
        run_qa_analysis(project_path)
    else:
        return "⚠️ No Python files detected"
```

## 🛠️ Configuration for AI Agents

### Environment Setup
```python
import os
from decouple import config

# Load OpenAI API key
try:
    api_key = config('OPENAI_API_KEY')
    os.environ['OPENAI_API_KEY'] = api_key
    print("✅ OpenAI API Key loaded")
except:
    print("⚠️ OpenAI API Key not found")
```

### Error Handling
```python
def safe_qa_analysis(path):
    try:
        from run_qa import run_qa_analysis
        run_qa_analysis(path)
        return "✅ Analysis completed successfully"
    except Exception as e:
        return f"❌ Analysis failed: {str(e)}"
```

## 📋 Common Use Cases for AI Agents

### 1. Pre-Commit Validation
```python
def pre_commit_check(repo_path):
    """Run QA before committing code"""
    from run_qa import run_qa_analysis
    print("🔍 Running pre-commit QA check...")
    run_qa_analysis(repo_path)
```

### 2. Code Review Assistant
```python
def code_review_analysis(pull_request_path):
    """Analyze code changes for review"""
    from qa_tools import check_python_syntax, scan_security_vulnerabilities
    
    syntax_result = check_python_syntax.invoke({"code_path": pull_request_path})
    security_result = scan_security_vulnerabilities.invoke({"code_path": pull_request_path})
    
    return {
        "syntax_issues": syntax_result,
        "security_concerns": security_result
    }
```

### 3. Project Health Monitor
```python
def monitor_project_health(project_paths):
    """Monitor multiple projects"""
    results = {}
    for path in project_paths:
        try:
            from run_qa import run_qa_analysis
            run_qa_analysis(path)
            results[path] = "✅ Healthy"
        except Exception as e:
            results[path] = f"❌ Issues: {e}"
    return results
```

## 🔍 Output Interpretation

### Structure Analysis Output
```
📊 Total Files: 150
📁 Directories: 25
🐍 Python Files: 45
⚛️ JS/React Files: 30
🎯 Complexity Score: 7/10
```

### Python Syntax Output
```
✅ Files Analyzed: 45
🚨 Syntax Errors: 0
⚠️ Style Issues: 12
🎯 Python Quality Score: 8/10
```

### Security Scan Output
```
🔒 High Risk Issues: 0
⚠️ Medium Risk Issues: 2
💡 Low Risk Issues: 5
🎯 Security Score: 7/10
```

## ⚠️ Important Notes for AI Agents

1. **No Port Checking**: The system is configured to skip localhost port checking by default
2. **Path Sanitization**: Personal information is automatically removed from reports
3. **Error Resilience**: Tools continue analysis even if individual components fail
4. **Resource Usage**: Large projects may take several minutes to analyze
5. **Dependencies**: Requires OpenAI API key or local Ollama setup

## 🚨 Troubleshooting

### Common Issues
```python
# Issue: Import errors
# Solution: Ensure all dependencies are installed
pip install -r requirements.txt

# Issue: OpenAI API errors
# Solution: Check API key configuration
from decouple import config
print(config('OPENAI_API_KEY', default='Not found'))

# Issue: Path not found
# Solution: Verify path exists and is accessible
import os
print(os.path.exists('path/to/project'))
```

### Debug Mode
```python
def debug_qa_analysis(path):
    """Run QA with detailed error reporting"""
    try:
        from run_qa import run_qa_analysis
        run_qa_analysis(path)
    except Exception as e:
        print(f"❌ Error details: {e}")
        import traceback
        traceback.print_exc()
```

## 📚 Additional Resources

- **Main README.md**: Human-readable documentation
- **requirements.txt**: All dependencies
- **examples/**: Usage examples and integrations
- **tests/**: Test suite for validation

## 🎯 Best Practices for AI Agents

1. **Always check if path exists** before analysis
2. **Handle exceptions gracefully** with try/catch blocks
3. **Use the simple `run_qa.py`** for most use cases
4. **Parse output systematically** using the scoring system
5. **Respect rate limits** when using OpenAI API
6. **Cache results** for repeated analysis of same projects

---

*This QA system is designed to be AI-agent friendly with clear interfaces, consistent output formats, and robust error handling.* 