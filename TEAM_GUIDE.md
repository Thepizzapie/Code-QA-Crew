# 🎯 Team Guide - Code QA Crew CLI

## 🚀 **Simple Commands for Your Team**

### **AI Model Options:**
- **OpenAI API** (recommended): Fast, high-quality analysis
- **Ollama** (free): Local AI, no API costs, private
- **Setup**: See [OLLAMA_SETUP.md](OLLAMA_SETUP.md) for local AI setup

### **Basic Usage Pattern:**
```bash
python qa_cli.py --path [FOLDER]                # Quick analysis (default)
python qa_cli.py --path [FOLDER] --crew         # Full CrewAI analysis with agents
python qa_cli.py --path [FOLDER] --port [PORT]  # Analysis + localhost check
python qa_cli.py --path [FOLDER] --crew --port [PORT]  # Full analysis + localhost
```

## 📋 **Common Team Scenarios**

### **1. Analyze Code Only (Default)**
```bash
# Analyze frontend code without localhost check
python qa_cli.py --path ./frontend --type react
```
**Use this**: Code quality analysis without demo site checking

### **2. Check if Demo Site is Running**
```bash
# Quick check - just the port
python qa_cli.py --localhost-only --port 3000
```
**Use this**: Before presentations to verify demo site is up

### **3. Analyze Frontend + Check Demo Site**
```bash
# Point to frontend folder and check port 3000
python qa_cli.py --path ./frontend --type react --port 3000
```
**Use this**: Full analysis of React frontend with demo site check

### **3. Analyze Backend + Check API**
```bash
# Point to backend folder and check API port
python qa_cli.py --path ./backend --type python --port 8000
```
**Use this**: Analyze Python backend and check if API is running

### **4. Check Multiple Services**
```bash
# Check frontend, backend, and database ports
python qa_cli.py --localhost-only --ports 3000,8000,5432
```
**Use this**: Verify entire stack is running

### **5. Analyze Specific Project Folder**
```bash
# Analyze any project folder without localhost check
python qa_cli.py --path /path/to/project --type mixed --code-only
```
**Use this**: Code quality analysis only

## 🎯 **Team Workflow Examples**

### **Frontend Developer:**
```bash
# Check React app and demo site
python qa_cli.py --path ./src --type react --port 3000
```

### **Backend Developer:**
```bash
# Check Python API and service
python qa_cli.py --path ./api --type python --port 8000
```

### **Full-Stack Developer:**
```bash
# Check both frontend and backend
python qa_cli.py --path ./frontend --port 3000
python qa_cli.py --path ./backend --port 8000
```

### **DevOps/QA Team:**
```bash
# Check entire stack
python qa_cli.py --localhost-only --ports 3000,8000,5432,6379
```

## 📁 **Path Examples**

| Path | Description |
|------|-------------|
| `./frontend` | Frontend folder |
| `./backend` | Backend folder |
| `./src` | Source code folder |
| `../other-project` | Different project |
| `/full/path/to/project` | Absolute path |
| `.` | Current directory |

## 🌐 **Port Examples**

| Port | Common Use |
|------|------------|
| `3000` | React development server |
| `8000` | Python/Django development |
| `5000` | Flask applications |
| `4200` | Angular development |
| `8080` | Alternative web servers |
| `5432` | PostgreSQL database |
| `6379` | Redis cache |

## ⚡ **Quick Reference**

### **Just Check Port:**
```bash
python qa_cli.py --localhost-only --port 3000
```

### **Just Analyze Code:**
```bash
python qa_cli.py --path ./my-folder --code-only
```

### **Full Analysis:**
```bash
python qa_cli.py --path ./my-folder --port 3000
```

### **Multiple Ports:**
```bash
python qa_cli.py --localhost-only --ports 3000,8000,5000
```

## 🎯 **For Team Leaders**

### **Pre-Demo Checklist:**
```bash
# 1. Check demo site
python qa_cli.py --localhost-only --port 3000

# 2. Quick code quality check
python qa_cli.py --path ./demo-project --type react --quick
```

### **Code Review Process:**
```bash
# Analyze the feature branch
python qa_cli.py --path ./feature-folder --type mixed --code-only
```

### **Deployment Verification:**
```bash
# Check all services are running
python qa_cli.py --localhost-only --ports 3000,8000,5432
```

## 🚨 **Troubleshooting**

### **Path doesn't exist:**
- Check the folder path is correct
- Use `ls` (Mac/Linux) or `dir` (Windows) to verify

### **Port not accessible:**
- Make sure the service is running
- Check the port number is correct
- Verify no firewall blocking

### **Analysis fails:**
- Check file permissions
- Ensure project type is correct
- Verify dependencies are installed

## 💡 **Pro Tips for Teams**

1. **Always check localhost before demos**
2. **Use `--localhost-only` for quick checks**
3. **Specify project type for better analysis**
4. **Use `--ports` to check multiple services**
5. **Save reports with `--output custom-report.md`**

## 🎯 **Ready to Use!**

Your team can now easily:
- ✅ Point to any folder: `--path ./folder`
- ✅ Check any port: `--port 3000`
- ✅ Analyze code quality
- ✅ Verify demo sites are running
- ✅ Generate comprehensive reports

**Start with**: `python qa_cli.py --path ./your-folder --port 3000` 