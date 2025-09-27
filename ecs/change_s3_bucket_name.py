import sys
import shutil

if len(sys.argv) != 3:
    print("Usage: python inject_bucket.py <bucket_name> <file_path>")
    sys.exit(1)

bucket_name = sys.argv[1]
file_path = sys.argv[2]
tmp_path = file_path + ".tmp"

with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

code = code.replace("REPLACE_BUCKET_NAME", bucket_name)

with open(tmp_path, "w", encoding="utf-8") as f:
    f.write(code)

shutil.move(tmp_path, file_path)

print(f"✅ Inserted bucket name: {bucket_name} into {file_path}")
