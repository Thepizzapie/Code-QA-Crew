#!/usr/bin/env python3
"""
Basic Usage Example - Code QA Crew
Demonstrates how to use the QA Crew for code analysis
"""

import os
import sys

# Add parent directory to path to import qa_crew
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qa_crew import QACrew

def main():
    """Basic usage example"""
    
    print("🤖 Code QA Crew - Basic Usage Example")
    print("=" * 50)
    
    # Initialize the QA Crew
    qa_crew = QACrew()
    
    # Example 1: Analyze current directory
    print("\n📁 Example 1: Analyzing current directory")
    current_dir = os.getcwd()
    result = qa_crew.run_analysis(current_dir, project_type="mixed")
    print("✅ Analysis complete!")
    
    # Example 2: Analyze a Python project
    print("\n🐍 Example 2: Python project analysis")
    python_project = "./examples"  # Analyze the examples directory
    result = qa_crew.run_analysis(python_project, project_type="python")
    print("✅ Python analysis complete!")
    
    # Example 3: Analyze with localhost check
    print("\n🌐 Example 3: Analysis with localhost check")
    result = qa_crew.run_analysis(current_dir, project_type="mixed", localhost_port="3000")
    print("✅ Analysis with localhost check complete!")
    
    print("\n🎉 All examples completed successfully!")
    print("📊 Check the generated reports for detailed analysis results.")

if __name__ == "__main__":
    main() 