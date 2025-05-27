#!/usr/bin/env python3
"""
Code QA Crew - Setup Script
Helps new users get started quickly with the QA analysis system.
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header():
    print("🤖 Code QA Crew - Setup Assistant")
    print("=" * 50)
    print("Setting up your professional code analysis environment...")
    print()

def check_python_version():
    """Check if Python version is compatible"""
    print("1️⃣ Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} - Compatible!")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} - Need Python 3.8+")
        print("   Please upgrade Python and try again.")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("\n2️⃣ Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("   ✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print("   ⚠️ Some dependencies failed to install (this is common with CrewAI)")
        print("   🔍 Checking if core functionality works...")
        
        # Test if the basic QA system works despite dependency issues
        try:
            import qa_tools
            print("   ✅ Core QA tools are available!")
            return True
        except ImportError:
            print("   ❌ Core dependencies missing")
            print("   Try running: pip install -r requirements.txt")
            return False

def setup_environment():
    """Help user set up environment variables"""
    print("\n3️⃣ Setting up environment...")
    
    env_file = Path(".env")
    if env_file.exists():
        print("   ✅ .env file already exists")
        return True
    
    print("   Choose your AI provider:")
    print("   A) OpenAI API (recommended, requires API key)")
    print("   B) Ollama (free, local AI)")
    print("   C) Skip for now")
    
    choice = input("   Enter choice (A/B/C): ").upper().strip()
    
    if choice == "A":
        api_key = input("   Enter your OpenAI API key: ").strip()
        if api_key:
            with open(".env", "w") as f:
                f.write(f"OPENAI_API_KEY={api_key}\n")
            print("   ✅ OpenAI configuration saved!")
            return True
        else:
            print("   ⚠️ No API key provided, skipping...")
            return False
    
    elif choice == "B":
        print("   Setting up Ollama configuration...")
        with open(".env", "w") as f:
            f.write("USE_OLLAMA=true\n")
            f.write("OLLAMA_MODEL=codellama:13b\n")
            f.write("OLLAMA_BASE_URL=http://localhost:11434\n")
        print("   ✅ Ollama configuration saved!")
        print("   📝 Next steps:")
        print("      1. Install Ollama from https://ollama.ai")
        print("      2. Run: ollama pull codellama:13b")
        print("      3. Run: ollama serve")
        return True
    
    else:
        print("   ⚠️ Skipping environment setup")
        print("   You can create .env file manually later")
        return False

def test_installation():
    """Test if the installation works"""
    print("\n4️⃣ Testing installation...")
    try:
        # Test basic import
        import qa_tools
        print("   ✅ QA tools imported successfully!")
        
        # Test CLI help
        result = subprocess.run([sys.executable, "qa_cli.py", "--help"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("   ✅ CLI interface working!")
            return True
        else:
            print("   ❌ CLI test failed")
            return False
            
    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        return False

def show_next_steps():
    """Show user what to do next"""
    print("\n🎉 Setup Complete!")
    print("=" * 50)
    print("🚀 Ready to analyze your code! Try these commands:")
    print()
    print("   # Quick test on current directory")
    print("   python qa_cli.py --quick")
    print()
    print("   # Analyze a specific project")
    print("   python qa_cli.py --path ./your-project")
    print()
    print("   # Full analysis with localhost check")
    print("   python qa_cli.py --path ./your-project --port 3000")
    print()
    print("📚 Documentation:")
    print("   - README.md - Complete guide")
    print("   - TEAM_GUIDE.md - Detailed usage")
    print("   - OLLAMA_SETUP.md - Local AI setup")
    print()
    print("🤖 For Cursor integration, see the README.md file!")

def main():
    """Main setup process"""
    print_header()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n⚠️ Setup incomplete - dependency installation failed")
        sys.exit(1)
    
    # Setup environment
    env_setup = setup_environment()
    
    # Test installation
    if test_installation():
        show_next_steps()
        if not env_setup:
            print("\n⚠️ Note: You'll need to configure AI provider in .env file")
            print("   See README.md for instructions")
    else:
        print("\n❌ Setup failed during testing")
        print("   Check the error messages above and try manual setup")
        sys.exit(1)

if __name__ == "__main__":
    main() 