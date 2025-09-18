# app/models.py
import re
from datetime import date

_username_ok = re.compile(r"^[A-Za-z0-9_-]+$")

def validate_username(text: str) -> str:
    text = text.strip()
    if not text:
        raise ValueError("Username cannot be empty.")
    if not _username_ok.match(text):
        raise ValueError("Username may contain letters, digits, underscore, or hyphen only.")
    return text

def validate_cafe_name(text: str) -> str:
    text = text.strip()
    if not text:
        raise ValueError("Cafe name cannot be empty.")
    return text

def validate_description(text: str) -> str:
    text = text.strip()
    if not text:
        raise ValueError("Description cannot be empty.")
    return text

def parse_rating(text: str) -> int:
    text = text.strip()
    try:
        value = int(text)
    except ValueError:
        raise ValueError("Rating must be a whole number.")
    if value < 1 or value > 5:
        raise ValueError("Rating must be between 1 and 5.")
    return value

def parse_date_visited(text: str) -> str:
    text = text.strip()
    try:
        d = date.fromisoformat(text)  # expects YYYY-MM-DD and checks that it is a real date
    except Exception:
        raise ValueError("Date must be in YYYY-MM-DD format and be a real calendar date.")
    return d.isoformat()
