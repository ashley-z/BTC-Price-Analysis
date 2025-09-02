#!/bin/bash

# Bitcoin Price Analysis Dashboard Startup Script

echo "🚀 Starting Bitcoin Price Analysis Dashboard..."
echo "=============================================="

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed or not in PATH"
    exit 1
fi

# Check if required files exist
if [ ! -f "dashboard.py" ]; then
    echo "❌ dashboard.py not found in current directory"
    exit 1
fi

# Check if requirements are installed
echo "Checking dependencies..."
python -c "import dash, pandas, numpy, plotly" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Required dependencies not installed"
    echo "Please run: pip install -r requirements.txt"
    exit 1
fi

echo "✅ Dependencies check passed"
echo ""

# Start the dashboard
echo "Starting dashboard at http://127.0.0.1:8050"
echo "Press Ctrl+C to stop the dashboard"
echo ""

python dashboard.py

