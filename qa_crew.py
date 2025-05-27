#!/usr/bin/env python3

"""
QA Crew - Professional Code Quality Analysis Team
CrewAI implementation with specialized agents and tools
"""

import os
from decouple import config
from crewai import Agent, Task, Crew, Process
# Import the CrewAI-compatible tools
import qa_crewai_tools

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

class QACrew:
    """Professional QA Crew for comprehensive code analysis"""
    
    def __init__(self):
        self.agents = self._create_agents()
        self.tasks = []
        
    def _create_agents(self):
        """Create specialized QA agents with assigned tools"""
        
        # CS Professor - Architecture and Complexity Analysis
        cs_professor = Agent(
            role="Software Architecture Analyst",
            goal="Analyze code structure, design patterns, and algorithmic complexity to identify architectural issues and improvement opportunities.",
            backstory="Experienced software architect with expertise in design patterns, code organization, and system design. Focuses on maintainability, scalability, and code quality from an architectural perspective.",
            tools=[qa_crewai_tools.analyze_code_structure, qa_crewai_tools.analyze_code_complexity, qa_crewai_tools.check_best_practices],
            verbose=True,
            allow_delegation=False
        )
        
        # Tech Stack Expert - Language-Specific Analysis
        tech_expert = Agent(
            role="Technology Stack Specialist",
            goal="Analyze Python, React, and SQL code for syntax errors, framework-specific issues, and adherence to best practices.",
            backstory="Full-stack developer with experience in Python, React, and SQL. Specializes in identifying language-specific issues, performance problems, and framework best practices.",
            tools=[qa_crewai_tools.check_python_syntax, qa_crewai_tools.analyze_react_components, qa_crewai_tools.validate_sql_queries, qa_crewai_tools.validate_imports, qa_crewai_tools.check_localhost_site],
            verbose=True,
            allow_delegation=False
        )
        
        # Dependencies Expert - Package and Security Analysis
        deps_expert = Agent(
            role="Dependency Management Specialist",
            goal="Analyze package dependencies for version compatibility, security vulnerabilities, and management best practices.",
            backstory="DevOps engineer specializing in dependency management and supply chain security. Experienced with package managers and identifying dependency-related issues.",
            tools=[qa_crewai_tools.check_package_dependencies, qa_crewai_tools.validate_imports],
            verbose=True,
            allow_delegation=False
        )
        
        # Security Expert - Vulnerability Assessment
        security_expert = Agent(
            role="Security Analyst",
            goal="Identify security vulnerabilities, anti-patterns, and potential attack vectors in code.",
            backstory="Cybersecurity professional with experience in application security and secure code review. Specializes in OWASP vulnerabilities and security best practices.",
            tools=[qa_crewai_tools.scan_security_vulnerabilities, qa_crewai_tools.check_best_practices],
            verbose=True,
            allow_delegation=False
        )
        
        # QA Tester - Comprehensive Quality Assessment
        qa_tester = Agent(
            role="Quality Assurance Engineer",
            goal="Perform comprehensive quality assessment including code quality, documentation review, and testing analysis.",
            backstory="QA engineer with experience in software testing and quality assurance. Specializes in synthesizing findings and providing actionable recommendations for code improvement.",
            tools=[qa_crewai_tools.run_general_qa_tests, qa_crewai_tools.analyze_code_structure, qa_crewai_tools.check_localhost_site],
            verbose=True,
            allow_delegation=False
        )
        
        return {
            'cs_professor': cs_professor,
            'tech_expert': tech_expert,
            'deps_expert': deps_expert,
            'security_expert': security_expert,
            'qa_tester': qa_tester
        }
    
    def create_tasks(self, code_path: str, project_type: str = "mixed", localhost_port: str = None):
        """Create analysis tasks for the crew"""
        
        # Sanitize the code_path for reports (remove personal info)
        sanitized_path = self._sanitize_path(code_path)
        
        tasks = []
        
        # Task 1: Architectural Review
        architectural_task = Task(
            description=f"""Conduct a comprehensive architectural and algorithmic analysis of the codebase at {sanitized_path}. 
            Focus on: 
            1) Overall code structure and organization
            2) Design patterns usage and appropriateness
            3) Algorithmic complexity and efficiency
            4) Separation of concerns and modularity
            5) Scalability and maintainability considerations
            
            Use your assigned tools to gather detailed insights. Analyze the actual path: {code_path}""",
            expected_output="A detailed architectural analysis report including: code organization assessment, design pattern evaluation, complexity analysis, architectural recommendations, and academic insights on improving the codebase structure. Include specific examples and line references where applicable.",
            agent=self.agents['cs_professor']
        )
        
        # Task 2: Technology Analysis
        tech_task = Task(
            description=f"""Perform deep technical analysis of the {project_type} codebase at {sanitized_path}.
            For Python code: check syntax, style (PEP 8), imports, and Python-specific best practices.
            For React components: analyze hooks usage, component structure, performance patterns, and accessibility.
            For SQL: validate query syntax, check for injection risks, and performance issues.
            {f'If possible, also check the running localhost site on port {localhost_port} for accessibility, performance, and basic functionality.' if localhost_port else ''}
            
            Use your assigned tools as appropriate for the project type. Analyze the actual path: {code_path}""",
            expected_output="A comprehensive technical analysis report covering: syntax validation results, framework-specific issues, performance concerns, technology-specific best practices violations, localhost site status (if applicable), and detailed recommendations for each technology stack found in the codebase.",
            agent=self.agents['tech_expert']
        )
        
        # Task 3: Dependency Validation
        deps_task = Task(
            description=f"""Analyze all package dependencies and dependency management practices for the project at {sanitized_path}.
            Examine requirements.txt, package.json, and other dependency files.
            Check for:
            1) Version compatibility issues
            2) Security vulnerabilities in dependencies
            3) Outdated packages
            4) Missing dependencies
            5) Dependency conflicts
            
            Use your assigned tools to perform thorough dependency analysis. Analyze the actual path: {code_path}""",
            expected_output="A detailed dependency analysis report including: dependency health score, security vulnerability assessment, version compatibility analysis, missing dependency identification, and specific recommendations for dependency management improvements.",
            agent=self.agents['deps_expert']
        )
        
        # Task 4: Security Assessment
        security_task = Task(
            description=f"""Conduct a thorough security assessment of the codebase at {sanitized_path}.
            Scan for:
            1) Common security vulnerabilities (OWASP Top 10)
            2) Hardcoded secrets and credentials
            3) Injection attack vectors
            4) Insecure coding patterns
            5) Authentication and authorization issues
            
            Use your assigned tools to identify security risks and provide remediation guidance. Analyze the actual path: {code_path}""",
            expected_output="A comprehensive security assessment report categorizing findings by risk level (high, medium, low), providing specific vulnerability details, potential impact analysis, and detailed remediation steps for each security issue identified.",
            agent=self.agents['security_expert']
        )
        
        # Task 5: Comprehensive QA
        qa_task = Task(
            description=f"""Synthesize all previous analysis results and perform final comprehensive QA testing for the project at {sanitized_path}.
            Review findings from architectural, technical, dependency, and security assessments.
            Conduct additional general QA tests including:
            1) Code quality metrics
            2) Documentation assessment
            3) Testing coverage evaluation
            4) Overall maintainability analysis
            {f'5) Final localhost site verification on port {localhost_port}' if localhost_port else ''}
            
            Use your assigned tools and generate a final executive summary with prioritized recommendations. Analyze the actual path: {code_path}""",
            expected_output="A comprehensive QA report that synthesizes all findings into an executive summary, provides an overall quality score, lists critical issues requiring immediate attention, includes localhost site status (if applicable), includes a prioritized action plan, and offers specific recommendations for improving code quality, security, and maintainability. This report should be suitable for both technical teams and management review.",
            agent=self.agents['qa_tester']
        )
        
        return [architectural_task, tech_task, deps_task, security_task, qa_task]
    
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
        """Run the complete QA analysis"""
        
        print("STARTING QA CREW ANALYSIS")
        print("=" * 60)
        print(f"Target: {code_path}")
        print(f"Type: {project_type}")
        if localhost_port:
            print(f"Localhost: port {localhost_port}")
        print()
        
        # Create tasks
        tasks = self.create_tasks(code_path, project_type, localhost_port)
        
        # Create and run crew
        crew = Crew(
            agents=list(self.agents.values()),
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )
        
        # Execute the crew
        result = crew.kickoff()
        
        print("\nQA CREW ANALYSIS COMPLETE!")
        print("=" * 60)
        
        return result

def main():
    """Main function for running QA analysis"""
    import argparse
    
    parser = argparse.ArgumentParser(description='QA Crew - Professional Code Analysis')
    parser.add_argument('--path', required=True, help='Path to code to analyze')
    parser.add_argument('--type', default='mixed', choices=['python', 'react', 'sql', 'mixed'], help='Project type')
    parser.add_argument('--port', help='Localhost port to check (optional)')
    
    args = parser.parse_args()
    
    # Initialize and run QA crew
    qa_crew = QACrew()
    result = qa_crew.run_analysis(args.path, args.type, args.port)
    
    print("\nFINAL RESULT:")
    print(result)

if __name__ == "__main__":
    main() 