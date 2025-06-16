"""
Configuration settings for the Streamlit app.
"""
import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()


class AppConfig:
    """Application configuration class."""
    
    # Azure Storage Settings
    STORAGE_ACCOUNT_NAME = "storage"
    CONTAINER_NAME = "data"
    BLOB_NAME = "sample_data.csv"
    
    # App Settings
    APP_TITLE = "Document Management Portal"
    APP_DESCRIPTION = "Multi-application document management system with AI-powered analysis"
    
    # Multi-page App Settings
    PORTAL_TITLE = "Document Management Portal"
    APP1_TITLE = "Assessment/Plan Extractor"
    APP2_TITLE = "Document Summarizer"
    APP_DESCRIPTION = "This Streamlit app loads and displays data from Azure Blob Storage."
    
    # Chart Settings
    DEFAULT_CHART_HEIGHT = 400
    DEFAULT_CHART_WIDTH = 600
    
    @classmethod
    def get_azure_storage_config(cls) -> Dict[str, str]:
        """Get Azure Storage configuration."""
        return {
            "storage_account_name": cls.STORAGE_ACCOUNT_NAME,
            "container_name": cls.CONTAINER_NAME,
            "blob_name": cls.BLOB_NAME,
            "connection_string": os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        }
    
    @classmethod
    def get_app_config(cls) -> Dict[str, Any]:
        """Get general app configuration."""
        return {
            "title": cls.APP_TITLE,
            "description": cls.APP_DESCRIPTION,
            "chart_height": cls.DEFAULT_CHART_HEIGHT,
            "chart_width": cls.DEFAULT_CHART_WIDTH
        }
    
    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production environment."""
        return os.getenv('WEBSITE_SITE_NAME') is not None
    
    @classmethod
    def get_environment(cls) -> str:
        """Get current environment (development or production)."""
        return "production" if cls.is_production() else "development"
