#!/bin/bash
# Startup script for Azure App Service

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Start Streamlit app with the correct configuration for Azure
exec streamlit run Home.py --server.port $PORT --server.address 0.0.0.0 --server.headless true --server.enableCORS false
