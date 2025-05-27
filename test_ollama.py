#!/usr/bin/env python3

"""
Test script to verify Ollama configuration
"""

import os
from decouple import config

def test_ollama_config():
    """Test Ollama configuration"""
    print("🧪 Testing Ollama Configuration")
    print("=" * 40)
    
    # Test environment variables
    use_ollama = config('USE_OLLAMA', default=False, cast=bool)
    
    if use_ollama:
        ollama_model = config('OLLAMA_MODEL', default='llama2')
        ollama_base_url = config('OLLAMA_BASE_URL', default='http://localhost:11434')
        
        print(f"✅ USE_OLLAMA: {use_ollama}")
        print(f"✅ OLLAMA_MODEL: {ollama_model}")
        print(f"✅ OLLAMA_BASE_URL: {ollama_base_url}")
        
        # Test connection
        import requests
        try:
            response = requests.get(f"{ollama_base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                print(f"✅ Ollama connection successful")
                print(f"📋 Available models: {len(models)}")
                for model in models:
                    print(f"   - {model.get('name', 'Unknown')}")
                
                # Check if configured model is available
                model_names = [m.get('name', '') for m in models]
                if any(ollama_model in name for name in model_names):
                    print(f"✅ Configured model '{ollama_model}' is available")
                else:
                    print(f"⚠️ Configured model '{ollama_model}' not found")
                    print(f"💡 Run: ollama pull {ollama_model}")
            else:
                print(f"❌ Ollama connection failed: HTTP {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Cannot connect to Ollama: {e}")
            print("💡 Make sure Ollama is running: ollama serve")
    else:
        # Test OpenAI configuration
        openai_key = config('OPENAI_API_KEY', default=None)
        if openai_key:
            print(f"✅ OpenAI API key configured")
            print(f"🔑 Key length: {len(openai_key)} characters")
        else:
            print("❌ No AI model configured")
            print("💡 Set either OPENAI_API_KEY or USE_OLLAMA=true in .env")

def test_qa_crew_import():
    """Test QA Crew import"""
    print("\n🧪 Testing QA Crew Import")
    print("=" * 40)
    
    try:
        from qa_crew import QACrew
        print("✅ QA Crew import successful")
        
        # Test agent creation
        crew = QACrew()
        print(f"✅ QA Crew initialized with {len(crew.agents)} agents")
        
        agent_names = list(crew.agents.keys())
        print(f"👥 Agents: {', '.join(agent_names)}")
        
    except Exception as e:
        print(f"❌ QA Crew import failed: {e}")

if __name__ == "__main__":
    test_ollama_config()
    test_qa_crew_import()
    
    print("\n🎯 Next Steps:")
    print("1. If using Ollama: ollama serve")
    print("2. Test analysis: python qa_cli.py --crew")
    print("3. See OLLAMA_SETUP.md for detailed setup") 