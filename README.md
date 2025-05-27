# Code QA Crew

Automated code quality analysis using AI agents. Provides comprehensive code review, security scanning, and quality assessment for Python, React, SQL, and mixed codebases.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![CrewAI](https://img.shields.io/badge/CrewAI-0.121.0-orange.svg)](https://crewai.com)
[![LangChain](https://img.shields.io/badge/LangChain-0.3.25-blue.svg)](https://langchain.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## Features

- **Multi-Agent Analysis**: 5 specialized AI agents for different aspects of code review
- **Real Analysis Tools**: 11 tools using LangChain for actual code analysis (not mock data)
- **Quality Scoring**: 1-10 scoring system with actionable recommendations
- **Security Scanning**: OWASP pattern detection with risk categorization
- **Multiple Interfaces**: Full CrewAI system, CLI, and standalone demo
- **Privacy Protection**: Path sanitization in reports

## Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API Key OR Ollama (for local AI)

### Installation
```bash
git clone https://github.com/yourusername/Code-QA-Crew.git
cd Code-QA-Crew
pip install -r requirements.txt
```

### Configuration

Copy `.env.example` to `.env` and configure:

**Option A: OpenAI API**
```bash
OPENAI_API_KEY=your_api_key_here
```

**Option B: Ollama (Local)**
```bash
USE_OLLAMA=true
OLLAMA_MODEL=codellama:13b
OLLAMA_BASE_URL=http://localhost:11434
```

### Usage

**Quick analysis:**
```bash
python qa_cli.py --quick --path ./my-project
```

**Full multi-agent analysis:**
```bash
python qa_crew.py --path ./my-project --type python
```

**Standalone demo:**
```bash
python demo_qa_crew.py --path ./my-project --type python
```

## Analysis Tools

| Tool | Purpose | Technology |
|------|---------|------------|
| Code Structure | Directory analysis, file counting | PythonREPLTool |
| Python Syntax | Syntax validation, PEP 8, imports | AST Parsing |
| React Components | Hook usage, component structure | File Analysis |
| SQL Validation | Query syntax, injection risks | Regex Patterns |
| Dependencies | Package analysis, vulnerabilities | File Parsing |
| Security Scan | OWASP vulnerabilities, secrets | Pattern Matching |
| General QA | Code quality, documentation | File System |
| Complexity | Cyclomatic complexity metrics | Code Analysis |
| Best Practices | Naming, error handling | Pattern Analysis |
| Import Validation | Import health, circular dependencies | AST Analysis |
| Localhost Check | Site accessibility, performance | HTTP Requests |

## AI Agents

1. **CS Professor** - Architecture and complexity analysis
2. **Tech Stack Expert** - Language-specific analysis (Python, React, SQL)
3. **Dependencies Expert** - Package management and security
4. **Security Expert** - Vulnerability assessment
5. **QA Tester** - Quality synthesis and testing strategy

## Scoring System

- **10/10** - Production ready
- **8-9/10** - Minor improvements needed
- **6-7/10** - Some issues to address
- **4-5/10** - Significant improvements needed
- **1-3/10** - Major refactoring required

## Security Risk Levels

- **High Risk** - Immediate attention required (eval, exec, SQL injection)
- **Medium Risk** - Should be addressed (pickle, subprocess)
- **Low Risk** - Best practice improvements

## Configuration Options

### AI Models

**OpenAI:**
```bash
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4-turbo-preview  # Default
```

**Ollama:**
```bash
USE_OLLAMA=true
OLLAMA_MODEL=codellama:13b
OLLAMA_BASE_URL=http://localhost:11434
```

### Model Comparison

| Model | Speed | Cost | Quality | Best For |
|-------|-------|------|---------|----------|
| GPT-4 Turbo | Fast | High | Excellent | Production |
| GPT-3.5 Turbo | Very Fast | Low | Good | Development |
| CodeLlama 13B | Medium | Free | Good | Code Analysis |
| Llama2 13B | Medium | Free | Fair | General QA |

## Project Structure

```
Code-QA-Crew/
├── qa_cli.py              # CLI interface
├── qa_tools.py            # LangChain analysis tools
├── qa_crew.py             # CrewAI multi-agent system
├── qa_crewai_tools.py     # CrewAI tool wrappers
├── demo_qa_crew.py        # Standalone demo
├── requirements.txt       # Dependencies
├── .env.example           # Configuration template
├── examples/              # Usage examples
├── tests/                 # Test suite
└── docs/                  # Documentation
```

## Examples

### Python Project
```bash
python qa_crew.py --path ./backend --type python
```

### React Project
```bash
python qa_crew.py --path ./frontend --type react --port 3000
```

### Mixed Project
```bash
python qa_crew.py --path ./fullstack --type mixed
```

### Development Workflow
```bash
# Quick check during development
python qa_cli.py --quick --path ./src

# Pre-commit validation
python qa_crew.py --path ./project --type mixed

# Localhost-only check
python qa_cli.py --localhost-only --port 3000
```

## Testing

Run the test suite:
```bash
python tests/test_qa_tools.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Run QA analysis on your changes
4. Ensure all scores are ≥ 7/10
5. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) file for details.
