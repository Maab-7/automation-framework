# Automation Framework - Digital Harbor

## Setup

1. Create virtual environment
   python -m venv venv
2. Activate venv
   source venv/bin/activate (Linux/Mac)
   venv\Scripts\activate (Windows)

3. Install dependencies
   pip install -r requirements.txt

## Run Tests

pytest tests/

## Run with Report

pytest tests/ --html=reports/report.html
