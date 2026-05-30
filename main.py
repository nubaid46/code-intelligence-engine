# main.py
# This is the FastAPI server
# It receives requests, calls analyzer, returns reports

from fastapi import FastAPI, HTTPException
from models import CodeRequest, AnalysisReport
from analyzer import CodeAnalyzer
from reporter import Reporter

# Create the FastAPI app
app = FastAPI(
    title="Code Intelligence Engine",
    description="Analyzes code quality and detects anti-patterns",
    version="1.0.0"
)

# Create instances of our tools
# These are created ONCE when server starts
analyzer = CodeAnalyzer()
reporter = Reporter()

@app.get("/")
def home():
    """Health check — tells you server is running."""
    return {
        "status": "running",
        "service": "Code Intelligence Engine",
        "version": "1.0.0"
    }

@app.post("/analyze", response_model=AnalysisReport)
def analyze_code(request: CodeRequest):
    """
    Main endpoint — analyzes submitted code.
    
    Send POST request with:
    {
        "code": "your code here",
        "language": "python",
        "filename": "myfile.py"
    }
    
    Returns complete analysis report.
    """
    
    # Validate input
    if not request.code.strip():
        raise HTTPException(
            status_code=400,
            detail="Code cannot be empty"
        )
    
    if len(request.code) > 50000:
        raise HTTPException(
            status_code=400,
            detail="Code too large. Maximum 50,000 characters."
        )
    
    # Run analysis
    issues = analyzer.analyze(
        code=request.code,
        language=request.language
    )
    
    # Generate report
    report = reporter.generate_report(
        code=request.code,
        language=request.language,
        filename=request.filename or "unknown",
        issues=issues
    )
    
    return report

@app.get("/health")
def health_check():
    """Simple health check for deployment monitoring."""
    return {"status": "healthy"}