from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
import pandas as pd
import os
from io import StringIO

# Load Azure connection string securely from .env file (not exposed in code)
def load_data():
    load_dotenv()
    conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    blob_client = BlobServiceClient.from_connection_string(conn_str).get_blob_client(
        container="raw-data", blob="claims_data.csv")
    csv_data = blob_client.download_blob().readall().decode("utf-8")
    return pd.read_csv(StringIO(csv_data), sep=';')