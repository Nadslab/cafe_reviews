from pathlib import Path
import json

from app import storage_db as storage

SRC = Path(__file__).resolve().parents[1] / "data" / "reviews"

def main():
    for p in sorted(SRC.glob("*.json")):
        with p.open(encoding="utf-8") as f:
            rec = json.load(f)
        # trust the existing fields; DB module will insert them as rows
        storage.save_review(rec)
        print(f"migrated {p.name}")

if __name__ == "__main__":
    main()
