"""
Azure Blob Storage utilities for the Streamlit app.
"""
import os
import pandas as pd
import io
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential


class BlobStorageManager:
    """Manages Azure Blob Storage operations for the application."""
    
    def __init__(self, storage_account_name: str, container_name: str):
        """
        Initialize the BlobStorageManager.
        
        Args:
            storage_account_name: Name of the Azure Storage Account
            container_name: Name of the blob container
        """
        self.storage_account_name = storage_account_name
        self.container_name = container_name
        self.connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        self._blob_service_client = None
    
    def _get_blob_service_client(self) -> BlobServiceClient:
        """Get the blob service client with appropriate authentication."""
        if self._blob_service_client is None:
            if self.connection_string:
                # Use connection string if available (local dev or explicit config)
                self._blob_service_client = BlobServiceClient.from_connection_string(
                    self.connection_string
                )
            else:
                # Use default Azure credential (Managed Identity in Azure App Service)
                account_url = f"https://{self.storage_account_name}.blob.core.windows.net"
                self._blob_service_client = BlobServiceClient(
                    account_url, 
                    credential=DefaultAzureCredential()
                )
        return self._blob_service_client
    
    def download_csv_as_dataframe(self, blob_name: str) -> pd.DataFrame:
        """
        Download a CSV blob and return it as a pandas DataFrame.
        
        Args:
            blob_name: Name of the blob file to download
            
        Returns:
            pandas.DataFrame: The CSV data as a DataFrame
            
        Raises:
            Exception: If there's an error downloading or parsing the blob
        """
        try:
            blob_service_client = self._get_blob_service_client()
            blob_client = blob_service_client.get_blob_client(
                container=self.container_name, 
                blob=blob_name
            )
            
            # Download blob data
            blob_data = blob_client.download_blob()
            csv_content = blob_data.readall()
            
            # Parse CSV content into DataFrame
            df = pd.read_csv(io.BytesIO(csv_content))
            
            return df
            
        except Exception as e:
            raise Exception(f"Error loading data from blob storage: {str(e)}")
    
    def list_blobs(self) -> list:
        """
        List all blobs in the container.
        
        Returns:
            list: List of blob names in the container
        """
        try:
            blob_service_client = self._get_blob_service_client()
            container_client = blob_service_client.get_container_client(self.container_name)
            
            blob_list = []
            for blob in container_client.list_blobs():
                blob_list.append(blob.name)
            
            return blob_list
            
        except Exception as e:
            raise Exception(f"Error listing blobs: {str(e)}")
    
    def check_blob_exists(self, blob_name: str) -> bool:
        """
        Check if a specific blob exists in the container.
        
        Args:
            blob_name: Name of the blob to check
            
        Returns:
            bool: True if blob exists, False otherwise
        """
        try:
            blob_service_client = self._get_blob_service_client()
            blob_client = blob_service_client.get_blob_client(
                container=self.container_name, 
                blob=blob_name
            )
            
            return blob_client.exists()
            
        except Exception:
            return False


# Factory function for easy instantiation
def create_blob_manager(storage_account_name: str, container_name: str) -> BlobStorageManager:
    """
    Factory function to create a BlobStorageManager instance.
    
    Args:
        storage_account_name: Name of the Azure Storage Account
        container_name: Name of the blob container
        
    Returns:
        BlobStorageManager: Configured blob storage manager instance
    """
    return BlobStorageManager(storage_account_name, container_name)
