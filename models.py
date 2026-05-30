# models.py
# This file defines what data looks like
# Think of it as a contract — 
# "input must look like THIS, output will look like THIS"

from pydantic import BaseModel  
# pydantic checks that data has correct format
from typing import List, Optional

class CodeRequest(BaseModel):
    # This is what USER SENDS to your API
    code: str           # the actual code as text
    language: str       # "python", "javascript" etc
    filename: Optional[str] = "unknown"  # optional filename

class Issue(BaseModel):
    # One single problem found in the code
    line_number: int        # which line has the problem
    issue_type: str         # what kind of problem
    description: str        # explain the problem simply
    severity: str           # "low", "medium", "high"
    suggestion: str         # how to fix it

class AnalysisReport(BaseModel):
    # This is what YOUR API SENDS BACK
    filename: str
    language: str
    total_lines: int        # how many lines of code
    quality_score: float    # 0 to 100, higher is better
    issues: List[Issue]     # list of all problems found
    summary: str            # one line summary
    passed: bool            # is code good enough?