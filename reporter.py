# reporter.py
# Takes the list of issues and creates a clean report
# Like a teacher grading your code

from typing import List
from models import Issue, AnalysisReport

class Reporter:
    
    def generate_report(
        self, 
        code: str,
        language: str,
        filename: str,
        issues: List[Issue]
    ) -> AnalysisReport:
        """
        Takes raw issues and creates a complete report.
        Calculates quality score based on issues found.
        """
        
        # Count total lines
        total_lines = len(code.split('\n'))
        
        # Calculate quality score
        # Start at 100, subtract points for each issue
        score = self._calculate_score(issues, total_lines)
        
        # Create summary sentence
        summary = self._create_summary(issues, score)
        
        # Code passes if score is above 70
        passed = score >= 70.0
        
        return AnalysisReport(
            filename=filename,
            language=language,
            total_lines=total_lines,
            quality_score=round(score, 1),
            issues=issues,
            summary=summary,
            passed=passed
        )
    
    def _calculate_score(
        self, 
        issues: List[Issue], 
        total_lines: int
    ) -> float:
        """
        Score starts at 100.
        High severity issues: -10 points each
        Medium severity issues: -5 points each
        Low severity issues: -2 points each
        Score never goes below 0.
        """
        score = 100.0
        
        # Points to subtract per severity
        severity_weights = {
            'high': 10,
            'medium': 5,
            'low': 2
        }
        
        for issue in issues:
            # Get weight for this severity
            # If severity not found, default to 3
            weight = severity_weights.get(issue.severity, 3)
            score -= weight
        
        # Score cannot go below 0
        return max(0.0, score)
    
    def _create_summary(
        self, 
        issues: List[Issue], 
        score: float
    ) -> str:
        """Creates a one-line human readable summary."""
        
        total = len(issues)
        
        # Count by severity
        high = sum(1 for i in issues if i.severity == 'high')
        medium = sum(1 for i in issues if i.severity == 'medium')
        low = sum(1 for i in issues if i.severity == 'low')
        
        if total == 0:
            return "Excellent! No issues found. Code quality is perfect."
        
        if score >= 80:
            quality = "Good"
        elif score >= 60:
            quality = "Needs improvement"
        else:
            quality = "Poor"
        
        return (
            f"{quality} code quality (score: {score:.0f}/100). "
            f"Found {total} issues: "
            f"{high} high, {medium} medium, {low} low severity."
        )