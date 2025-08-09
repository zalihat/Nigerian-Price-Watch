import json
from pathlib import Path
import datetime

# === CONFIG ===
BRONZE_DIR = Path("data/bronze")
METADATA_PATH = Path("data/bronze_metadata.json")

# === GET ALL FILES IN BRONZE DIR ===
metadata = {}

for file in BRONZE_DIR.glob("*.xlsx"):
    mod_time = datetime.datetime.fromtimestamp(file.stat().st_mtime).isoformat()
    metadata[file.name] = mod_time
    print(f"[FOUND] {file.name} → {mod_time}")

# === WRITE TO METADATA STORE ===
with open(METADATA_PATH, 'w', encoding='utf-8') as f:
    json.dump(metadata, f, indent=4)

print(f"✅ Metadata saved to {METADATA_PATH}")
