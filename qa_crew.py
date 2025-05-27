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
        
        print(f"✅ Ollama configured: {ollama_model} at {ollama_base_url}")
        return ollama_model
    else:
        # Configure OpenAI
        try:
            openai_api_key = config('OPENAI_API_KEY')
            os.environ['OPENAI_API_KEY'] = openai_api_key
            print("✅ OpenAI API Key loaded successfully")
            return 'gpt-4-turbo-preview'
        except Exception as e:
            print(f"⚠️ Warning: Could not load OPENAI_API_KEY from .env file: {e}")
            print("💡 Tip: Set USE_OLLAMA=true in .env to use local Ollama instead")
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
            role="Expert Computer Science Professor and Software Architecture Analyst",
            goal="Conduct comprehensive architectural and algorithmic analysis of codebases to identify design patterns, architectural flaws, algorithmic inefficiencies, and provide academic-level insights on code structure and computational complexity.",
            backstory="You are a distinguished Computer Science Professor with 20+ years of experience in software engineering, algorithms, and system design. You have published numerous papers on software architecture and have mentored thousands of students. Your expertise spans multiple programming paradigms, design patterns, and computational theory. You approach code analysis with both theoretical rigor and practical wisdom, identifying not just what's wrong but explaining the underlying computer science principles that should guide better solutions.",
            tools=[qa_crewai_tools.analyze_code_structure, qa_crewai_tools.analyze_code_complexity, qa_crewai_tools.check_best_practices],
            verbose=True,
            allow_delegation=False
        )
        
        # Tech Stack Expert - Language-Specific Analysis
        tech_expert = Agent(
            role="Senior Full-Stack Developer and Technology Specialist",
            goal="Perform deep technical analysis of Python, React, and SQL code to identify syntax errors, framework-specific issues, performance bottlenecks, and adherence to technology-specific best practices and conventions.",
            backstory="You are a seasoned full-stack developer with 15+ years of hands-on experience building production applications using Python, React, and SQL databases. You've worked at major tech companies and startups, shipping code that serves millions of users. You know the common pitfalls, performance gotchas, and best practices for each technology stack. Your analysis goes beyond surface-level syntax checking to understand the nuances of how these technologies work together in real-world applications.",
            tools=[qa_crewai_tools.check_python_syntax, qa_crewai_tools.analyze_react_components, qa_crewai_tools.validate_sql_queries, qa_crewai_tools.validate_imports, qa_crewai_tools.check_localhost_site],
            verbose=True,
            allow_delegation=False
        )
        
        # Dependencies Expert - Package and Security Analysis
        deps_expert = Agent(
            role="Package Management and Dependency Security Specialist",
            goal="Analyze and validate all package dependencies, version compatibility, security vulnerabilities, and dependency management practices to ensure robust, secure, and maintainable software supply chains.",
            backstory="You are a DevOps and Security Engineer specializing in software supply chain security and dependency management. You've seen countless production incidents caused by dependency issues - from version conflicts to security vulnerabilities in third-party packages. You understand the intricacies of package managers (pip, npm, yarn), semantic versioning, and the importance of keeping dependencies up-to-date while maintaining stability. Your expertise helps teams avoid the common traps of dependency hell and security breaches.",
            tools=[qa_crewai_tools.check_package_dependencies, qa_crewai_tools.validate_imports],
            verbose=True,
            allow_delegation=False
        )
        
        # Security Expert - Vulnerability Assessment
        security_expert = Agent(
            role="Cybersecurity Analyst and Application Security Specialist",
            goal="Conduct thorough security assessments to identify vulnerabilities, security anti-patterns, potential attack vectors, and compliance issues while providing actionable remediation guidance.",
            backstory="You are a certified cybersecurity professional with extensive experience in application security, penetration testing, and secure code review. You've worked with organizations to secure their applications against OWASP Top 10 vulnerabilities and have experience with security frameworks like NIST and ISO 27001. You think like an attacker while maintaining the mindset of a defender, always looking for ways code could be exploited and how to prevent those attacks. Your analysis covers everything from injection attacks to authentication flaws to data exposure risks.",
            tools=[qa_crewai_tools.scan_security_vulnerabilities, qa_crewai_tools.check_best_practices],
            verbose=True,
            allow_delegation=False
        )
        
        # QA Tester - Comprehensive Quality Assessment
        qa_tester = Agent(
            role="Senior Quality Assurance Engineer and Test Strategy Lead",
            goal="Perform comprehensive quality assurance testing including functional testing, code quality assessment, documentation review, and overall system reliability analysis to ensure software meets production readiness standards.",
            backstory="You are an experienced QA Engineer with 12+ years in software testing across various industries and project types. You've developed testing strategies for everything from small startups to enterprise applications. You understand the full testing pyramid - from unit tests to integration tests to end-to-end testing. Your approach is methodical and thorough, ensuring that software not only works as intended but is maintainable, documented, and ready for production deployment. You're the final gatekeeper who synthesizes all findings into actionable recommendations.",
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
        
        print("🚀 STARTING QA CREW ANALYSIS")
        print("=" * 60)
        print(f"📁 Target: {code_path}")
        print(f"🏷️ Type: {project_type}")
        if localhost_port:
            print(f"🌐 Localhost: port {localhost_port}")
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
        
        print("\n✅ QA CREW ANALYSIS COMPLETE!")
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
    
    print("\n📊 FINAL RESULT:")
    print(result)

if __name__ == "__main__":
    main() 