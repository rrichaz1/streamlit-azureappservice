#!/bin/bash

# Local Development Script for Streamlit App
# This script runs the Streamlit app locally with proper environment setup

echo "🚀 Starting Streamlit app locally..."

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "Please create a .env file with your Azure Storage connection string:"
    echo "AZURE_STORAGE_CONNECTION_STRING=your_connection_string_here"
    exit 1
fi

echo "✅ Found .env file"

# Check if required packages are installed
echo "📦 Checking dependencies..."
pip install -r requirements.txt

# Run syntax check
echo "🔍 Checking syntax..."
python -m py_compile app.py blob_storage.py config.py
if [ $? -ne 0 ]; then
    echo "❌ Syntax errors found! Please fix before running."
    exit 1
fi

echo "✅ All checks passed!"
echo "🌐 Starting Streamlit on http://localhost:8501"
echo "📝 The app will automatically load your .env file"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the Streamlit app
streamlit run app.py
