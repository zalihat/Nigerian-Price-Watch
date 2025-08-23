import os
import boto3
import glob
from pathlib import Path
from ingest_to_s3 import IngestData

def lambda_handler(event, context):
    ingest_data = IngestData()

    old_page_url = "https://nigerianstat.gov.ng/elibrary"
    new_page_url = "https://microdata.nigerianstat.gov.ng/index.php/catalog/162/study-description"

    output_dir = "/tmp/bronze"
    metadata_file = "/tmp/bronze_metadata.json"
    bucket = os.environ["S3_BUCKET"]

    # Run ingestion
    ingest_data.ingest_old_page_data(old_page_url)
    ingest_data.ingest_new_page_data(new_page_url)

    # Upload results to S3
    s3 = boto3.client("s3")
    for file in glob.glob(f"{output_dir}/*.xlsx"):
        s3.upload_file(file, bucket, f"bronze/{os.path.basename(file)}")

    if os.path.exists(metadata_file):
        s3.upload_file(metadata_file, bucket, "bronze/bronze_metadata.json")

    return {"status": "done"}
