# 🦙 Ollama Setup Guide

Complete guide for using Ollama (local AI) instead of OpenAI API keys with the Code QA Crew.

## 🎯 Why Use Ollama?

- **🆓 Free**: No API costs
- **🔒 Private**: All processing happens locally
- **⚡ Fast**: No network latency after initial setup
- **🌐 Offline**: Works without internet connection
- **🎛️ Control**: Full control over model selection and parameters

## 📋 Prerequisites

- **RAM**: 8GB minimum (16GB+ recommended for larger models)
- **Storage**: 4-20GB per model
- **OS**: Windows, macOS, or Linux

## 🚀 Installation

### Windows
1. Download from https://ollama.ai
2. Run the installer
3. Ollama will start automatically

### macOS
```bash
# Using Homebrew (recommended)
brew install ollama

# Or download from https://ollama.ai
```

### Linux
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

## 🤖 Model Selection

### For Code Analysis (Recommended)
```bash
# Best for code analysis
ollama pull codellama:13b

# Larger, more capable (requires 16GB+ RAM)
ollama pull codellama:34b

# Smaller, faster (8GB RAM)
ollama pull codellama:7b
```

### For General QA
```bash
# Balanced performance
ollama pull llama2:13b

# Lightweight option
ollama pull llama2:7b

# Latest Mistral model
ollama pull mistral:7b
```

### For Advanced Analysis
```bash
# Latest Llama model (requires 16GB+ RAM)
ollama pull llama3:8b

# Code-specific fine-tuned model
ollama pull deepseek-coder:6.7b
```

## ⚙️ Configuration

### 1. Start Ollama Service
```bash
# Start the Ollama service
ollama serve
```

### 2. Test Your Model
```bash
# Test the model works
ollama run codellama:13b "Write a Python function to reverse a string"
```

### 3. Configure QA Crew
Create or update your `.env` file:

```bash
# Ollama Configuration
USE_OLLAMA=true
OLLAMA_MODEL=codellama:13b
OLLAMA_BASE_URL=http://localhost:11434

# Optional: Remove OpenAI key if switching completely
# OPENAI_API_KEY=your_key_here
```

## 🧪 Testing the Setup

### Quick Test
```bash
# Test with current directory
python qa_cli.py --crew

# Test with specific project
python qa_cli.py --path ./my-project --crew
```

### Verify Ollama Connection
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Should return list of installed models
```

## 📊 Performance Comparison

| Model | Size | RAM Needed | Speed | Code Quality | Best For |
|-------|------|------------|-------|--------------|----------|
| codellama:7b | 3.8GB | 8GB | Fast | Good | Quick checks |
| codellama:13b | 7.3GB | 16GB | Medium | Excellent | Code analysis |
| codellama:34b | 19GB | 32GB | Slow | Outstanding | Deep analysis |
| llama2:7b | 3.8GB | 8GB | Fast | Fair | General QA |
| llama2:13b | 7.3GB | 16GB | Medium | Good | Balanced use |
| mistral:7b | 4.1GB | 8GB | Fast | Good | Mixed projects |

## 🔧 Advanced Configuration

### Custom Ollama Port
If you need to run Ollama on a different port:

```bash
# Start Ollama on custom port
OLLAMA_HOST=0.0.0.0:11435 ollama serve
```

Update `.env`:
```bash
OLLAMA_BASE_URL=http://localhost:11435
```

### Multiple Models
You can switch between models by updating the `.env` file:

```bash
# For Python-heavy projects
OLLAMA_MODEL=codellama:13b

# For React/JavaScript projects
OLLAMA_MODEL=llama2:13b

# For security analysis
OLLAMA_MODEL=mistral:7b
```

### Model Parameters
Create `ollama_config.json` for custom parameters:

```json
{
  "temperature": 0.1,
  "top_p": 0.9,
  "max_tokens": 2048,
  "stop": ["```", "---"]
}
```

## 🚨 Troubleshooting

### Ollama Not Starting
```bash
# Check if service is running
ps aux | grep ollama

# Restart service
ollama serve

# Check logs
ollama logs
```

### Model Not Found
```bash
# List installed models
ollama list

# Pull missing model
ollama pull codellama:13b
```

### Memory Issues
```bash
# Check available RAM
free -h  # Linux
vm_stat  # macOS

# Use smaller model if needed
ollama pull codellama:7b
```

### Connection Issues
```bash
# Test connection
curl http://localhost:11434/api/version

# Check firewall settings
# Ensure port 11434 is not blocked
```

## 🎯 Usage Examples

### Basic Code Analysis
```bash
# Quick analysis with Ollama
python qa_cli.py --crew

# Specific project type
python qa_cli.py --path ./backend --type python --crew
```

### With Localhost Checking
```bash
# Full analysis including demo site
python qa_cli.py --path ./frontend --crew --port 3000
```

### Switching Models
```bash
# Update .env for different model
echo "OLLAMA_MODEL=llama2:13b" >> .env

# Run analysis
python qa_cli.py --crew
```

## 💡 Tips for Best Results

### Model Selection
- **Code Analysis**: Use `codellama:13b` or `codellama:34b`
- **Security Review**: Use `mistral:7b` or `llama2:13b`
- **Quick Checks**: Use `codellama:7b` or `llama2:7b`
- **Mixed Projects**: Use `llama2:13b`

### Performance Optimization
- **Close other applications** to free up RAM
- **Use SSD storage** for faster model loading
- **Restart Ollama** if responses become slow
- **Monitor system resources** during analysis

### Quality Improvements
- **Use larger models** for more detailed analysis
- **Run multiple passes** with different models
- **Combine with OpenAI** for critical projects
- **Review outputs** as local models may vary

## 🔄 Switching Back to OpenAI

To switch back to OpenAI API:

1. Update `.env`:
```bash
USE_OLLAMA=false
OPENAI_API_KEY=your_openai_key_here
```

2. Or comment out Ollama settings:
```bash
# USE_OLLAMA=true
# OLLAMA_MODEL=codellama:13b
# OLLAMA_BASE_URL=http://localhost:11434
OPENAI_API_KEY=your_openai_key_here
```

## 📚 Additional Resources

- **Ollama Documentation**: https://ollama.ai/docs
- **Model Library**: https://ollama.ai/library
- **Community Models**: https://huggingface.co/models?other=ollama
- **Performance Benchmarks**: https://ollama.ai/blog/performance

---

**Need Help?** Check the troubleshooting section above or refer to the main [README.md](README.md) for general usage instructions. 