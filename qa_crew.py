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
        
        # Python Expert - Python-Specific Analysis
        python_expert = Agent(
            role="Senior Python Developer and Performance Specialist",
            goal="Perform deep Python-specific analysis including syntax validation, PEP compliance, performance optimization, framework usage (Django, Flask, FastAPI), testing patterns, and Python ecosystem best practices.",
            backstory="Python core contributor with 12+ years of Python development experience. Worked on large-scale Python applications, contributed to popular open-source libraries, and understand the nuances of Python performance, memory management, and the GIL.",
            tools=[qa_crewai_tools.advanced_python_analysis, qa_crewai_tools.check_python_syntax, qa_crewai_tools.validate_imports],
            verbose=True,
            allow_delegation=False
        )
        
        # React Expert - Frontend Analysis
        react_expert = Agent(
            role="Senior React/Frontend Developer and Performance Specialist",
            goal="Analyze React applications for component architecture, hook usage, state management, performance optimization, accessibility, and modern React patterns including Next.js, TypeScript integration, and testing strategies.",
            backstory="React expert who has been building React applications since version 0.14. Seen the evolution from class components to hooks, from Redux to Context API to Zustand. Understand React's reconciliation algorithm, know how to optimize re-renders, and can spot performance bottlenecks instantly.",
            tools=[qa_crewai_tools.react_performance_analysis, qa_crewai_tools.analyze_react_components, qa_crewai_tools.check_localhost_site],
            verbose=True,
            allow_delegation=False
        )
        
        # Swift Expert - iOS/macOS Analysis
        swift_expert = Agent(
            role="Senior iOS/macOS Developer and Swift Performance Specialist",
            goal="Analyze Swift and SwiftUI applications for code quality, performance optimization, memory management, iOS/macOS best practices, architecture patterns (MVVM, VIPER), and modern Swift features including Combine, async/await, and SwiftUI declarative patterns.",
            backstory="Swift expert who has been developing iOS and macOS applications since Swift 1.0 and Objective-C before that. Shipped dozens of apps to the App Store, understand the intricacies of iOS SDK, memory management with ARC, and performance optimization for mobile devices.",
            tools=[qa_crewai_tools.swift_swiftui_analysis, qa_crewai_tools.analyze_code_structure, qa_crewai_tools.check_best_practices],
            verbose=True,
            allow_delegation=False
        )
        
        # Database Expert - SQL and Database Analysis
        database_expert = Agent(
            role="Database Architect and SQL Performance Specialist",
            goal="Analyze SQL queries, database schema design, indexing strategies, security vulnerabilities (SQL injection), query optimization, and database-specific best practices across PostgreSQL, MySQL, SQLite, and NoSQL databases.",
            backstory="Database architect with 15+ years of experience designing and optimizing database systems. Worked with everything from small SQLite databases to massive PostgreSQL clusters serving millions of queries per day.",
            tools=[qa_crewai_tools.validate_sql_queries, qa_crewai_tools.security_vulnerability_scan],
            verbose=True,
            allow_delegation=False
        )
        
        # DevOps Expert - Infrastructure and Deployment
        devops_expert = Agent(
            role="DevOps Engineer and Infrastructure Specialist",
            goal="Analyze deployment configurations, Docker files, CI/CD pipelines, infrastructure as code, monitoring setup, and deployment best practices to ensure reliable, scalable, and maintainable infrastructure.",
            backstory="DevOps engineer with expertise in containerization, orchestration, and cloud platforms. Built CI/CD pipelines that deploy code safely to production thousands of times per day.",
            tools=[qa_crewai_tools.analyze_code_structure, qa_crewai_tools.check_localhost_site, qa_crewai_tools.dependency_vulnerability_check],
            verbose=True,
            allow_delegation=False
        )
        
        # Documentation Expert - Documentation Quality Analysis
        documentation_expert = Agent(
            role="Technical Documentation Specialist and Information Architect",
            goal="Analyze and improve documentation quality, completeness, accessibility, and user experience to ensure comprehensive, maintainable, and user-friendly project documentation.",
            backstory="Technical writing specialist with 10+ years of experience creating documentation for software projects, APIs, and developer tools. Understand that great documentation is crucial for project success, maintainability, and developer experience.",
            tools=[qa_crewai_tools.analyze_documentation_quality, qa_crewai_tools.research_best_practices, qa_crewai_tools.analyze_code_structure],
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
        
        # Manager Agent - Natural Language Task Delegation
        manager = Agent(
            role="QA Team Manager and Task Coordinator",
            goal="Interpret natural language requests from users and delegate appropriate analysis tasks to specialist agents based on the user's needs and project requirements.",
            backstory="Experienced QA team lead with deep knowledge of each specialist's capabilities. Expert at understanding user requirements and matching them to the right combination of specialists. Can interpret requests like 'check my Swift app for bugs and security issues' and delegate to Swift Expert and Security Analyst accordingly.",
            tools=[],
            verbose=True,
            allow_delegation=True
        )
        
        return {
            'manager': manager,
            'cs_professor': cs_professor,
            'python_expert': python_expert,
            'react_expert': react_expert,
            'swift_expert': swift_expert,
            'database_expert': database_expert,
            'devops_expert': devops_expert,
            'documentation_expert': documentation_expert,
            'tech_expert': tech_expert,
            'deps_expert': deps_expert,
            'security_expert': security_expert,
            'qa_tester': qa_tester
        }
    
    def create_tasks(self, code_path: str, project_type: str = "mixed", localhost_port: str = None):
        """Create analysis tasks for all 11 agents"""
        
        # Sanitize the code_path for reports (remove personal info)
        sanitized_path = self._sanitize_path(code_path)
        
        tasks = []
        
        # Task 1: CS Professor - Architectural Review
        tasks.append(Task(
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
        
        # Task 7: Documentation Expert - Documentation Quality Analysis
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
        
        # Task 8: Technology Analysis
        tasks.append(Task(
            description=f"""Perform deep technical analysis of the {project_type} codebase at {sanitized_path}.
            For Python code: check syntax, style (PEP 8), imports, and Python-specific best practices.
            For React components: analyze hooks usage, component structure, performance patterns, and accessibility.
            For SQL: validate query syntax, check for injection risks, and performance issues.
            {f'If possible, also check the running localhost site on port {localhost_port} for accessibility, performance, and basic functionality.' if localhost_port else ''}
            
            Use your assigned tools as appropriate for the project type. Analyze the actual path: {code_path}""",
            expected_output="A comprehensive technical analysis report covering: syntax validation results, framework-specific issues, performance concerns, technology-specific best practices violations, localhost site status (if applicable), and detailed recommendations for each technology stack found in the codebase.",
            agent=self.agents['tech_expert']
        ))
        
        # Task 9: Dependency Validation
        tasks.append(Task(
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
        ))
        
        # Task 10: Security Assessment
        tasks.append(Task(
            description=f"""Conduct a thorough security assessment of the codebase located at: {code_path}
            
            IMPORTANT: Use the scan_security_vulnerabilities tool with the path "{code_path}" to scan for:
            1) Common security vulnerabilities (OWASP Top 10)
            2) Hardcoded secrets and credentials
            3) Injection attack vectors
            4) Insecure coding patterns
            5) Authentication and authorization issues
            
            Then use the check_best_practices tool with the same path to verify coding standards.
            
            Provide a comprehensive security assessment with remediation guidance.""",
            expected_output="A comprehensive security assessment report categorizing findings by risk level (high, medium, low), providing specific vulnerability details, potential impact analysis, and detailed remediation steps for each security issue identified.",
            agent=self.agents['security_expert']
        ))
        
        # Task 11: Comprehensive QA
        tasks.append(Task(
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

    def list_available_agents(self):
        """List all available agents with their specializations"""
        print("\n🤖 AVAILABLE QA AGENTS")
        print("=" * 60)
        
        agent_info = {
            'cs_professor': 'Software Architecture Analyst - Code structure, design patterns, algorithmic complexity',
            'python_expert': 'Senior Python Developer - Python syntax, PEP compliance, performance optimization',
            'react_expert': 'Senior React Developer - Component architecture, hooks, performance, accessibility',
            'swift_expert': 'Senior iOS/macOS Developer - Swift code quality, SwiftUI, memory management',
            'database_expert': 'Database Architect - SQL optimization, schema design, injection vulnerabilities',
            'devops_expert': 'DevOps Engineer - Docker, CI/CD, infrastructure, deployment best practices',
            'documentation_expert': 'Documentation Specialist - Documentation quality, completeness, standards',
            'tech_expert': 'Technology Stack Specialist - Multi-language syntax, framework best practices',
            'deps_expert': 'Dependency Management Specialist - Package security, version compatibility',
            'security_expert': 'Security Analyst - OWASP vulnerabilities, secure coding patterns',
            'qa_tester': 'Quality Assurance Engineer - Overall quality metrics, testing coverage'
        }
        
        for i, (agent_key, description) in enumerate(agent_info.items(), 1):
            print(f"{i:2d}. {description}")
        
        print(f"{len(agent_info) + 1:2d}. ALL AGENTS - Run complete analysis with all agents")
        print()
        
        return list(agent_info.keys())
    
    def run_single_agent_analysis(self, agent_key: str, code_path: str, project_type: str = "mixed", localhost_port: str = None):
        """Run analysis with a single specific agent"""
        
        if agent_key not in self.agents:
            print(f"❌ Error: Agent '{agent_key}' not found!")
            return None
        
        print(f"\n🚀 RUNNING SINGLE AGENT ANALYSIS")
        print("=" * 60)
        print(f"Agent: {self.agents[agent_key].role}")
        print(f"Target: {code_path}")
        print(f"Type: {project_type}")
        if localhost_port:
            print(f"Localhost: port {localhost_port}")
        print()
        
        # Create a single task for the selected agent
        sanitized_path = self._sanitize_path(code_path)
        
        # Create agent-specific task
        if agent_key == 'cs_professor':
            task = Task(
                description=f"""Conduct a comprehensive architectural and algorithmic analysis of the codebase at {sanitized_path}. 
                Focus on: 
                1) Overall code structure and organization
                2) Design patterns usage and appropriateness
                3) Algorithmic complexity and efficiency
                4) Separation of concerns and modularity
                5) Scalability and maintainability considerations
                
                Use your assigned tools to gather detailed insights. Analyze the actual path: {code_path}""",
                expected_output="A detailed architectural analysis report including: code organization assessment, design pattern evaluation, complexity analysis, architectural recommendations, and academic insights on improving the codebase structure.",
                agent=self.agents[agent_key]
            )
        elif agent_key == 'python_expert':
            task = Task(
                description=f"""As a Senior Python Developer, perform deep Python-specific analysis of the codebase at {sanitized_path}.
                Focus on:
                1) Python syntax validation and PEP compliance
                2) Python-specific performance patterns and anti-patterns
                3) Framework usage (Django, Flask, FastAPI) best practices
                4) Import structure and dependency management
                5) Python ecosystem integration
                
                Use your assigned tools for comprehensive Python analysis. Analyze the actual path: {code_path}""",
                expected_output="A comprehensive Python-specific analysis report covering: syntax validation, PEP compliance, performance optimization opportunities, framework-specific recommendations, import analysis, and Python ecosystem best practices.",
                agent=self.agents[agent_key]
            )
        elif agent_key == 'react_expert':
            task = Task(
                description=f"""As a Senior React Developer, analyze the frontend components and React patterns in the codebase at {sanitized_path}.
                Focus on:
                1) React component architecture and hook usage
                2) State management patterns and performance optimization
                3) Modern React patterns and TypeScript integration
                4) Accessibility and user experience considerations
                {f'5) Live application analysis on localhost:{localhost_port}' if localhost_port else '5) Static component analysis'}
                
                Use your assigned tools for React-specific analysis. Analyze the actual path: {code_path}""",
                expected_output="A detailed React analysis report including: component architecture assessment, hook usage patterns, performance optimization recommendations, accessibility evaluation, and modern React best practices compliance.",
                agent=self.agents[agent_key]
            )
        elif agent_key == 'security_expert':
            task = Task(
                description=f"""Conduct a thorough security assessment of the codebase located at: {code_path}
                
                IMPORTANT: Use the scan_security_vulnerabilities tool with the path "{code_path}" to scan for:
                1) Common security vulnerabilities (OWASP Top 10)
                2) Hardcoded secrets and credentials
                3) Injection attack vectors
                4) Insecure coding patterns
                5) Authentication and authorization issues
                
                Then use the check_best_practices tool with the same path to verify coding standards.
                
                Provide a comprehensive security assessment with remediation guidance.""",
                expected_output="A comprehensive security assessment report categorizing findings by risk level (high, medium, low), providing specific vulnerability details, potential impact analysis, and detailed remediation steps for each security issue identified.",
                agent=self.agents[agent_key]
            )
        else:
            # Generic task for other agents
            task = Task(
                description=f"""Perform specialized analysis of the codebase at {sanitized_path} according to your expertise. Use your assigned tools to provide detailed insights and recommendations. Analyze the actual path: {code_path}""",
                expected_output="A detailed analysis report with findings, recommendations, and actionable insights specific to your area of expertise.",
                agent=self.agents[agent_key]
            )
        
        # Create and run crew with single agent
        crew = Crew(
            agents=[self.agents[agent_key]],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        # Execute the crew
        result = crew.kickoff()
        
        print(f"\n✅ SINGLE AGENT ANALYSIS COMPLETE!")
        print("=" * 60)
        
        return result

    def run_selected_agents_analysis(self, selected_agent_keys: list, code_path: str, project_type: str = "mixed", localhost_port: str = None):
        """Run analysis with multiple selected agents"""
        
        # Validate all selected agents exist
        for agent_key in selected_agent_keys:
            if agent_key not in self.agents:
                print(f"❌ Error: Agent '{agent_key}' not found!")
                return None
        
        print(f"\n🚀 RUNNING SELECTED AGENTS ANALYSIS")
        print("=" * 60)
        print(f"Selected Agents: {len(selected_agent_keys)}")
        for agent_key in selected_agent_keys:
            print(f"  • {self.agents[agent_key].role}")
        print(f"Target: {code_path}")
        print(f"Type: {project_type}")
        if localhost_port:
            print(f"Localhost: port {localhost_port}")
        print()
        
        # Create tasks for selected agents
        tasks = []
        sanitized_path = self._sanitize_path(code_path)
        
        for agent_key in selected_agent_keys:
            if agent_key == 'cs_professor':
                task = Task(
                    description=f"""Conduct a comprehensive architectural and algorithmic analysis of the codebase at {sanitized_path}. 
                    Focus on: 
                    1) Overall code structure and organization
                    2) Design patterns usage and appropriateness
                    3) Algorithmic complexity and efficiency
                    4) Separation of concerns and modularity
                    5) Scalability and maintainability considerations
                    
                    Use your assigned tools to gather detailed insights. Analyze the actual path: {code_path}""",
                    expected_output="A detailed architectural analysis report including: code organization assessment, design pattern evaluation, complexity analysis, architectural recommendations, and academic insights on improving the codebase structure.",
                    agent=self.agents[agent_key]
                )
            elif agent_key == 'python_expert':
                task = Task(
                    description=f"""As a Senior Python Developer, perform deep Python-specific analysis of the codebase at {sanitized_path}.
                    Focus on:
                    1) Python syntax validation and PEP compliance
                    2) Python-specific performance patterns and anti-patterns
                    3) Framework usage (Django, Flask, FastAPI) best practices
                    4) Import structure and dependency management
                    5) Python ecosystem integration
                    
                    Use your assigned tools for comprehensive Python analysis. Analyze the actual path: {code_path}""",
                    expected_output="A comprehensive Python-specific analysis report covering: syntax validation, PEP compliance, performance optimization opportunities, framework-specific recommendations, import analysis, and Python ecosystem best practices.",
                    agent=self.agents[agent_key]
                )
            elif agent_key == 'react_expert':
                task = Task(
                    description=f"""As a Senior React Developer, analyze the frontend components and React patterns in the codebase at {sanitized_path}.
                    Focus on:
                    1) React component architecture and hook usage
                    2) State management patterns and performance optimization
                    3) Modern React patterns and TypeScript integration
                    4) Accessibility and user experience considerations
                    {f'5) Live application analysis on localhost:{localhost_port}' if localhost_port else '5) Static component analysis'}
                    
                    Use your assigned tools for React-specific analysis. Analyze the actual path: {code_path}""",
                    expected_output="A detailed React analysis report including: component architecture assessment, hook usage patterns, performance optimization recommendations, accessibility evaluation, and modern React best practices compliance.",
                    agent=self.agents[agent_key]
                )
            elif agent_key == 'security_expert':
                task = Task(
                    description=f"""Conduct a thorough security assessment of the codebase located at: {code_path}
                    
                    IMPORTANT: Use the scan_security_vulnerabilities tool with the path "{code_path}" to scan for:
                    1) Common security vulnerabilities (OWASP Top 10)
                    2) Hardcoded secrets and credentials
                    3) Injection attack vectors
                    4) Insecure coding patterns
                    5) Authentication and authorization issues
                    
                    Then use the check_best_practices tool with the same path to verify coding standards.
                    
                    Provide a comprehensive security assessment with remediation guidance.""",
                    expected_output="A comprehensive security assessment report categorizing findings by risk level (high, medium, low), providing specific vulnerability details, potential impact analysis, and detailed remediation steps for each security issue identified.",
                    agent=self.agents[agent_key]
                )
            else:
                # Generic task for other agents
                task = Task(
                    description=f"""Perform specialized analysis of the codebase at {sanitized_path} according to your expertise. Use your assigned tools to provide detailed insights and recommendations. Analyze the actual path: {code_path}""",
                    expected_output="A detailed analysis report with findings, recommendations, and actionable insights specific to your area of expertise.",
                    agent=self.agents[agent_key]
                )
            
            tasks.append(task)
        
        # Create and run crew with selected agents
        selected_agents = [self.agents[key] for key in selected_agent_keys]
        crew = Crew(
            agents=selected_agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )
        
        # Execute the crew
        result = crew.kickoff()
        
        print(f"\n✅ SELECTED AGENTS ANALYSIS COMPLETE!")
        print("=" * 60)
        
        return result

    def run_natural_language_analysis(self, user_request: str, code_path: str, project_type: str = "mixed", localhost_port: str = None):
        """Run analysis based on natural language user request by interpreting and selecting appropriate agents"""
        
        print(f"\n🎯 NATURAL LANGUAGE QA REQUEST")
        print("=" * 60)
        print(f"User Request: {user_request}")
        print(f"Target: {code_path}")
        print(f"Type: {project_type}")
        if localhost_port:
            print(f"Localhost: port {localhost_port}")
        print()
        
        # Simple keyword-based agent selection
        request_lower = user_request.lower()
        selected_agents = []
        
        # Determine which agents to use based on keywords
        if any(word in request_lower for word in ['python', 'py', 'pip', 'django', 'flask', 'fastapi']):
            selected_agents.append('python_expert')
            print("🐍 Selected: Python Expert (detected Python-related keywords)")
        
        if any(word in request_lower for word in ['react', 'jsx', 'tsx', 'frontend', 'component', 'hook']):
            selected_agents.append('react_expert')
            print("⚛️ Selected: React Expert (detected React-related keywords)")
        
        if any(word in request_lower for word in ['swift', 'ios', 'macos', 'swiftui', 'xcode', 'app store']):
            selected_agents.append('swift_expert')
            print("🍎 Selected: Swift Expert (detected Swift/iOS-related keywords)")
        
        if any(word in request_lower for word in ['security', 'vulnerabilit', 'hack', 'attack', 'owasp', 'injection', 'hole']):
            selected_agents.append('security_expert')
            print("🔒 Selected: Security Expert (detected security-related keywords)")
        
        if any(word in request_lower for word in ['sql', 'database', 'query', 'mysql', 'postgres', 'sqlite']):
            selected_agents.append('database_expert')
            print("🗃️ Selected: Database Expert (detected database-related keywords)")
        
        if any(word in request_lower for word in ['docker', 'deploy', 'devops', 'ci/cd', 'infrastructure']):
            selected_agents.append('devops_expert')
            print("🚀 Selected: DevOps Expert (detected DevOps-related keywords)")
        
        if any(word in request_lower for word in ['document', 'readme', 'docs', 'comment']):
            selected_agents.append('documentation_expert')
            print("📚 Selected: Documentation Expert (detected documentation-related keywords)")
        
        if any(word in request_lower for word in ['depend', 'package', 'npm', 'pip', 'version']):
            selected_agents.append('deps_expert')
            print("📦 Selected: Dependencies Expert (detected dependency-related keywords)")
        
        if any(word in request_lower for word in ['bug', 'error', 'issue', 'problem', 'quality', 'test']):
            if 'python' in request_lower or project_type == 'python':
                if 'python_expert' not in selected_agents:
                    selected_agents.append('python_expert')
                    print("🐍 Selected: Python Expert (detected bug/quality keywords for Python project)")
            else:
                selected_agents.append('qa_tester')
                print("🧪 Selected: QA Tester (detected general quality/testing keywords)")
        
        if any(word in request_lower for word in ['architecture', 'design', 'pattern', 'structure', 'complexity']):
            selected_agents.append('cs_professor')
            print("🏗️ Selected: Architecture Analyst (detected architecture-related keywords)")
        
        if any(word in request_lower for word in ['performance', 'speed', 'optimization', 'slow']):
            if 'python' in request_lower:
                if 'python_expert' not in selected_agents:
                    selected_agents.append('python_expert')
                    print("🐍 Selected: Python Expert (detected performance keywords for Python)")
            elif 'react' in request_lower:
                if 'react_expert' not in selected_agents:
                    selected_agents.append('react_expert')
                    print("⚛️ Selected: React Expert (detected performance keywords for React)")
        
        # If no specific agents selected, default to general analysis
        if not selected_agents:
            selected_agents = ['cs_professor', 'qa_tester', 'security_expert']
            print("🔍 No specific keywords detected, using general analysis agents")
        
        # Remove duplicates while preserving order
        selected_agents = list(dict.fromkeys(selected_agents))
        
        print(f"\n📋 Running analysis with {len(selected_agents)} selected agents...")
        print()
        
        # Run the selected agents
        if len(selected_agents) == 1:
            result = self.run_single_agent_analysis(selected_agents[0], code_path, project_type, localhost_port)
        else:
            result = self.run_selected_agents_analysis(selected_agents, code_path, project_type, localhost_port)
        
        return result

def main():
    """Main function for running QA analysis with natural language or agent selection"""
    import argparse
    
    parser = argparse.ArgumentParser(description='QA Crew - Professional Code Analysis with Natural Language Interface')
    parser.add_argument('--path', required=True, help='Path to code to analyze')
    parser.add_argument('--type', default='mixed', choices=['python', 'react', 'swift', 'sql', 'mixed'], help='Project type')
    parser.add_argument('--port', help='Localhost port to check (optional)')
    parser.add_argument('--agents', help='Comma-separated list of agent numbers or "all" (optional)')
    parser.add_argument('--request', help='Natural language request for analysis (e.g., "check my Swift app for bugs and security issues")')
    
    args = parser.parse_args()
    
    # Initialize QA crew
    qa_crew = QACrew()
    
    # If natural language request is provided, use that
    if args.request:
        result = qa_crew.run_natural_language_analysis(args.request, args.path, args.type, args.port)
    # If agents specified via command line, use agent selection
    elif args.agents:
        if args.agents.lower() == 'all':
            result = qa_crew.run_analysis(args.path, args.type, args.port)
        else:
            available_agents = qa_crew.list_available_agents()
            try:
                if ',' in args.agents:
                    # Multiple agents
                    agent_numbers = [int(x.strip()) for x in args.agents.split(',')]
                    selected_agents = []
                    for num in agent_numbers:
                        if 1 <= num <= len(available_agents):
                            selected_agents.append(available_agents[num - 1])
                        else:
                            print(f"❌ Invalid agent number: {num}")
                            return
                    
                    result = qa_crew.run_selected_agents_analysis(selected_agents, args.path, args.type, args.port)
                else:
                    # Single agent
                    agent_num = int(args.agents)
                    if 1 <= agent_num <= len(available_agents):
                        selected_agent = available_agents[agent_num - 1]
                        result = qa_crew.run_single_agent_analysis(selected_agent, args.path, args.type, args.port)
                    else:
                        print(f"❌ Invalid agent number: {agent_num}")
                        return
            except ValueError:
                print("❌ Invalid agents format. Use numbers separated by commas or 'all'.")
                return
    # Interactive mode
    else:
        print("🎯 QA CREW - PROFESSIONAL CODE ANALYSIS")
        print("=" * 60)
        
        # Always show the available agents first
        available_agents = qa_crew.list_available_agents()
        
        print("Choose your preferred input method:")
        print("1. 🔢 Simple Agent Selection - Pick agents by number")
        print("2. 💬 Natural Language Request - Describe what you want in plain English")
        print()
        
        choice = input("Enter 1 for simple selection or 2 for natural language: ").strip()
        
        if choice == '1':
            print("\n🔢 SIMPLE AGENT SELECTION")
            print("=" * 40)
            print("Select agent(s) to run:")
            print("- Enter single number (e.g., '2' for Python Expert)")
            print("- Enter multiple numbers separated by commas (e.g., '2,10' for Python + Security)")
            print("- Enter 'all' or '12' to run all agents")
            print()
            
            selection = input("Your selection: ").strip()
            
            if selection.lower() == 'all' or selection == str(len(available_agents) + 1):
                # Run all agents
                result = qa_crew.run_analysis(args.path, args.type, args.port)
            else:
                # Parse selected agent numbers
                try:
                    if ',' in selection:
                        # Multiple agents
                        agent_numbers = [int(x.strip()) for x in selection.split(',')]
                        selected_agents = []
                        for num in agent_numbers:
                            if 1 <= num <= len(available_agents):
                                selected_agents.append(available_agents[num - 1])
                            else:
                                print(f"❌ Invalid agent number: {num}")
                                return
                        
                        result = qa_crew.run_selected_agents_analysis(selected_agents, args.path, args.type, args.port)
                    else:
                        # Single agent
                        agent_num = int(selection)
                        if 1 <= agent_num <= len(available_agents):
                            selected_agent = available_agents[agent_num - 1]
                            result = qa_crew.run_single_agent_analysis(selected_agent, args.path, args.type, args.port)
                        else:
                            print(f"❌ Invalid agent number: {agent_num}")
                            return
                except ValueError:
                    print("❌ Invalid selection format. Please enter numbers or 'all'.")
                    return
        elif choice == '2':
            print("\n💬 NATURAL LANGUAGE REQUEST")
            print("=" * 40)
            print("Examples of what you can say:")
            print("• 'Check my Swift app for bugs and security vulnerabilities'")
            print("• 'Review my Python code for performance and best practices'")
            print("• 'Analyze my React components for accessibility issues'")
            print("• 'Do a complete security audit of my application'")
            print("• 'Check if my code follows best practices and is well documented'")
            print("• 'I need the Swift expert to review my code for bugs and the security expert to check for holes'")
            print()
            
            user_request = input("Describe what you want analyzed: ").strip()
            if user_request:
                result = qa_crew.run_natural_language_analysis(user_request, args.path, args.type, args.port)
            else:
                print("❌ No request provided.")
                return
        else:
            print("❌ Invalid choice. Please enter 1 or 2.")
            return
    
    print("\nFINAL RESULT:")
    print(result)

if __name__ == "__main__":
    main() 