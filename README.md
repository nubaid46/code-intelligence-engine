# code-intelligence-engine
AI-powered REST API that analyzes Python code quality,  detects anti-patterns, and returns quality scores with  fix suggestions. Built with FastAPI and rule-based  static analysis engine from scratch.
# Code Intelligence Engine

An AI-powered REST API that analyzes Python code 
quality and detects anti-patterns automatically.

## What it does
- Detects bad variable names
- Finds deeply nested loops (O(n³) complexity)
- Identifies empty exception handlers
- Flags magic numbers
- Returns quality score 0-100

## Built with
- FastAPI
- Python
- Regex pattern matching
- Rule-based static analysis

## How to run
pip install fastapi uvicorn pydantic
uvicorn main:app --reload

## API Endpoints
POST /analyze → analyze code quality
GET /health → check server status

## Example
Send any Python code → get quality score + 
specific issues with fix suggestions
