import os
import boto3
import glob
from pathlib import Path
from ingest_to_s3 import IngestData

def lambda_handler(event, context):
    ingest_data = IngestData()

    old_page_url = "https://nigerianstat.gov.ng/elibrary"
    new_page_url = "https://microdata.nigerianstat.gov.ng/index.php/catalog/162/study-description"

    # Run ingestion
    ingest_data.ingest_old_page_data(old_page_url)
    ingest_data.ingest_new_page_data(new_page_url)

  

    return {"status": "done"}
