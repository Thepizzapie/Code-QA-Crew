#!/usr/bin/env python3

"""
Enhanced QA Crew - Professional Code Quality Analysis Team with 10 Specialized Agents
CrewAI implementation with enhanced specialized agents and tools
"""

import os
import yaml
from pathlib import Path
from decouple import config
from crewai import Agent, Task, Crew, Process
import qa_crewai_tools
import time

# Load environment variables and configure AI model
def setup_ai_model():
    """Configure AI model - either OpenAI or Ollama"""
    use_ollama = config('USE_OLLAMA', default=False, cast=bool)
    
    if use_ollama:
        # Configure Ollama
        ollama_model = config('OLLAMA_MODEL', default='llama2')
        ollama_base_url = config('OLLAMA_BASE_URL', default='http://localhost:11434')
        
        os.environ['OPENAI_API_BASE'] = ollama_base_url
        os.environ['OPENAI_MODEL_NAME'] = ollama_model
        os.environ['OPENAI_API_KEY'] = 'ollama'  # Dummy key for Ollama
        
        print(f"Ollama configured: {ollama_model} at {ollama_base_url}")
        return ollama_model
    else:
        # Configure OpenAI
        try:
            openai_api_key = config('OPENAI_API_KEY')
            os.environ['OPENAI_API_KEY'] = openai_api_key
            print("OpenAI API Key loaded successfully")
            return 'gpt-4-turbo-preview'
        except Exception as e:
            print(f"Warning: Could not load OPENAI_API_KEY from .env file: {e}")
            print("Tip: Set USE_OLLAMA=true in .env to use local Ollama instead")
            return None

# Setup AI model
model_name = setup_ai_model()

