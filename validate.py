#!/usr/bin/env python3
"""
Validation script to test all components of the Streamlit Azure app.
"""

print('=== FINAL VALIDATION REPORT ===')
print()

# Test environment loading
from dotenv import load_dotenv
import os
load_dotenv()
conn_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
print(f'✅ Environment: Connection string loaded ({len(conn_str)} chars)')

# Test configuration
from config import AppConfig
config = AppConfig.get_azure_storage_config()
app_config = AppConfig.get_app_config()
print(f'✅ Configuration: Azure config loaded')
print(f'   - Storage Account: {config["storage_account_name"]}')
print(f'   - Container: {config["container_name"]}')
print(f'   - Blob: {config["blob_name"]}')
print(f'   - App Title: {app_config["title"]}')

# Test blob storage
from blob_storage import create_blob_manager
blob_manager = create_blob_manager(config['storage_account_name'], config['container_name'])
print(f'✅ Blob Storage: Manager initialized')

# Test data loading
df = blob_manager.download_csv_as_dataframe(config['blob_name'])
print(f'✅ Data Loading: CSV loaded successfully')
print(f'   - Shape: {df.shape[0]} rows × {df.shape[1]} columns')
print(f'   - Columns: {list(df.columns)}')

# Test blob existence check
exists = blob_manager.check_blob_exists(config['blob_name'])
print(f'✅ Blob Check: File exists = {exists}')

print()
print('🎉 ALL TESTS PASSED - Ready for development and deployment!')
print()
print('📊 Sample Data Preview:')
print(df.head(3))
