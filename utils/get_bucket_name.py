import json
import subprocess

def get_bucket_name(service_path="../infrastructure/services/s3"):
    result = subprocess.run(
        ["terraform", "output", "-json"],
        cwd=service_path,
        capture_output=True,
        text=True,
        check=True
    )
    outputs = json.loads(result.stdout)
    return outputs["bucket_name"]["value"]

if __name__ == "__main__":
    bucket_name = get_bucket_name()
    file = "ingest_to_s3.py" 
    # Update ingestdata.py (or generate a config file)
    with open(file, "r") as f:
        code = f.read()
 
    # Replace placeholder (e.g., BUCKET_NAME = "REPLACE_ME")
    code = code.replace("REPLACE_BUCKET_NAME", bucket_name)

    with open(file, "w") as f:
        f.write(code)

    print(f"Inserted bucket name: {bucket_name} into {file}")
