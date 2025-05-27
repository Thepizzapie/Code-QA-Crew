#!/usr/bin/env python3

from qa_tools import (
    analyze_code_structure,
    check_python_syntax,
    scan_security_vulnerabilities,
    check_package_dependencies,
    run_general_qa_tests
)

def run_qa_analysis(target_path):
    print("🔍 FULL QA ANALYSIS")
    print("=" * 60)
    print(f"📁 Target: {target_path}")
    print()
    
    # 1. Code Structure
    print("1️⃣ Analyzing code structure...")
    try:
        result = analyze_code_structure.invoke({"folder_path": target_path})
        print("✅ Code structure analysis completed")
        print(result[:500] + "..." if len(result) > 500 else result)
    except Exception as e:
        print(f"❌ Failed: {e}")
    
    print("\n" + "="*60 + "\n")
    
    # 2. Python Syntax
    print("2️⃣ Checking Python syntax...")
    try:
        result = check_python_syntax.invoke({"code_path": target_path})
        print("✅ Python syntax check completed")
        print(result[:500] + "..." if len(result) > 500 else result)
    except Exception as e:
        print(f"❌ Failed: {e}")
    
    print("\n" + "="*60 + "\n")
    
    # 3. Security Scan
    print("3️⃣ Running security scan...")
    try:
        result = scan_security_vulnerabilities.invoke({"code_path": target_path})
        print("✅ Security scan completed")
        print(result[:500] + "..." if len(result) > 500 else result)
    except Exception as e:
        print(f"❌ Failed: {e}")
    
    print("\n" + "="*60 + "\n")
    
    # 4. Dependencies
    print("4️⃣ Checking dependencies...")
    try:
        result = check_package_dependencies.invoke({"code_path": target_path})
        print("✅ Dependencies check completed")
        print(result[:500] + "..." if len(result) > 500 else result)
    except Exception as e:
        print(f"❌ Failed: {e}")
    
    print("\n" + "="*60 + "\n")
    
    # 5. General QA
    print("5️⃣ Running general QA tests...")
    try:
        result = run_general_qa_tests.invoke({"code_path": target_path})
        print("✅ General QA tests completed")
        print(result[:500] + "..." if len(result) > 500 else result)
    except Exception as e:
        print(f"❌ Failed: {e}")
    
    print("\n" + "="*60)
    print("✅ QA ANALYSIS COMPLETE!")

if __name__ == "__main__":
    target = r"C:\Users\adria\OneDrive\Desktop\YieldWise Data Scrappers"
    run_qa_analysis(target) 