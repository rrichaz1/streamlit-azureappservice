# Streamlit Azure Data Dashboard

A modern Streamlit application that loads and visualizes CSV data from Azure Blob Storage, with interactive analytics and deployment automation.

App cretaed with Github COPILOT - AGENT mode with Claude 4

## 🚀 Features

- 📊 Interactive data dashboard with multiple visualization tabs
- ☁️ Azure Blob Storage integration for data loading
- 📈 Data analytics with charts, histograms, and statistics
- 🎨 Modern UI with sidebar information panel
- 📱 Responsive design
- ⬇️ CSV download functionality
- 🔄 Automated deployment to Azure App Service

## 🛠️ Setup

### 1. Environment Variables

Copy the example environment file and configure your settings:

```bash
cp .env.example .env
```

Edit `.env` and add your actual values:
- `GOOGLE_API_KEY`: Your Google API key (if using AI features)
- `AZURE_STORAGE_CONNECTION_STRING`: Your Azure Storage connection string

### 2. Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the app locally:
   ```bash
   ./run_local.sh
   # or manually: streamlit run app.py
   ```

### 3. Azure Storage Setup

1. Create an Azure Storage Account
2. Create a container named `data`
3. Upload your CSV file as `sample_data.csv`
4. Copy the connection string to your `.env` file

## Direct Deployment to Azure App Service (No Docker Required)

This project is configured for direct deployment to Azure App Service using Python runtime.

### Project Structure
```
├── app.py               # Main Streamlit application (clean UI code)
├── blob_storage.py      # Azure Blob Storage operations
├── config.py            # Application configuration
├── requirements.txt     # Python dependencies
├── Procfile            # Startup command for Azure
├── startup.sh          # Custom startup script
├── deploy.sh           # Automated deployment script
├── .deployment         # Azure deployment configuration
├── .gitignore          # Files to exclude from deployment
└── README.md           # This file
```

## Step-by-Step Deployment Instructions

### Method 1: Azure CLI Deployment (Recommended)

#### 1. Prerequisites
- Azure account (https://portal.azure.com)
- Azure CLI installed (`brew install azure-cli` on macOS)

#### 2. Login to Azure
```sh
az login
```

#### 3. Create Azure Resources
```sh
# Set variables (replace with your values)
RESOURCE_GROUP="streamlit"
APP_NAME="streamlit"
LOCATION="eastus"

# Create resource group (if it doesn't exist)
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create App Service Plan for Linux
az appservice plan create \
  --name ${APP_NAME}-plan \
  --resource-group $RESOURCE_GROUP \
  --sku B1 \
  --is-linux

# Create Web App with Python 3.11 runtime
az webapp create \
  --resource-group $RESOURCE_GROUP \
  --plan ${APP_NAME}-plan \
  --name $APP_NAME \
  --runtime "PYTHON|3.11"
```

#### 4. Deploy Your Code (Corrected Scripts)

**Method A: Using the automated deployment script (Recommended)**
```sh
# Make the script executable (first time only)
chmod +x deploy.sh

# Run the deployment script
./deploy.sh
```

**Method B: Manual deployment with corrected zip command**
```sh
# Clean up unnecessary files
rm -rf .venv .azure __pycache__ *.pyc app.zip

# Create deployment package (CORRECTED - includes all necessary files)
zip -r app.zip \
    app.py \
    blob_storage.py \
    config.py \
    startup.sh \
    requirements.txt \
    Procfile \
    .deployment

# Deploy to Azure
az webapp deploy \
  --resource-group $RESOURCE_GROUP \
  --name $APP_NAME \
  --src-path app.zip \
  --type zip
```

#### 5. Configure App Settings (Important!)
```sh
# Set the startup command to use your Procfile
az webapp config set \
  --resource-group $RESOURCE_GROUP \
  --name $APP_NAME \
  --startup-file "startup.sh"

# Set Azure Storage connection string for blob access
az webapp config appsettings set \
  --resource-group $RESOURCE_GROUP \
  --name $APP_NAME \
  --settings AZURE_STORAGE_CONNECTION_STRING="your_connection_string_here"

# Enable application logging
az webapp log config \
  --resource-group $RESOURCE_GROUP \
  --name $APP_NAME \
  --application-logging filesystem \
  --level information
```

#### 6. Browse to Your App
```sh
echo "Your app is available at: https://${APP_NAME}.azurewebsites.net"
```

### Method 2: VS Code Azure Extension

1. **Install Azure App Service Extension**
   - Open Extensions (`Cmd+Shift+X`)
   - Search for "Azure App Service"
   - Install the extension

2. **Sign in to Azure**
   - Click Azure icon in sidebar
   - Sign in to your Azure account

3. **Deploy**
   - Right-click your project folder
   - Select "Deploy to Web App..."
   - Choose Python 3.11 runtime
   - Follow the prompts

### Method 3: Git Deployment

#### Setup Git deployment source:
```sh
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit"

# Configure deployment source
az webapp deployment source config-local-git \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP

# Get the Git URL and deploy
git remote add azure $(az webapp deployment source config-local-git --name $APP_NAME --resource-group $RESOURCE_GROUP --query url --output tsv)
git push azure main
```

## Troubleshooting

### Check Application Logs
```sh
# Stream logs in real-time
az webapp log tail --name $RG  --resource-group $resourcegroup

# Download log files
az webapp log download --name $RG  --resource-group $resourcegroup
```

### Common Issues and Solutions

1. **App shows default Azure page**
   - Ensure `Procfile` is in the root directory
   - Check that startup command is configured correctly
   - Verify Python version is set to 3.11

2. **Module not found errors**
   - Ensure all dependencies are in `requirements.txt`
   - Check deployment logs for pip install errors

3. **Port binding issues**
   - Verify Procfile uses `$PORT` environment variable
   - Ensure `--server.address 0.0.0.0` is specified

4. **Streamlit specific issues**
   - Add `--server.headless true` to Procfile
   - Check if CORS settings need configuration

### Test Locally Before Deployment
```sh
# Install dependencies
pip install -r requirements.txt

# Test the exact command from Procfile
PORT=8000 streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true
```

### Quick Fix Commands
If your current deployment isn't working, try these:

```sh
# Set the correct Python version
az webapp config set --resource-group $RG --name $APP--python-version 3.11

# Configure startup file
az webapp config set --resource-group $RG --name $APP--startup-file "startup.sh"

# Restart the app
az webapp restart --name $APP--resource-group $RG
```

For more details, see Azure’s official documentation: https://learn.microsoft.com/en-us/azure/app-service/quickstart-python


