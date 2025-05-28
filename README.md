# QA Crew System - Multi-Architecture Code Analysis Platform

## Overview

This project provides a comprehensive code quality analysis platform for automated code review, security scanning, and quality assessment across multiple programming languages.

## System Architecture

### CrewAI Multi-Agent System (`qa_crew.py`)
- **Basic Configuration**: 5 specialized agents (cs_professor, tech_expert, deps_expert, security_expert, qa_tester)
- **Enhanced Configuration**: 9 specialized agents including Python, React, Swift, Database, DevOps, Dependencies, Security, CS Professor, and QA experts
- **Approach**: Traditional multi-agent framework with predefined roles and sequential task execution
- **Best For**: Comprehensive analysis with detailed specialist reports and structured workflows

**Agents:**
- **CS Professor**: Architecture and algorithmic analysis
- **Tech Stack Expert**: Python, React, SQL analysis  
- **Dependencies Expert**: Package management and security
- **Security Expert**: Vulnerability assessment
- **QA Tester**: Quality synthesis and final reporting

**Usage:**
```bash
# Interactive mode - shows menu with choices
python qa_crew.py --path ./project

# Or specify project type
python qa_crew.py --path ./project --type python
```

**Interactive Options:**
1. **Simple Agent Selection** - Pick agents by number (1-11) or "all"
2. **Natural Language Request** - Describe what you want in plain English

**Command Line Options:**
```bash
# Direct agent selection
python qa_crew.py --path ./project --agents "1,2,10"

# Natural language request
python qa_crew.py --path ./project --request "analyze security vulnerabilities"
```

## Installation

### Prerequisites
- Python 3.8 or higher
- OpenAI API Key (recommended) or Ollama for local AI

### Setup
```bash
# Clone and install
git clone <repository-url>
cd crew_test
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys
```

### Environment Configuration
```bash
# OpenAI (Recommended)
OPENAI_API_KEY=your_api_key_here

# Or Ollama (Local AI)
USE_OLLAMA=true
OLLAMA_MODEL=codellama:13b
OLLAMA_BASE_URL=http://localhost:11434
```

## Quick Start

```bash
# Basic interactive analysis
python qa_crew.py --path .

# The system will show you two options:
# 1. Simple Agent Selection (pick by numbers)
# 2. Natural Language Request (describe in plain English)
```

## Supported Technologies

### Programming Languages
- **Python**: Syntax, PEP 8, performance, frameworks (Django, Flask, FastAPI)
- **JavaScript/React**: Components, hooks, performance, accessibility
- **Swift**: iOS/macOS development, SwiftUI, memory management
- **SQL**: Query validation, injection risks, optimization

### Project Types
- **Python**: Pure Python projects and scripts
- **React**: Frontend applications and components
- **Swift**: iOS/macOS applications
- **Mixed**: Full-stack projects with multiple technologies

## Analysis Capabilities

### Code Quality Assessment
- Syntax validation and style compliance
- Architectural analysis and design patterns
- Performance optimization recommendations
- Best practices verification

### Security Analysis
- OWASP Top 10 vulnerability scanning
- Hardcoded credential detection
- SQL injection and XSS prevention
- Security configuration assessment

### Dependency Management
- Package vulnerability scanning
- Version compatibility analysis
- Supply chain security assessment
- Dependency health scoring

## Configuration

### Agent Configuration
Customize agents in `config/agents.yaml` or `config/agents_enhanced.yaml`:
```yaml
cs_professor:
  role: "Software Architecture Analyst"
  goal: "Analyze code structure and design patterns"
  tools: ["analyze_code_structure", "complexity_metrics"]
```

## Project Structure

```
crew_test/
├── qa_crew.py              # Main CrewAI multi-agent system
├── qa_crew_enhanced.py     # Enhanced multi-agent system
├── qa_crewai_tools.py      # Analysis tool implementations
├── config/                 # Agent and task configurations
├── requirements.txt        # Dependencies
└── README.md              # This file
```

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Technical Specifications

- **Python**: 3.8+ required
- **AI Models**: OpenAI GPT-4/3.5, Ollama (CodeLlama, Llama2, Mistral)
- **Architecture**: Multi-agent systems with tool integration
- **Security**: OWASP compliance, local processing, privacy protection
