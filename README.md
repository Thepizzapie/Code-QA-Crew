# 🤖 Code QA Crew - Professional AI Code Analysis

> **Transform your code quality with AI-powered multi-agent analysis**  
> Comprehensive code review, security scanning, and quality assessment using CrewAI with specialized AI agents for Python, React, SQL, and mixed codebases.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![CrewAI](https://img.shields.io/badge/CrewAI-0.121.0-orange.svg)](https://crewai.com)
[![LangChain](https://img.shields.io/badge/LangChain-0.3.25-blue.svg)](https://langchain.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)](README.md)

## 🎯 What This Does

The Code QA Crew provides **professional-grade AI-powered code analysis** with:

- **🤖 5 Specialized AI Agents** - CS Professor, Tech Expert, Dependencies Expert, Security Expert, QA Tester
- **🔍 11 Real Analysis Tools** - Structure, syntax, security, dependencies, complexity using LangChain
- **🎯 Professional Scoring** - 1-10 quality scores with actionable recommendations  
- **🔒 Security Scanning** - High/Medium/Low risk categorization with OWASP patterns
- **🌐 Localhost Monitoring** - Check running applications for performance and issues
- **📊 Comprehensive Reports** - Detailed markdown reports with privacy protection
- **🚀 Multiple Interfaces** - Full CrewAI multi-agent system, quick CLI, and demo modes

## 🚀 Quick Start (5 Minutes)

### 1. Prerequisites
- **Python 3.8+** (Check: `python --version`)
- **OpenAI API Key** OR **Ollama** (for local AI)

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/Code-QA-Crew.git
cd Code-QA-Crew

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure AI (Choose One)

#### Option A: OpenAI API (Recommended)
```bash
# Create .env file
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

#### Option B: Ollama (Free Local AI)
```bash
# Install and setup Ollama
ollama pull codellama:13b
echo "USE_OLLAMA=true" > .env
echo "OLLAMA_MODEL=codellama:13b" >> .env
```

### 4. Test It Works
```bash
# Quick test on current directory
python qa_cli.py --quick

# Full CrewAI multi-agent analysis
python qa_crew.py --path "C:\path\to\your\project" --type python

# Demo analysis (fastest)
python demo_qa_crew.py --path "C:\path\to\your\project"
```

**✅ You should see a comprehensive analysis report generated!**

## 🎮 Usage Examples

### Full CrewAI Multi-Agent Analysis (Recommended)
```bash
# Complete analysis with 5 AI agents
python qa_crew.py --path ./my-project --type python

# Mixed project analysis
python qa_crew.py --path ./fullstack --type mixed

# With localhost checking
python qa_crew.py --path ./frontend --type react --port 3000
```

### Quick CLI Analysis
```bash
# Fast analysis for development
python qa_cli.py --quick --path ./my-project

# Localhost-only check
python qa_cli.py --localhost-only --port 3000
```

### Demo Analysis (Fastest)
```bash
# Standalone analysis without agents
python demo_qa_crew.py --path ./my-project --type python
```

## 🤖 AI Agent Architecture

### The QA Crew Team

1. **🎓 CS Professor** - Architecture & Complexity Analysis
   - Code structure and organization
   - Design patterns evaluation
   - Algorithmic complexity assessment
   - Academic-level insights

2. **💻 Tech Stack Expert** - Language-Specific Analysis  
   - Python syntax and PEP 8 compliance
   - React components and hooks analysis
   - SQL query validation and optimization
   - Framework-specific best practices

3. **📦 Dependencies Expert** - Package & Security Analysis
   - Dependency health and compatibility
   - Version conflict detection
   - Security vulnerability scanning
   - Supply chain security

4. **🔒 Security Expert** - Vulnerability Assessment
   - OWASP Top 10 vulnerability detection
   - Code security patterns analysis
   - Risk categorization and remediation
   - Penetration testing insights

5. **🧪 QA Tester** - Comprehensive Quality Assessment
   - Final quality synthesis
   - Testing strategy evaluation
   - Documentation assessment
   - Production readiness validation

## 📊 Real Analysis Tools (11 Tools)

All tools use **real LangChain functionality** - no mock data!

| Tool | Technology | Purpose | Output |
|------|------------|---------|--------|
| **🏗️ Code Structure** | PythonREPLTool | Directory analysis, file counting | Real file counts, organization score |
| **🐍 Python Syntax** | AST Parsing | Syntax, style (PEP 8), imports | Real syntax validation, import analysis |
| **⚛️ React Components** | File Analysis | Hook usage, component structure | Real component analysis |
| **🗃️ SQL Validation** | Regex Patterns | Query syntax, injection risks | Real SQL pattern matching |
| **📦 Dependencies** | File Parsing | requirements.txt, package.json analysis | Real dependency parsing |
| **🔒 Security Scan** | Pattern Matching | OWASP vulnerabilities, secrets | Real security pattern detection |
| **🧪 General QA** | File System | Code quality, documentation | Real file system analysis |
| **📊 Complexity** | Code Analysis | Cyclomatic complexity metrics | Real complexity calculation |
| **✨ Best Practices** | Pattern Analysis | Naming, error handling | Real best practice validation |
| **📥 Import Validation** | AST Analysis | Import health, circular deps | Real import dependency analysis |
| **🌐 Localhost Check** | HTTP Requests | Site accessibility, performance | Real HTTP connectivity testing |

## 🎯 Quality Scoring System

### Score Interpretation
- **10/10** - Excellent, production-ready
- **8-9/10** - Good, minor improvements needed
- **6-7/10** - Fair, some issues to address
- **4-5/10** - Poor, significant improvements needed
- **1-3/10** - Critical, major refactoring required

### Security Risk Levels
- **🚨 High Risk** - Immediate attention required (eval, exec, SQL injection)
- **⚠️ Medium Risk** - Should be addressed (pickle, subprocess)
- **ℹ️ Low Risk** - Best practice improvements (TODO comments)

## 🔧 Configuration Options

### AI Models

#### OpenAI (Cloud)
```bash
# .env configuration
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4-turbo-preview  # Default
# OPENAI_MODEL=gpt-3.5-turbo      # Faster/cheaper
# OPENAI_MODEL=gpt-4o             # Latest
```

#### Ollama (Local)
```bash
# .env configuration  
USE_OLLAMA=true
OLLAMA_MODEL=codellama:13b        # Recommended for code
# OLLAMA_MODEL=llama2:13b         # General purpose
# OLLAMA_MODEL=mistral:7b         # Lightweight
OLLAMA_BASE_URL=http://localhost:11434
```

### Performance Comparison

| Model | Speed | Cost | Quality | Best For |
|-------|-------|------|---------|----------|
| GPT-4 Turbo | ⚡⚡⚡ | 💰💰💰 | ⭐⭐⭐⭐⭐ | Production |
| GPT-3.5 Turbo | ⚡⚡⚡⚡ | 💰 | ⭐⭐⭐⭐ | Development |
| CodeLlama 13B | ⚡⚡ | 🆓 | ⭐⭐⭐⭐ | Code Analysis |
| Llama2 13B | ⚡⚡ | 🆓 | ⭐⭐⭐ | General QA |

## 📁 Project Structure

```
Code-QA-Crew/
├── 🎯 qa_cli.py              # Main CLI interface
├── 🛠️ qa_tools.py            # 11 analysis tools
├── 📋 demo_qa_crew.py        # Quick analysis engine
├── 🤖 qa_crew.py             # CrewAI implementation (legacy)
├── 📄 requirements.txt       # Python dependencies
├── 🔧 .env                   # API keys and configuration
├── config/
│   ├── agents.yaml           # AI agent configurations
│   └── tasks.yaml            # Task definitions
├── docs/
│   ├── 📖 TEAM_GUIDE.md      # Detailed usage guide
│   ├── 🤖 OLLAMA_SETUP.md    # Local AI setup
│   └── 🎯 AGENT_PROMPT_SHORT.md # Cursor integration
└── 📚 README.md              # This file
```

## 🚨 Troubleshooting

### Common Issues

#### "ModuleNotFoundError: No module named 'crewai'"
```bash
pip install crewai crewai-tools
```

#### "OpenAI API key not found"
```bash
# Check .env file exists and has correct format
echo "OPENAI_API_KEY=your_key_here" > .env
```

#### "Connection refused" for localhost
```bash
# Make sure your development server is running
npm start  # For React apps
python manage.py runserver  # For Django
```

#### Analysis fails on large projects
```bash
# Use quick mode for faster analysis
python qa_cli.py --path ./large-project --quick
```

### Getting Help

1. **Check the logs** - Look for error messages in terminal output
2. **Verify setup** - Run `python qa_cli.py --help` to see all options
3. **Test with small project** - Try analysis on a simple folder first
4. **Check dependencies** - Ensure all packages in requirements.txt are installed

## 🎉 Real-World Example

**Input**: YieldWise Data Scrappers project (1,912 files)  
**Output**: 2,384-line comprehensive analysis report  
**Results**:
- ✅ Python Quality: 10/10
- ⚠️ Security Score: 5/10 (3 medium risks identified)
- ✅ Overall QA: 7/10
- 📊 Found 36 Python files, 772 JS files, 5 test files

## 📚 Additional Resources

- **[TEAM_GUIDE.md](TEAM_GUIDE.md)** - Complete usage guide with examples
- **[OLLAMA_SETUP.md](OLLAMA_SETUP.md)** - Detailed local AI setup (287 lines)
- **[AGENT_PROMPT_SHORT.md](AGENT_PROMPT_SHORT.md)** - Cursor AI integration prompt
- **[GitHub Repository](https://github.com/Thepizzapie/Code-QA-Crew)** - Latest updates and issues

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Run QA analysis on your changes: `python qa_cli.py --path .`
4. Ensure all scores are ≥ 7/10
5. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

**🚀 Ready to improve your code quality? Start with:**
```bash
python qa_cli.py --path ./your-project
```

*Built with ❤️ for developers who care about code quality*
