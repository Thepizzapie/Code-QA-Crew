#!/usr/bin/env python3

"""
QA CLI - Command Line Interface for Code QA Crew
Allows specifying folder paths and ports for analysis
"""

import argparse
import os
import sys
from pathlib import Path
from qa_crew import QACrew
from demo_qa_crew import run_demo_qa_analysis, demo_localhost_check
from qa_tools import check_localhost_site

def main():
    parser = argparse.ArgumentParser(
        description="Code QA Crew - Analyze code and check localhost sites",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Quick analysis (current directory)
  python qa_cli.py
  
  # Code analysis only (default)
  python qa_cli.py --path ./frontend --type react
  
  # Full CrewAI analysis with specialized agents
  python qa_cli.py --path ./frontend --crew
  
  # Code analysis + localhost check
  python qa_cli.py --path ./frontend --type react --port 3000
  
  # CrewAI analysis + localhost check
  python qa_cli.py --path ./frontend --crew --port 3000
  
  # Check localhost only
  python qa_cli.py --localhost-only --port 3000
  
  # Multiple ports check
  python qa_cli.py --localhost-only --ports 3000,8000,5000
        """
    )
    
    # Path arguments
    parser.add_argument(
        '--path', '-p',
        type=str,
        default='.',
        help='Path to analyze (default: current directory)'
    )
    
    parser.add_argument(
        '--type', '-t',
        choices=['python', 'react', 'sql', 'mixed'],
        default='mixed',
        help='Project type (default: mixed)'
    )
    
    # Port arguments
    parser.add_argument(
        '--port',
        type=str,
        help='Single port to check (e.g., 3000)'
    )
    
    parser.add_argument(
        '--ports',
        type=str,
        help='Multiple ports to check, comma-separated (e.g., 3000,8000,5000)'
    )
    
    # Analysis options
    parser.add_argument(
        '--localhost-only',
        action='store_true',
        help='Only check localhost, skip code analysis'
    )
    
    parser.add_argument(
        '--code-only',
        action='store_true',
        help='Only analyze code, skip localhost check'
    )
    
    parser.add_argument(
        '--quick',
        action='store_true',
        help='Quick analysis (faster, less detailed)'
    )
    
    parser.add_argument(
        '--crew',
        action='store_true',
        help='Use full CrewAI implementation with specialized agents (slower but more comprehensive)'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output file for report (default: auto-generated)'
    )
    
    args = parser.parse_args()
    
    # Validate path
    if not os.path.exists(args.path):
        print(f"❌ Error: Path '{args.path}' does not exist")
        sys.exit(1)
    
    # Convert relative path to absolute
    analysis_path = os.path.abspath(args.path)
    
    print("🎯 CODE QA CREW - CLI")
    print("=" * 60)
    print(f"📁 Target Path: {analysis_path}")
    print(f"🏷️ Project Type: {args.type}")
    
    # Handle localhost-only mode
    if args.localhost_only:
        if args.port:
            print(f"🌐 Checking localhost:{args.port}")
            result = check_localhost_site(args.port)
            print(result)
        elif args.ports:
            ports = [p.strip() for p in args.ports.split(',')]
            print(f"🌐 Checking multiple ports: {', '.join(ports)}")
            for port in ports:
                print(f"\n🔍 Port {port}:")
                try:
                    result = check_localhost_site(port)
                    # Extract status line
                    lines = result.split('\n')
                    for line in lines:
                        if 'Status:' in line:
                            print(f"   {line.strip()}")
                            break
                except Exception as e:
                    print(f"   ❌ Error: {e}")
        else:
            print("❌ Error: --localhost-only requires --port or --ports")
            sys.exit(1)
        return
    
    # Handle code-only mode
    if args.code_only:
        print("🔍 Running code analysis only...")
        report = run_demo_qa_analysis(analysis_path, args.type, check_localhost=False)
        print("✅ Code analysis complete!")
        return
    
    # Handle multiple ports
    if args.ports:
        ports = [p.strip() for p in args.ports.split(',')]
        print(f"🌐 Will check multiple ports: {', '.join(ports)}")
        
        # Run analysis for each port
        for i, port in enumerate(ports):
            print(f"\n{'='*60}")
            print(f"🔍 ANALYSIS {i+1}/{len(ports)} - Port {port}")
            print(f"{'='*60}")
            
            try:
                report = run_demo_qa_analysis(
                    analysis_path, 
                    args.type, 
                    check_localhost=True, 
                    port=port
                )
                print(f"✅ Analysis complete for port {port}")
            except Exception as e:
                print(f"❌ Analysis failed for port {port}: {e}")
        return
    
    # Handle single port or no port - DEFAULT TO CODE ONLY
    check_localhost = bool(args.port)
    port = args.port if args.port else None
    
    if check_localhost:
        print(f"🌐 Will check localhost:{port}")
    else:
        print("🔍 Code analysis only (no localhost check)")
    
    print("\n🚀 Starting analysis...")
    
    try:
        if args.crew:
            # Use full CrewAI implementation
            print("🤖 Using CrewAI with specialized agents...")
            qa_crew = QACrew()
            result = qa_crew.run_analysis(analysis_path, args.type, port)
            
            # Save result if output specified
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(str(result))
                print(f"📄 CrewAI report saved to: {args.output}")
        else:
            # Use demo/quick analysis
            report = run_demo_qa_analysis(
                analysis_path, 
                args.type, 
                check_localhost=check_localhost, 
                port=port or "3000"  # Fallback port for function call
            )
            
            # Save custom output if specified
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(report)
                print(f"📄 Demo report saved to: {args.output}")
        
        print("\n✅ ANALYSIS COMPLETE!")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        sys.exit(1)

def quick_check():
    """Quick function for simple checks"""
    if len(sys.argv) == 1:
        print("🎯 QA CLI - Quick Usage:")
        print("python qa_cli.py                                # Analyze current directory (code only)")
        print("python qa_cli.py --path ./frontend              # Analyze specific folder (code only)")
        print("python qa_cli.py --path ./frontend --port 3000  # Analyze folder + check port")
        print("python qa_cli.py --localhost-only --port 3000   # Check port only")
        print("python qa_cli.py --help                         # Full help")
        return
    
    main()

if __name__ == "__main__":
    quick_check() 