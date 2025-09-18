# app/storage.py
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

# project_root / data / reviews
REVIEWS_DIR = Path(__file__).resolve().parents[1] / "data" / "reviews"

def ensure_reviews_dir() -> None:
    REVIEWS_DIR.mkdir(parents=True, exist_ok=True)

def now_utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def generate_review_id() -> str:
    # time stamp for ordering + short random suffix for uniqueness
    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    short = uuid4().hex[:6]
    return f"r-{ts}-{short}"

def save_review(record: dict) -> Path:
    """Write one review to data/reviews/<review_id>.json and return the path."""
    ensure_reviews_dir()
    review_id = record["review_id"]
    path = REVIEWS_DIR / f"{review_id}.json"
    # avoid rare collision
    while path.exists():
        record["review_id"] = generate_review_id()
        path = REVIEWS_DIR / f"{record['review_id']}.json"

    text = json.dumps(record, indent=2, ensure_ascii=False)
    with path.open("w", encoding="utf-8") as f:
        f.write(text)
        f.write("\n")
    return path

def list_summaries() -> list[tuple[str, str, str, int]]:
    """Return a list of (created_at, username, cafe_name, rating) sorted newest first."""
    ensure_reviews_dir()
    rows: list[tuple[str, str, str, int]] = []
    for p in REVIEWS_DIR.glob("*.json"):
        try:
            with p.open("r", encoding="utf-8") as f:
                data = json.load(f)
            rows.append((data["created_at"], data["username"], data["cafe_name"], int(data["rating"])))
        except Exception:
            # skip unreadable files
            continue
    rows.sort(key=lambda r: r[0], reverse=True)
    return rows
