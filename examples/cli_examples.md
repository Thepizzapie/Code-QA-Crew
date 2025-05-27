# CLI Usage Examples

This document provides practical examples of using the Code QA Crew command-line interfaces.

## Quick Start Examples

### 1. Basic Analysis
```bash
# Analyze current directory
python qa_cli.py --quick

# Analyze specific project
python qa_cli.py --path "./my-project" --quick
```

### 2. Full CrewAI Multi-Agent Analysis
```bash
# Complete analysis with all 5 AI agents
python qa_crew.py --path "./my-project" --type python

# Mixed project (Python + React + SQL)
python qa_crew.py --path "./fullstack-app" --type mixed

# React project with localhost check
python qa_crew.py --path "./frontend" --type react --port 3000
```

### 3. Demo Analysis (Fastest)
```bash
# Quick standalone analysis
python demo_qa_crew.py --path "./my-project" --type python

# Mixed project demo
python demo_qa_crew.py --path "./fullstack-app" --type mixed
```

## Project Type Examples

### Python Projects
```bash
# Django project
python qa_crew.py --path "./django-app" --type python

# Flask API
python qa_crew.py --path "./flask-api" --type python --port 5000

# Data science project
python qa_crew.py --path "./ml-project" --type python
```

### React Projects
```bash
# Create React App
python qa_crew.py --path "./react-app" --type react --port 3000

# Next.js project
python qa_crew.py --path "./nextjs-app" --type react --port 3000

# React Native
python qa_crew.py --path "./react-native-app" --type react
```

### Mixed Projects
```bash
# Full-stack application
python qa_crew.py --path "./fullstack" --type mixed --port 3000

# Microservices architecture
python qa_crew.py --path "./microservices" --type mixed

# Monorepo
python qa_crew.py --path "./monorepo" --type mixed
```

## Advanced Usage

### Localhost-Only Checks
```bash
# Check if development server is running
python qa_cli.py --localhost-only --port 3000

# Check multiple services
python qa_cli.py --localhost-only --port 3000
python qa_cli.py --localhost-only --port 8000
python qa_cli.py --localhost-only --port 5000
```

### Development Workflow
```bash
# 1. Pre-development assessment
python qa_cli.py --quick --path ./project

# 2. During development (fast checks)
python demo_qa_crew.py --path ./src --type python

# 3. Pre-commit validation
python qa_crew.py --path ./project --type mixed

# 4. Production readiness check
python qa_crew.py --path ./project --type mixed --port 3000
```

## Real-World Examples

### E-commerce Application
```bash
# Backend API analysis
python qa_crew.py --path "./ecommerce-api" --type python --port 8000

# Frontend analysis
python qa_crew.py --path "./ecommerce-frontend" --type react --port 3000

# Full application analysis
python qa_crew.py --path "./ecommerce" --type mixed
```

### Data Pipeline
```bash
# ETL scripts analysis
python qa_crew.py --path "./data-pipeline" --type python

# Database scripts
python qa_crew.py --path "./database" --type sql

# Complete pipeline
python qa_crew.py --path "./data-project" --type mixed
```

### Microservices
```bash
# Individual service
python qa_crew.py --path "./user-service" --type python --port 8001

# API Gateway
python qa_crew.py --path "./api-gateway" --type python --port 8000

# All services
python qa_crew.py --path "./microservices" --type mixed
```

## Tips and Best Practices

### Performance Tips
- Use `--quick` for fast development checks
- Use `demo_qa_crew.py` for standalone analysis without AI agents
- Use full `qa_crew.py` for comprehensive production-ready analysis

### CI/CD Integration
```bash
# In your CI pipeline
python qa_cli.py --quick --path ./src
if [ $? -eq 0 ]; then
    echo "✅ QA checks passed"
else
    echo "❌ QA checks failed"
    exit 1
fi
```

### Team Workflow
```bash
# Code review preparation
python qa_crew.py --path ./feature-branch --type mixed

# Release candidate validation
python qa_crew.py --path ./release --type mixed --port 3000
``` 