#!/bin/bash

# Azure Streamlit App Deployment Script
# Usage: ./deploy.sh

set -e  # Exit on any error

echo "🚀 Starting deployment process..."

# Configuration
RESOURCE_GROUP=""
APP_NAME="streamlit"

# Clean up old deployment files
echo "🧹 Cleaning up old deployment files..."
rm -f app.zip

# Check syntax before deployment
echo "🔍 Checking syntax..."
python -m py_compile Home.py utils/config.py utils/blob_storage.py utils/mock_data.py
find pages -name "*.py" -exec python -m py_compile {} \;
if [ $? -ne 0 ]; then
    echo "❌ Syntax errors found! Please fix before deploying."
    exit 1
fi
echo "✅ Syntax check passed!"

# Create deployment package with all necessary files
echo "📦 Creating deployment package..."
zip -r app.zip \
    Home.py \
    pages/ \
    utils/ \
    startup.sh \
    requirements.txt \
    Procfile \
    .deployment

echo "📋 Deployment package contents:"
unzip -l app.zip

# Deploy to Azure
echo "☁️  Deploying to Azure App Service..."
az webapp deploy \
    --resource-group "$RESOURCE_GROUP" \
    --name "$APP_NAME" \
    --src-path app.zip \
    --type zip

# Check deployment status
echo "✅ Deployment completed!"
echo "🌐 Your app is available at: https://${APP_NAME}.azurewebsites.net"

# Optional: Open logs
read -p "🔍 Do you want to view real-time logs? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📊 Opening real-time logs..."
    az webapp log tail --name "$APP_NAME" --resource-group "$RESOURCE_GROUP"
fi