class EnhancedQACrew:
    """Enhanced QA Crew with 10 specialized agents for comprehensive code analysis"""
    
    def __init__(self):
        print(f"Enhanced QA Crew initialized with 10 agents using {model_name}")
        
        self.agents_config = self._load_agents_config()
        self.tasks_config = self._load_tasks_config()
        self.agents = self._create_agents()
        
    def _load_agents_config(self):
        """Load enhanced agents configuration from YAML"""
        config_path = Path("config/agents_enhanced.yaml")
        if config_path.exists():
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        else:
            raise FileNotFoundError("Enhanced agents configuration not found")
    
    def _load_tasks_config(self):
        """Load enhanced tasks configuration from YAML"""
        config_path = Path("config/tasks_enhanced.yaml")
        if config_path.exists():
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        else:
            raise FileNotFoundError("Enhanced tasks configuration not found")
        
    def _create_agents(self):
        """Create all 10 specialized QA agents with assigned tools"""
        
        agents = {}
        
        # CS Professor - Architecture and Complexity Analysis
        agents['cs_professor'] = Agent(
            role=self.agents_config['cs_professor']['role'],
            goal=self.agents_config['cs_professor']['goal'],
            backstory=self.agents_config['cs_professor']['backstory'],
            tools=[qa_crewai_tools.analyze_code_structure, qa_crewai_tools.analyze_code_complexity, qa_crewai_tools.check_best_practices],
            verbose=True,
            allow_delegation=False
        )
        
        # Python Expert - Python-Specific Analysis
        agents['python_expert'] = Agent(
            role=self.agents_config['python_expert']['role'],
            goal=self.agents_config['python_expert']['goal'],
            backstory=self.agents_config['python_expert']['backstory'],
            tools=[qa_crewai_tools.advanced_python_analysis, qa_crewai_tools.check_python_syntax, qa_crewai_tools.validate_imports],
            verbose=True,
            allow_delegation=False
        )
        
        # React Expert - Frontend Analysis
        agents['react_expert'] = Agent(
            role=self.agents_config['react_expert']['role'],
            goal=self.agents_config['react_expert']['goal'],
            backstory=self.agents_config['react_expert']['backstory'],
            tools=[qa_crewai_tools.react_performance_analysis, qa_crewai_tools.analyze_react_components, qa_crewai_tools.check_localhost_site],
            verbose=True,
            allow_delegation=False
        )
        
        # Swift Expert - iOS/macOS Analysis
        agents['swift_expert'] = Agent(
            role=self.agents_config['swift_expert']['role'],
            goal=self.agents_config['swift_expert']['goal'],
            backstory=self.agents_config['swift_expert']['backstory'],
            tools=[qa_crewai_tools.swift_swiftui_analysis, qa_crewai_tools.analyze_code_structure, qa_crewai_tools.check_best_practices],
            verbose=True,
            allow_delegation=False
        )
        
        # Database Expert - SQL and Database Analysis
        agents['database_expert'] = Agent(
            role=self.agents_config['database_expert']['role'],
            goal=self.agents_config['database_expert']['goal'],
            backstory=self.agents_config['database_expert']['backstory'],
            tools=[qa_crewai_tools.validate_sql_queries, qa_crewai_tools.security_vulnerability_scan],
            verbose=True,
            allow_delegation=False
        )
        
        # DevOps Expert - Infrastructure and Deployment
        agents['devops_expert'] = Agent(
            role=self.agents_config['devops_expert']['role'],
            goal=self.agents_config['devops_expert']['goal'],
            backstory=self.agents_config['devops_expert']['backstory'],
            tools=[qa_crewai_tools.analyze_code_structure, qa_crewai_tools.check_localhost_site, qa_crewai_tools.dependency_vulnerability_check],
            verbose=True,
            allow_delegation=False
        )
        
        # Dependencies Expert - Package and Security Analysis
        agents['dependencies_expert'] = Agent(
            role=self.agents_config['dependencies_expert']['role'],
            goal=self.agents_config['dependencies_expert']['goal'],
            backstory=self.agents_config['dependencies_expert']['backstory'],
            tools=[qa_crewai_tools.dependency_vulnerability_check, qa_crewai_tools.check_package_dependencies, qa_crewai_tools.validate_imports],
            verbose=True,
            allow_delegation=False
        )
        
        # Security Expert - Vulnerability Assessment
        agents['security_expert'] = Agent(
            role=self.agents_config['security_expert']['role'],
            goal=self.agents_config['security_expert']['goal'],
            backstory=self.agents_config['security_expert']['backstory'],
            tools=[qa_crewai_tools.security_vulnerability_scan, qa_crewai_tools.scan_security_vulnerabilities, qa_crewai_tools.check_best_practices],
            verbose=True,
            allow_delegation=False
        )
        
        # QA Tester - Comprehensive Quality Assessment
        agents['qa_tester'] = Agent(
            role=self.agents_config['qa_tester']['role'],
            goal=self.agents_config['qa_tester']['goal'],
            backstory=self.agents_config['qa_tester']['backstory'],
            tools=[qa_crewai_tools.run_general_qa_tests, qa_crewai_tools.analyze_code_structure, qa_crewai_tools.check_localhost_site],
            verbose=True,
            allow_delegation=False
        )
        
        # Documentation Expert - Documentation Quality Analysis
        agents['documentation_expert'] = Agent(
            role=self.agents_config['documentation_expert']['role'],
            goal=self.agents_config['documentation_expert']['goal'],
            backstory=self.agents_config['documentation_expert']['backstory'],
            tools=[qa_crewai_tools.analyze_documentation_quality, qa_crewai_tools.research_best_practices, qa_crewai_tools.analyze_code_structure],
            verbose=True,
            allow_delegation=False
        )
        
        return agents
    
    def create_tasks(self, code_path: str, project_type: str = "mixed", localhost_port: str = None):
        """Create analysis tasks for all 10 agents"""
        
        # Sanitize the code_path for reports (remove personal info)
        sanitized_path = self._sanitize_path(code_path)
        
        tasks = []
        
        # Task 1: CS Professor - Architectural Review
        tasks.append(Task(
            description=f"""As an expert Computer Science Professor, conduct a comprehensive architectural and algorithmic analysis of the codebase at {sanitized_path}. 
            Focus on: 
            1) Overall code structure and organization from an academic perspective
            2) Design patterns usage and appropriateness
            3) Algorithmic complexity and computational efficiency
            4) Software engineering principles adherence
            5) Scalability and maintainability from a theoretical standpoint
            
            Use your assigned tools to gather detailed insights. Analyze the actual path: {code_path}""",
            expected_output="A detailed academic-level architectural analysis report including: theoretical foundations, design pattern evaluation, computational complexity analysis, software engineering principles assessment, and scholarly recommendations for improving the codebase architecture.",
            agent=self.agents['cs_professor']
        ))
        
        # Task 2: Python Expert - Deep Python Analysis
        tasks.append(Task(
            description=f"""As a Senior Python Developer, perform deep Python-specific analysis of the codebase at {sanitized_path}.
            Focus on:
            1) Python syntax validation and PEP compliance
            2) Python-specific performance patterns and anti-patterns
            3) Framework usage (Django, Flask, FastAPI) best practices
            4) Import structure and dependency management
            5) Python ecosystem integration
            
            Use your assigned tools for comprehensive Python analysis. Analyze the actual path: {code_path}""",
            expected_output="A comprehensive Python-specific analysis report covering: syntax validation, PEP compliance, performance optimization opportunities, framework-specific recommendations, import analysis, and Python ecosystem best practices.",
            agent=self.agents['python_expert']
        ))
        
        # Task 3: React Expert - Frontend Analysis
        tasks.append(Task(
            description=f"""As a Senior React Developer, analyze the frontend components and React patterns in the codebase at {sanitized_path}.
            Focus on:
            1) React component architecture and hook usage
            2) State management patterns and performance optimization
            3) Modern React patterns and TypeScript integration
            4) Accessibility and user experience considerations
            {f'5) Live application analysis on localhost:{localhost_port}' if localhost_port else '5) Static component analysis'}
            
            Use your assigned tools for React-specific analysis. Analyze the actual path: {code_path}""",
            expected_output="A detailed React analysis report including: component architecture assessment, hook usage patterns, performance optimization recommendations, accessibility evaluation, and modern React best practices compliance.",
            agent=self.agents['react_expert']
        ))
        
        # Task 4: Swift Expert - iOS/macOS Analysis
        tasks.append(Task(
            description=f"""As a Senior Swift Developer, analyze any Swift/iOS/macOS code in the codebase at {sanitized_path}.
            Focus on:
            1) Swift code quality and modern language features
            2) iOS/macOS architecture patterns (MVVM, VIPER)
            3) SwiftUI and UIKit best practices
            4) Memory management and performance optimization
            5) Platform-specific considerations
            
            Use your assigned tools for Swift-specific analysis. Analyze the actual path: {code_path}""",
            expected_output="A comprehensive Swift analysis report covering: code quality assessment, architecture pattern evaluation, platform-specific recommendations, performance optimization opportunities, and modern Swift best practices.",
            agent=self.agents['swift_expert']
        ))
        
        # Task 5: Database Expert - SQL and Database Analysis
        tasks.append(Task(
            description=f"""As a Database Architect, analyze all database-related code and SQL queries in the codebase at {sanitized_path}.
            Focus on:
            1) SQL query optimization and performance
            2) Database schema design and normalization
            3) Indexing strategies and query execution plans
            4) SQL injection vulnerabilities and security
            5) Database-specific best practices
            
            Use your assigned tools for database analysis. Analyze the actual path: {code_path}""",
            expected_output="A detailed database analysis report including: SQL query optimization recommendations, schema design evaluation, security vulnerability assessment, indexing strategy suggestions, and database best practices compliance.",
            agent=self.agents['database_expert']
        ))
        
        # Task 6: DevOps Expert - Infrastructure Analysis
        tasks.append(Task(
            description=f"""As a DevOps Engineer, analyze the deployment and infrastructure configurations in the codebase at {sanitized_path}.
            Focus on:
            1) Docker files and containerization best practices
            2) CI/CD pipeline configurations
            3) Infrastructure as code and deployment strategies
            4) Monitoring and logging setup
            {f'5) Live application infrastructure on localhost:{localhost_port}' if localhost_port else '5) Static infrastructure analysis'}
            
            Use your assigned tools for DevOps analysis. Analyze the actual path: {code_path}""",
            expected_output="A comprehensive DevOps analysis report covering: containerization assessment, CI/CD pipeline evaluation, infrastructure recommendations, monitoring setup analysis, and deployment best practices.",
            agent=self.agents['devops_expert']
        ))
        
        # Task 7: Dependencies Expert - Package Management Analysis
        tasks.append(Task(
            description=f"""As a Package Management Specialist, analyze all dependencies and package management practices in the codebase at {sanitized_path}.
            Focus on:
            1) Dependency version management and compatibility
            2) Security vulnerabilities in third-party packages
            3) Package manager best practices (pip, npm, yarn)
            4) Supply chain security and dependency auditing
            5) Version pinning and update strategies
            
            Use your assigned tools for dependency analysis. Analyze the actual path: {code_path}""",
            expected_output="A detailed dependency management report including: security vulnerability assessment, version compatibility analysis, package manager best practices evaluation, supply chain security recommendations, and dependency update strategies.",
            agent=self.agents['dependencies_expert']
        ))
        
        # Task 8: Security Expert - Comprehensive Security Assessment
        tasks.append(Task(
            description=f"""As a Cybersecurity Analyst, conduct a thorough security assessment of the codebase at {sanitized_path}.
            Focus on:
            1) OWASP Top 10 vulnerability assessment
            2) Code injection and XSS vulnerabilities
            3) Authentication and authorization security
            4) Data protection and encryption practices
            5) Security configuration and hardening
            
            Use your assigned tools for security analysis. Analyze the actual path: {code_path}""",
            expected_output="A comprehensive security assessment report categorizing findings by CVSS scores, providing specific vulnerability details, attack vector analysis, compliance assessment, and detailed remediation steps for each security issue identified.",
            agent=self.agents['security_expert']
        ))
        
        # Task 9: QA Tester - Final Quality Assessment
        tasks.append(Task(
            description=f"""As a Senior QA Engineer, synthesize all previous analysis results and perform final comprehensive quality assessment for the project at {sanitized_path}.
            Review findings from all specialist teams and conduct additional quality assurance testing:
            1) Overall code quality metrics and maintainability
            2) Documentation completeness and quality
            3) Testing coverage and strategy evaluation
            4) Production readiness assessment
            {f'5) End-to-end application testing on localhost:{localhost_port}' if localhost_port else '5) Static quality analysis'}
            
            Use your assigned tools and generate a final executive summary. Analyze the actual path: {code_path}""",
            expected_output="A comprehensive executive QA report that synthesizes all specialist findings, provides an overall quality score with detailed breakdown, lists critical issues requiring immediate attention, includes production readiness checklist, and offers a prioritized action plan suitable for both technical teams and management review.",
            agent=self.agents['qa_tester']
        ))
        
        # Task 10: Documentation Expert - Documentation Quality Analysis
        tasks.append(Task(
            description=f"""As a Documentation Specialist, analyze the quality and consistency of the project's documentation at {sanitized_path}.
            Focus on:
            1) Documentation structure and organization
            2) Clarity and readability of technical documentation
            3) Consistency and adherence to project documentation standards
            4) Completeness and accuracy of information
            5) Research and best practices for documentation improvement
            
            Use your assigned tools for documentation analysis. Analyze the actual path: {code_path}""",
            expected_output="A detailed documentation analysis report that provides insights into the project's documentation quality, identifies areas for improvement, and offers recommendations for enhancing the project's documentation.",
            agent=self.agents['documentation_expert']
        ))
        
        return tasks
    
    def _sanitize_path(self, path: str) -> str:
        """Remove personal information from file paths for reports"""
        import re
        
        # Remove Windows user paths - use raw strings to avoid escape issues
        path = re.sub(r'C:\\Users\\[^\\]+\\', r'C:\\Users\\[USER]\\', path)
        
        # Remove common personal directories
        path = re.sub(r'OneDrive\\Desktop\\', '', path)
        path = re.sub(r'Documents\\', '', path)
        path = re.sub(r'Downloads\\', '', path)
        
        # Remove long absolute paths, keep relative structure
        if len(path) > 50:
            parts = path.split('\\')
            if len(parts) > 3:
                path = '...\\' + '\\'.join(parts[-2:])
        
        return path
    
    def run_analysis(self, code_path: str, project_type: str = "mixed", localhost_port: str = None):
        """Run the complete enhanced QA analysis with all 10 agents"""
        
        analysis_start_time = time.time()
        
        # Log crew start
        print("STARTING ENHANCED QA CREW ANALYSIS")
        print("=" * 60)
        print(f"Target: {code_path}")
        print(f"Type: {project_type}")
        print(f"Agents: 10 specialized experts")
        if localhost_port:
            print(f"Localhost: port {localhost_port}")
        print()
        
        try:
            # Create tasks
            tasks = self.create_tasks(code_path, project_type, localhost_port)
            
            # Create and run crew with all 10 agents
            crew = Crew(
                agents=list(self.agents.values()),
                tasks=tasks,
                process=Process.sequential,
                verbose=True
            )
            
            # Execute the crew
            result = crew.kickoff()
            
            analysis_duration = time.time() - analysis_start_time
            
            # Log completion
            print("\nENHANCED QA CREW ANALYSIS COMPLETE!")
            print("=" * 60)
            print(f"Analyzed by {len(self.agents)} specialized agents")
            print(f"Total Duration: {analysis_duration:.2f} seconds")
            
            return result
            
        except Exception as e:
            analysis_duration = time.time() - analysis_start_time
            print(f"Analysis failed! Duration: {analysis_duration:.2f} seconds")
            
            raise

def main():
    """Main function for running enhanced QA analysis"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Enhanced QA Crew - Professional Code Analysis with 10 Specialists')
    parser.add_argument('--path', required=True, help='Path to code to analyze')
    parser.add_argument('--type', default='mixed', choices=['python', 'react', 'swift', 'sql', 'mixed'], help='Project type')
    parser.add_argument('--port', help='Localhost port to check (optional)')
    
    args = parser.parse_args()
    
    # Initialize and run enhanced QA crew
    qa_crew = EnhancedQACrew()
    result = qa_crew.run_analysis(args.path, args.type, args.port)
    
    print("\nFINAL RESULT:")
    print(result)

if __name__ == "__main__":
    main() 