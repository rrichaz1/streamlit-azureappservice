#!/bin/bash
# Azure Blob Storage setup script

# Variables
RESOURCE_GROUP=""
STORAGE_ACCOUNT=""
CONTAINER_NAME="data"
APP_NAME="streamlit"

echo "Setting up Azure Blob Storage for Streamlit app..."

# Create storage account
echo "Creating storage account: $STORAGE_ACCOUNT"
az storage account create \
    --name $STORAGE_ACCOUNT \
    --resource-group $RESOURCE_GROUP \
    --location canadacentral \
    --sku Standard_LRS

# Create container
echo "Creating container: $CONTAINER_NAME"
az storage container create \
    --name $CONTAINER_NAME \
    --account-name $STORAGE_ACCOUNT

# Upload sample CSV
echo "Uploading sample_data.csv to container"
az storage blob upload \
    --file sample_data.csv \
    --container-name $CONTAINER_NAME \
    --name sample_data.csv \
    --account-name $STORAGE_ACCOUNT

# Get connection string
echo "Getting storage connection string..."
CONNECTION_STRING=$(az storage account show-connection-string \
    --name $STORAGE_ACCOUNT \
    --resource-group $RESOURCE_GROUP \
    --output tsv)

# Set app setting
echo "Configuring App Service with storage connection string..."
az webapp config appsettings set \
    --resource-group $RESOURCE_GROUP \
    --name $APP_NAME \
    --settings AZURE_STORAGE_CONNECTION_STRING="$CONNECTION_STRING"

echo "✅ Azure Blob Storage setup complete!"
echo "Storage Account: $STORAGE_ACCOUNT"
echo "Container: $CONTAINER_NAME"
echo "Sample CSV uploaded and App Service configured."
