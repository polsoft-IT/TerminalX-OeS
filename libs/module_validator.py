"""
 ============================================================
  MODULE/PLUGIN NAME: ModuleValidator
  VERSION: 1.0.0
  MODULE CLASS: ModuleValidator
  DESCRIPTION:
       Module validation system for TerminalX

  AUTHOR:  Sebastian Januchowski
  COMPANY: polsoft.ITS™ Dev
  EMAIL:   polsoft.its@mail.com
  GITHUB:  polsoft-IT
  STATUS:  stable

 ============================================================
  COMPATIBILITY
 ============================================================
  PYTHON: 3.10+
  OS: Windows / Linux / macOS / Android (TerminalOS Runtime)
  ARCH: x86_64 / ARM64
  TERMINALOS KERNEL: v1.0+
"""

import ast
import os
import sys
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from pathlib import Path
from libs.clean_logger import CleanLogger, LogLevel
from libs.dependency_resolver import DependencyResolver, Dependency, DependencyType


@dataclass
class ValidationResult:
    """Validation result"""
    module_name: str
    valid: bool
    errors: List[str]
    warnings: List[str]
    info: Dict[str, Any]


class ModuleValidator:
    """Module validation system"""
    
    def __init__(self, dependency_resolver: Optional[DependencyResolver] = None,
                 logger: Optional[CleanLogger] = None):
        """
        Initialize module validator
        
        Args:
            dependency_resolver: Dependency resolver instance
            logger: Logger instance
        """
        self.logger = logger or CleanLogger("ModuleValidator", LogLevel.INFO)
        self.dependency_resolver = dependency_resolver or DependencyResolver()
        self.validation_rules: Dict[str, callable] = {}
        
        # Register default validation rules
        self._register_default_rules()
        
    def _register_default_rules(self) -> None:
        """Register default validation rules"""
        self.validation_rules['syntax'] = self._validate_syntax
        self.validation_rules['imports'] = self._validate_imports
        self.validation_rules['structure'] = self._validate_structure
        self.validation_rules['dependencies'] = self._validate_dependencies
        self.validation_rules['security'] = self._validate_security
        
    def validate_module(self, module_path: str, rules: Optional[List[str]] = None) -> ValidationResult:
        """
        Validate a module
        
        Args:
            module_path: Path to module file or directory
            rules: Validation rules to apply (None for all)
            
        Returns:
            Validation result
        """
        path = Path(module_path)
        module_name = path.name
        
        errors = []
        warnings = []
        info = {}
        
        # Determine if it's a file or directory
        if path.is_file():
            info['type'] = 'file'
            files_to_validate = [path]
        elif path.is_dir():
            info['type'] = 'package'
            files_to_validate = list(path.rglob('*.py'))
        else:
            return ValidationResult(
                module_name=module_name,
                valid=False,
                errors=['Path does not exist'],
                warnings=[],
                info={}
            )
            
        # Apply validation rules
        rules_to_apply = rules or list(self.validation_rules.keys())
        
        for rule_name in rules_to_apply:
            if rule_name in self.validation_rules:
                rule_errors, rule_warnings = self.validation_rules[rule_name](files_to_validate)
                errors.extend(rule_errors)
                warnings.extend(rule_warnings)
                
        valid = len(errors) == 0
        info['files_checked'] = len(files_to_validate)
        info['rules_applied'] = rules_to_apply
        
        return ValidationResult(
            module_name=module_name,
            valid=valid,
            errors=errors,
            warnings=warnings,
            info=info
        )
        
    def _validate_syntax(self, files: List[Path]) -> Tuple[List[str], List[str]]:
        """
        Validate Python syntax
        
        Args:
            files: List of Python files
            
        Returns:
            Tuple of (errors, warnings)
        """
        errors = []
        warnings = []
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    source = f.read()
                ast.parse(source, filename=str(file_path))
            except SyntaxError as e:
                errors.append(f"Syntax error in {file_path}: {e}")
            except UnicodeDecodeError:
                warnings.append(f"Could not read {file_path} as UTF-8")
                
        return errors, warnings
        
    def _validate_imports(self, files: List[Path]) -> Tuple[List[str], List[str]]:
        """
        Validate imports
        
        Args:
            files: List of Python files
            
        Returns:
            Tuple of (errors, warnings)
        """
        errors = []
        warnings = []
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    source = f.read()
                    
                tree = ast.parse(source, filename=str(file_path))
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            if not self._is_importable(alias.name):
                                warnings.append(f"Potentially unimportable module: {alias.name} in {file_path}")
                                
                    elif isinstance(node, ast.ImportFrom):
                        if node.module and not self._is_importable(node.module):
                            warnings.append(f"Potentially unimportable module: {node.module} in {file_path}")
                            
            except Exception:
                pass
                
        return errors, warnings
        
    def _is_importable(self, module_name: str) -> bool:
        """
        Check if module is importable
        
        Args:
            module_name: Module name
            
        Returns:
            True if importable
        """
        try:
            __import__(module_name)
            return True
        except ImportError:
            return False
            
    def _validate_structure(self, files: List[Path]) -> Tuple[List[str], List[str]]:
        """
        Validate module structure
        
        Args:
            files: List of Python files
            
        Returns:
            Tuple of (errors, warnings)
        """
        errors = []
        warnings = []
        
        # Check for __init__.py in directories
        directories = set(f.parent for f in files if f.parent.name)
        for directory in directories:
            if not (directory / '__init__.py').exists():
                warnings.append(f"Missing __init__.py in directory: {directory}")
                
        return errors, warnings
        
    def _validate_dependencies(self, files: List[Path]) -> Tuple[List[str], List[str]]:
        """
        Validate dependencies
        
        Args:
            files: List of Python files
            
        Returns:
            Tuple of (errors, warnings)
        """
        errors = []
        warnings = []
        
        # Check for requirements.txt or setup.py
        parent_dir = files[0].parent if files else Path('.')
        has_requirements = (parent_dir / 'requirements.txt').exists()
        has_setup = (parent_dir / 'setup.py').exists()
        
        if not has_requirements and not has_setup:
            warnings.append("No requirements.txt or setup.py found")
            
        return errors, warnings
        
    def _validate_security(self, files: List[Path]) -> Tuple[List[str], List[str]]:
        """
        Validate security issues
        
        Args:
            files: List of Python files
            
        Returns:
            Tuple of (errors, warnings)
        """
        errors = []
        warnings = []
        
        dangerous_patterns = [
            ('eval', 'Use of eval() is dangerous'),
            ('exec', 'Use of exec() is dangerous'),
            ('__import__', 'Direct use of __import__'),
            ('input(', 'Use of input() may be unsafe'),
            ('open(', 'File operations should be validated'),
        ]
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    source = f.read()
                    
                for pattern, message in dangerous_patterns:
                    if pattern in source:
                        warnings.append(f"{message} in {file_path}")
                        
            except Exception:
                pass
                
        return errors, warnings
        
    def add_validation_rule(self, name: str, rule: callable) -> None:
        """
        Add custom validation rule
        
        Args:
            name: Rule name
            rule: Rule function (files -> (errors, warnings))
        """
        self.validation_rules[name] = rule
        self.logger.info(f"Added validation rule: {name}")
        
    def remove_validation_rule(self, name: str) -> bool:
        """
        Remove validation rule
        
        Args:
            name: Rule name
            
        Returns:
            True if removed
        """
        if name in self.validation_rules:
            del self.validation_rules[name]
            self.logger.info(f"Removed validation rule: {name}")
            return True
        return False
        
    def validate_manifest(self, manifest_data: Dict[str, Any]) -> ValidationResult:
        """
        Validate module manifest
        
        Args:
            manifest_data: Manifest data dictionary
            
        Returns:
            Validation result
        """
        errors = []
        warnings = []
        
        # Required fields
        required_fields = ['name', 'version', 'author', 'description', 'entry_point']
        for field in required_fields:
            if field not in manifest_data:
                errors.append(f"Missing required field: {field}")
                
        # Validate version format
        if 'version' in manifest_data:
            version = manifest_data['version']
            if not self._is_valid_version(version):
                errors.append(f"Invalid version format: {version}")
                
        # Validate dependencies
        if 'dependencies' in manifest_data:
            for dep in manifest_data['dependencies']:
                if 'name' not in dep:
                    errors.append("Dependency missing 'name' field")
                    
        valid = len(errors) == 0
        
        return ValidationResult(
            module_name=manifest_data.get('name', 'unknown'),
            valid=valid,
            errors=errors,
            warnings=warnings,
            info={'type': 'manifest'}
        )
        
    def _is_valid_version(self, version: str) -> bool:
        """
        Check if version string is valid
        
        Args:
            version: Version string
            
        Returns:
            True if valid
        """
        parts = version.split('.')
        if len(parts) < 1 or len(parts) > 3:
            return False
            
        for part in parts:
            if not part.isdigit():
                return False
                
        return True
        
    def get_stats(self) -> Dict[str, any]:
        """
        Get validator statistics
        
        Returns:
            Statistics dictionary
        """
        return {
            'validation_rules': len(self.validation_rules),
            'rule_names': list(self.validation_rules.keys())
        }


# Global module validator instance
module_validator = ModuleValidator()
