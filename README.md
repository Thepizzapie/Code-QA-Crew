# 🎯 Code QA Crew

A comprehensive AI-powered code quality assurance system that analyzes code and validates localhost applications.

## 🚀 Quick Start

### **Analyze Code Only (Default):**
```bash
python qa_cli.py --path ./your-project
```

### **Analyze Code + Check Demo Site:**
```bash
python qa_cli.py --path ./your-project --port 3000
```

### **Check Demo Site Only:**
```bash
python qa_cli.py --localhost-only --port 3000
```

## 📋 Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up environment:**
Create a `.env` file with:
```
OPENAI_API_KEY=your-openai-api-key
```

3. **Test the system:**
```bash
python qa_cli.py --localhost-only --port 3000
```

## 🎯 Usage

### **Basic Pattern:**
```bash
python qa_cli.py --path [FOLDER] --port [PORT]
```

### **Common Commands:**
- `--path ./frontend` - Analyze frontend code only (default)
- `--path ./frontend --port 3000` - Analyze frontend + check demo
- `--localhost-only --port 3000` - Quick port check only
- `--localhost-only --ports 3000,8000,5000` - Check multiple ports
- `--path ./backend --port 8000` - Analyze backend + check API

## 📁 Project Structure

```
qa-crew/
├── qa_cli.py              # Command-line interface
├── qa_tools.py            # QA analysis tools
├── demo_qa_crew.py        # Main QA crew logic
├── config/
│   ├── agents.yaml        # AI agent configurations
│   └── tasks.yaml         # Task definitions
├── requirements.txt       # Dependencies
├── TEAM_GUIDE.md         # Detailed team usage guide
├── AGENT_PROMPT_SHORT.md # Agent validation prompt
└── README.md             # This file
```

## 🔧 Features

- ✅ **Code Quality Analysis** - Syntax, style, best practices
- ✅ **Security Scanning** - Vulnerability detection
- ✅ **Localhost Validation** - Demo site accessibility
- ✅ **Performance Monitoring** - Response time measurement
- ✅ **Multi-Technology Support** - Python, React, SQL, mixed
- ✅ **Automated Reporting** - Comprehensive markdown reports

## 📖 Documentation

- **[TEAM_GUIDE.md](TEAM_GUIDE.md)** - Complete usage guide for teams
- **[AGENT_PROMPT_SHORT.md](AGENT_PROMPT_SHORT.md)** - Prompt for AI agents

## 🎯 For Teams

This system is designed for development teams to:
1. **Validate demo sites** before presentations
2. **Ensure code quality** before deployment
3. **Automate security scanning** in CI/CD pipelines
4. **Generate comprehensive reports** for code reviews

## 🤖 For AI Agents

Use the validation prompt in `AGENT_PROMPT_SHORT.md` to ensure all generated code meets quality standards.

## 🚨 Requirements

- Python 3.8+
- OpenAI API key
- Internet connection for security scanning

## 📞 Support

For issues or questions, refer to the `TEAM_GUIDE.md` for detailed troubleshooting and usage examples. 