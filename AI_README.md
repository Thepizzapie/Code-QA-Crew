# AI Agent Technical Guide - QA Crew System

## System Overview for AI Agents

This is a multi-agent code analysis system with three main entry points. AI agents (like Cursor) should understand the following architecture:

## Core Files and Entry Points

### Primary Entry Point: `qa_crew.py`
- **Main Command**: `python qa_crew.py --path <target_path>`
- **Interactive Mode**: Shows menu with agent selection or natural language input
- **Architecture**: CrewAI framework with 11 specialized agents
- **Dependencies**: `crewai`, `qa_crewai_tools`

### Enhanced Version: `qa_crew_enhanced.py`
- **Command**: `python qa_crew_enhanced.py --path <target_path>`
- **Architecture**: Extended CrewAI with 9 specialized agents
- **Additional Features**: Debug logging, enhanced reporting
- **Dependencies**: Same as basic version

### Tools Implementation: `qa_crewai_tools.py`
- **Purpose**: Contains all analysis tools used by agents
- **Key Functions**: 31 analysis tools for different code aspects
- **Pattern**: Each tool returns structured analysis data
- **Integration**: Imported by both crew systems

## Agent Architecture

### Basic CrewAI System (qa_crew.py)
```python
# 11 Agents with specific roles:
agents = {
    'manager': QA Team Manager (delegation only),
    'cs_professor': Software Architecture Analyst,
    'python_expert': Senior Python Developer,
    'react_expert': Senior React/Frontend Developer,
    'swift_expert': Senior iOS/macOS Developer,
    'database_expert': Database Architect,
    'devops_expert': DevOps Engineer,
    'documentation_expert': Technical Documentation Specialist,
    'tech_expert': Technology Stack Specialist,
    'deps_expert': Dependency Management Specialist,
    'security_expert': Security Analyst,
    'qa_tester': Quality Assurance Engineer
}
```

### Tool Assignment Pattern
Each agent has specific tools assigned based on expertise:
```python
# Example: Security Expert
security_expert = Agent(
    role="Security Analyst",
    tools=[scan_security_vulnerabilities, check_best_practices],
    # ... other config
)
```

## Key Functions for AI Understanding

### Main Analysis Flow
1. **Path Input**: User provides `--path <directory>`
2. **Agent Selection**: Interactive menu or command line args
3. **Task Creation**: `create_tasks()` generates analysis tasks
4. **Execution**: CrewAI runs agents with assigned tools
5. **Output**: JSON results with findings and recommendations

### Tool Execution Pattern
```python
# Tools in qa_crewai_tools.py follow this pattern:
@tool("tool_name")
def analysis_function(code_path: str) -> str:
    """Tool description for AI agent"""
    # Analysis logic
    return json.dumps(results)
```

### Interactive Mode Logic
```python
# In main() function:
if not args.agents and not args.request:
    # Show interactive menu
    choice = input("Enter 1 for agent selection or 2 for natural language")
    if choice == '1':
        # Agent number selection
    elif choice == '2':
        # Natural language processing
```

## Configuration Files

### Agent Definitions: `config/agents.yaml` and `config/agents_enhanced.yaml`
- Defines agent roles, goals, and backstories
- Maps tools to agents
- Used by enhanced crew system

### Task Definitions: `config/tasks.yaml` and `config/tasks_enhanced.yaml`
- Defines analysis tasks for each agent
- Specifies expected outputs
- Controls task execution order

## Environment Setup

### Required Environment Variables
```bash
# OpenAI (recommended)
OPENAI_API_KEY=your_key_here

# Or Ollama (local AI)
USE_OLLAMA=true
OLLAMA_MODEL=codellama:13b
OLLAMA_BASE_URL=http://localhost:11434
```

### Dependencies
```python
# Core requirements from requirements.txt:
crewai>=0.28.8
openai>=1.12.0
python-decouple>=3.8
# ... see requirements.txt for full list
```

## Analysis Capabilities

### Supported Project Types
- **Python**: Syntax, PEP 8, frameworks (Django, Flask, FastAPI)
- **React**: Components, hooks, performance, accessibility
- **Swift**: iOS/macOS, SwiftUI, memory management
- **SQL**: Query validation, injection risks
- **Mixed**: Multi-language projects

### Tool Categories
1. **Code Structure**: `analyze_code_structure`, `analyze_code_complexity`
2. **Language-Specific**: `check_python_syntax`, `analyze_react_components`, `swift_swiftui_analysis`
3. **Security**: `scan_security_vulnerabilities`, `security_vulnerability_scan`
4. **Dependencies**: `check_package_dependencies`, `dependency_vulnerability_check`
5. **Quality**: `run_general_qa_tests`, `check_best_practices`

## Output Format

### Standard Output Structure
```json
{
  "executive_summary": {
    "overall_quality_score": "score/100",
    "key_findings": ["finding1", "finding2"],
    "critical_issues": ["issue1", "issue2"]
  },
  "detailed_analysis": {
    "agent_name": "analysis_results"
  },
  "recommendations": ["rec1", "rec2"]
}
```

## Error Handling

### Common Issues
1. **Missing API Key**: System falls back to Ollama if configured
2. **Invalid Path**: Validation in `_sanitize_path()` function
3. **Tool Failures**: Individual tool errors don't stop entire analysis
4. **Import Errors**: Graceful degradation when optional dependencies missing

## Integration Points for AI Agents

### Code Analysis Entry Points
- Use `qa_crew.py` for standard analysis
- Use `qa_crew_enhanced.py` for detailed analysis with debug info
- Direct tool access via `qa_crewai_tools.py` functions

### Extending the System
- Add new tools to `qa_crewai_tools.py`
- Update agent configurations in `config/` files
- Modify task assignments in crew classes

### Natural Language Interface
The system accepts natural language requests like:
- "Check my Swift app for bugs and security issues"
- "Analyze Python code for performance problems"
- "Review React components for accessibility"

This triggers automatic agent selection based on keyword detection in `run_natural_language_analysis()` function. 