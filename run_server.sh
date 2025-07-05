#!/bin/bash

# Simple script to run a local Python web server for the GA4 demo site

PORT=8000

echo "🚀 Starting local web server..."
echo "📱 Site will be available at: http://localhost:$PORT"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

# Check if Python 3 is available
if command -v python3 &> /dev/null; then
    echo "Using Python 3..."
    python3 -m http.server $PORT
elif command -v python &> /dev/null; then
    echo "Using Python 2..."
    python -m SimpleHTTPServer $PORT
else
    echo "❌ Error: Python not found. Please install Python to run the server."
    exit 1
fi