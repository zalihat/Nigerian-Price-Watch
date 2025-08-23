import boto3
import io
import pandas as pd

# Connect to MinIO
s3 = boto3.client(
    's3',
    endpoint_url="http://localhost:9000",  # MinIO server URL
    aws_access_key_id="minioadmin",        # Change if you set different creds
    aws_secret_access_key="minioadmin"
)

# Example: save DataFrame to MinIO without saving locally
df = pd.DataFrame({"name": ["apple", "banana"], "price": [2, 3]})

# Convert DataFrame to Parquet in memory
buffer = io.BytesIO()
df.to_parquet(buffer, index=False)
buffer.seek(0)

# Upload directly to MinIO
s3.upload_fileobj(buffer, "datalake", "silver/mydata.parquet")
print("✅ Uploaded directly to MinIO")
