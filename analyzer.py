# analyzer.py
# This is the most important file
# It reads code and finds problems
# Like a teacher checking your homework

import re  # re = regular expressions = pattern matching in text
from typing import List
from models import Issue

class CodeAnalyzer:
    """
    This class analyzes code and finds issues.
    
    It checks for:
    1. Bad variable names (x, y, z, tmp)
    2. Functions that are too long (hard to understand)
    3. Lines that are too long (hard to read)
    4. Missing error handling (no try/except)
    5. Repeated code patterns
    6. Empty except blocks (catching errors but doing nothing)
    7. Too many nested loops (slow code)
    """
    
    def __init__(self):
        # These are variable names that are too short
        # Good code uses descriptive names like "user_age" not "x"
        self.bad_variable_names = [
            'x', 'y', 'z', 'tmp', 'temp', 
            'var', 'data2', 'data3', 'foo', 'bar'
        ]
        
        # Functions longer than this are too complex
        self.max_function_lines = 30
        
        # Lines longer than this are hard to read
        self.max_line_length = 100
    
    def analyze(self, code: str, language: str) -> List[Issue]:
        """
        Main function — runs all checks on the code.
        Returns a list of issues found.
        """
        issues = []  # start with empty list of issues
        
        # Split code into individual lines
        lines = code.split('\n')
        
        # Run each check
        # Each check adds issues to our list if it finds problems
        issues.extend(self._check_line_length(lines))
        issues.extend(self._check_bad_variable_names(lines))
        issues.extend(self._check_empty_except(lines))
        issues.extend(self._check_missing_error_handling(lines, language))
        issues.extend(self._check_function_length(lines, language))
        issues.extend(self._check_nested_loops(lines))
        issues.extend(self._check_magic_numbers(lines))
        
        return issues
    
    def _check_line_length(self, lines: List[str]) -> List[Issue]:
        """
        Check if any line is too long.
        Long lines are hard to read.
        """
        issues = []
        
        for line_num, line in enumerate(lines, start=1):
            # enumerate gives us (index, value)
            # start=1 means we count from line 1 not line 0
            
            if len(line) > self.max_line_length:
                issues.append(Issue(
                    line_number=line_num,
                    issue_type="LINE_TOO_LONG",
                    description=f"Line is {len(line)} characters. Maximum is {self.max_line_length}.",
                    severity="low",
                    suggestion="Break this line into multiple shorter lines for readability."
                ))
        
        return issues
    
    def _check_bad_variable_names(self, lines: List[str]) -> List[Issue]:
        """
        Find variables with bad names like x, y, tmp.
        Good variable names describe what they contain.
        """
        issues = []
        
        for line_num, line in enumerate(lines, start=1):
            for bad_name in self.bad_variable_names:
                # This pattern looks for: bad_name = something
                # \b means word boundary (so 'x' doesnt match 'extra')
                pattern = rf'\b{bad_name}\s*='
                
                if re.search(pattern, line):
                    issues.append(Issue(
                        line_number=line_num,
                        issue_type="BAD_VARIABLE_NAME",
                        description=f"Variable '{bad_name}' is not descriptive.",
                        severity="medium",
                        suggestion=f"Replace '{bad_name}' with a descriptive name like 'user_count' or 'total_price'."
                    ))
        
        return issues
    
    def _check_empty_except(self, lines: List[str]) -> List[Issue]:
        """
        Find empty except blocks.
        Empty except = you catch an error but do nothing about it.
        This hides bugs and makes debugging impossible.
        
        Bad code:
        try:
            risky_operation()
        except:        ← catches error
            pass       ← does nothing! Bug hidden!
        """
        issues = []
        
        for line_num, line in enumerate(lines, start=1):
            stripped = line.strip()  # remove spaces from start and end
            
            # Check if this line is "except:" or "except Exception:"
            if stripped.startswith('except'):
                # Check if the NEXT line is just "pass"
                if line_num < len(lines):
                    next_line = lines[line_num].strip()
                    if next_line == 'pass':
                        issues.append(Issue(
                            line_number=line_num,
                            issue_type="EMPTY_EXCEPT_BLOCK",
                            description="Empty except block found. Error is caught but ignored.",
                            severity="high",
                            suggestion="Add logging or error handling inside the except block. Never silently ignore errors."
                        ))
        
        return issues
    
    def _check_missing_error_handling(self, lines: List[str], language: str) -> List[Issue]:
        """
        Check if file operations have error handling.
        Opening files can fail — always wrap in try/except.
        """
        issues = []
        
        if language.lower() != 'python':
            return issues  # only check Python for now
        
        for line_num, line in enumerate(lines, start=1):
            # Look for file open operations
            if 'open(' in line:
                # Check if this line is inside a try block
                # Simple check: look at surrounding lines
                start = max(0, line_num - 5)  # 5 lines before
                surrounding = lines[start:line_num]
                
                # If no 'try' found nearby, flag it
                has_try = any('try:' in l for l in surrounding)
                
                if not has_try:
                    issues.append(Issue(
                        line_number=line_num,
                        issue_type="MISSING_ERROR_HANDLING",
                        description="File operation without error handling.",
                        severity="high",
                        suggestion="Wrap file operations in try/except to handle FileNotFoundError."
                    ))
        
        return issues
    
    def _check_function_length(self, lines: List[str], language: str) -> List[Issue]:
        """
        Find functions that are too long.
        Long functions are hard to understand and test.
        Rule: if a function is longer than 30 lines, split it up.
        """
        issues = []
        
        if language.lower() != 'python':
            return issues
        
        function_start = None      # line where current function starts
        function_name = ""         # name of current function
        
        for line_num, line in enumerate(lines, start=1):
            stripped = line.strip()
            
            # Detect function start
            if stripped.startswith('def '):
                # If we were already in a function, check its length
                if function_start is not None:
                    length = line_num - function_start
                    if length > self.max_function_lines:
                        issues.append(Issue(
                            line_number=function_start,
                            issue_type="FUNCTION_TOO_LONG",
                            description=f"Function '{function_name}' is {length} lines long.",
                            severity="medium",
                            suggestion=f"Break '{function_name}' into smaller functions. Each function should do ONE thing."
                        ))
                
                # Start tracking new function
                function_start = line_num
                # Extract function name
                # "def my_function(args):" → "my_function"
                function_name = stripped.split('(')[0].replace('def ', '')
        
        return issues
    
    def _check_nested_loops(self, lines: List[str]) -> List[Issue]:
        """
        Find deeply nested loops.
        3 or more nested loops = O(n³) = very slow.
        
        Bad code:
        for i in range(n):        ← loop 1
            for j in range(n):    ← loop 2
                for k in range(n): ← loop 3 — TOO SLOW!
        """
        issues = []
        nesting_level = 0
        
        for line_num, line in enumerate(lines, start=1):
            stripped = line.strip()
            
            if stripped.startswith('for ') or stripped.startswith('while '):
                # Count indentation to find nesting level
                # Each 4 spaces = one level deeper
                indent = len(line) - len(line.lstrip())
                nesting_level = indent // 4
                
                if nesting_level >= 3:
                    issues.append(Issue(
                        line_number=line_num,
                        issue_type="DEEP_NESTING",
                        description=f"Loop nested {nesting_level} levels deep. This causes O(n^{nesting_level}) time complexity.",
                        severity="high",
                        suggestion="Refactor using helper functions or different data structures to reduce nesting."
                    ))
        
        return issues
    
    def _check_magic_numbers(self, lines: List[str]) -> List[Issue]:
        """
        Find magic numbers — unexplained numbers in code.
        
        Bad:  if age > 65:        ← what is 65? Why?
        Good: RETIREMENT_AGE = 65
              if age > RETIREMENT_AGE:  ← clear!
        """
        issues = []
        
        for line_num, line in enumerate(lines, start=1):
            stripped = line.strip()
            
            # Skip comments and constant definitions
            if stripped.startswith('#') or stripped.startswith('='):
                continue
            
            # Find numbers in code (not in string quotes)
            # Look for numbers greater than 1
            numbers = re.findall(r'(?<!["\'])\b([3-9][0-9]+)\b(?!["\'])', line)
            
            if numbers and '=' not in line.split('#')[0]:
                issues.append(Issue(
                    line_number=line_num,
                    issue_type="MAGIC_NUMBER",
                    description=f"Magic number(s) {numbers} found. Unclear what they mean.",
                    severity="low",
                    suggestion="Replace magic numbers with named constants. Example: MAX_RETRIES = 100"
                ))
        
        return issues