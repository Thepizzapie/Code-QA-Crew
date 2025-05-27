#!/usr/bin/env python3

"""
CrewAI-compatible tools that wrap our LangChain functionality
"""

from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import qa_tools

class CodeStructureInput(BaseModel):
    """Input schema for code structure analysis."""
    folder_path: str = Field(description="Path to the code directory or file to analyze")

class CodeStructureTool(BaseTool):
    name: str = "analyze_code_structure"
    description: str = "Analyze code structure using real Python execution and file system analysis"
    args_schema: Type[BaseModel] = CodeStructureInput

    def _run(self, folder_path: str) -> str:
        """Execute the code structure analysis."""
        return qa_tools.analyze_code_structure.invoke({"folder_path": folder_path})

class PythonSyntaxInput(BaseModel):
    """Input schema for Python syntax checking."""
    code_path: str = Field(description="Path to Python file or directory")

class PythonSyntaxTool(BaseTool):
    name: str = "check_python_syntax"
    description: str = "Check Python syntax using real AST parsing and linting"
    args_schema: Type[BaseModel] = PythonSyntaxInput

    def _run(self, code_path: str) -> str:
        """Execute the Python syntax check."""
        return qa_tools.check_python_syntax.invoke({"code_path": code_path})

class SecurityScanInput(BaseModel):
    """Input schema for security vulnerability scanning."""
    code_path: str = Field(description="Path to code to scan for security issues")

class SecurityScanTool(BaseTool):
    name: str = "scan_security_vulnerabilities"
    description: str = "Scan for security vulnerabilities using real pattern matching"
    args_schema: Type[BaseModel] = SecurityScanInput

    def _run(self, code_path: str) -> str:
        """Execute the security vulnerability scan."""
        return qa_tools.scan_security_vulnerabilities.invoke({"code_path": code_path})

class DependencyCheckInput(BaseModel):
    """Input schema for dependency checking."""
    code_path: str = Field(description="Path to project with dependency files")

class DependencyCheckTool(BaseTool):
    name: str = "check_package_dependencies"
    description: str = "Check package dependencies for validity, security, and compatibility"
    args_schema: Type[BaseModel] = DependencyCheckInput

    def _run(self, code_path: str) -> str:
        """Execute the dependency check."""
        return qa_tools.check_package_dependencies.invoke({"code_path": code_path})

class LocalhostCheckInput(BaseModel):
    """Input schema for localhost checking."""
    port: str = Field(default="3000", description="Port number to check")
    path: str = Field(default="/", description="Path to check on the site")

class LocalhostCheckTool(BaseTool):
    name: str = "check_localhost_site"
    description: str = "Check if a localhost site is operational and accessible"
    args_schema: Type[BaseModel] = LocalhostCheckInput

    def _run(self, port: str = "3000", path: str = "/") -> str:
        """Execute the localhost check."""
        return qa_tools.check_localhost_site.invoke({"port": port, "path": path})

class GeneralQAInput(BaseModel):
    """Input schema for general QA testing."""
    code_path: str = Field(description="Path to code to test")

class GeneralQATool(BaseTool):
    name: str = "run_general_qa_tests"
    description: str = "Run general QA tests including code quality, documentation, and testing coverage"
    args_schema: Type[BaseModel] = GeneralQAInput

    def _run(self, code_path: str) -> str:
        """Execute the general QA tests."""
        return qa_tools.run_general_qa_tests.invoke({"code_path": code_path})

class ReactAnalysisInput(BaseModel):
    """Input schema for React component analysis."""
    code_path: str = Field(description="Path to React project or component files")

class ReactAnalysisTool(BaseTool):
    name: str = "analyze_react_components"
    description: str = "Analyze React components for best practices and common issues"
    args_schema: Type[BaseModel] = ReactAnalysisInput

    def _run(self, code_path: str) -> str:
        """Execute the React component analysis."""
        return qa_tools.analyze_react_components.invoke({"code_path": code_path})

class SQLValidationInput(BaseModel):
    """Input schema for SQL validation."""
    code_path: str = Field(description="Path to files containing SQL queries")

class SQLValidationTool(BaseTool):
    name: str = "validate_sql_queries"
    description: str = "Validate SQL queries and database interactions"
    args_schema: Type[BaseModel] = SQLValidationInput

    def _run(self, code_path: str) -> str:
        """Execute the SQL validation."""
        return qa_tools.validate_sql_queries.invoke({"code_path": code_path})

class CodeComplexityInput(BaseModel):
    """Input schema for code complexity analysis."""
    code_path: str = Field(description="Path to code to analyze")

class CodeComplexityTool(BaseTool):
    name: str = "analyze_code_complexity"
    description: str = "Analyze code complexity metrics and identify areas for improvement"
    args_schema: Type[BaseModel] = CodeComplexityInput

    def _run(self, code_path: str) -> str:
        """Execute the code complexity analysis."""
        return qa_tools.analyze_code_complexity.invoke({"code_path": code_path})

class BestPracticesInput(BaseModel):
    """Input schema for best practices checking."""
    code_path: str = Field(description="Path to code to check")

class BestPracticesTool(BaseTool):
    name: str = "check_best_practices"
    description: str = "Check adherence to coding best practices and standards"
    args_schema: Type[BaseModel] = BestPracticesInput

    def _run(self, code_path: str) -> str:
        """Execute the best practices check."""
        return qa_tools.check_best_practices.invoke({"code_path": code_path})

class ImportValidationInput(BaseModel):
    """Input schema for import validation."""
    code_path: str = Field(description="Path to code to validate imports")

class ImportValidationTool(BaseTool):
    name: str = "validate_imports"
    description: str = "Validate import statements and dependencies"
    args_schema: Type[BaseModel] = ImportValidationInput

    def _run(self, code_path: str) -> str:
        """Execute the import validation."""
        return qa_tools.validate_imports.invoke({"code_path": code_path})

# Create instances of all tools for easy import
analyze_code_structure = CodeStructureTool()
check_python_syntax = PythonSyntaxTool()
scan_security_vulnerabilities = SecurityScanTool()
check_package_dependencies = DependencyCheckTool()
check_localhost_site = LocalhostCheckTool()
run_general_qa_tests = GeneralQATool()
analyze_react_components = ReactAnalysisTool()
validate_sql_queries = SQLValidationTool()
analyze_code_complexity = CodeComplexityTool()
check_best_practices = BestPracticesTool()
validate_imports = ImportValidationTool() 