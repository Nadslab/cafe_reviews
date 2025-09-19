# cli.py
from app import models
from app import storage_db as storage
import sys

def prompt_line(label: str) -> str:
    while True:
        value = input(label).strip()
        if value:
            return value
        print("Please enter a value.")

def prompt_validated(label: str, validator):
    """Ask repeatedly until validator accepts the input and returns the cleaned value."""
    while True:
        raw = input(label)
        try:
            return validator(raw)
        except ValueError as e:
            print(f"{e}")

def confirm(prompt: str = "Save this review? [y/n]: ") -> bool:
    while True:
        ans = input(prompt).strip().lower()
        if ans in ("y", "yes"):
            return True
        if ans in ("n", "no"):
            return False
        print("Please type y or n.")

def add_review_flow() -> None:
    print("Welcome to the cafe review app.")

    # gather and validate each field with re-prompts
    username = prompt_validated("Username: ", models.validate_username)
    cafe_name = prompt_validated("Cafe name: ", models.validate_cafe_name)
    description = prompt_validated("Description: ", models.validate_description)
    rating = prompt_validated("Rating 1-5: ", models.parse_rating)
    date_visited = prompt_validated("Date visited YYYY-MM-DD: ", models.parse_date_visited)

    # show summary and ask for confirmation
    print("\nSummary")
    print(f"  Username:     {username}")
    print(f"  Cafe name:    {cafe_name}")
    print(f"  Description:  {description}")
    print(f"  Rating:       {rating}/5")
    print(f"  Date visited: {date_visited}\n")

    if not confirm():
        print("Canceled. Nothing saved.")
        return

    # build the record with program-supplied fields
    created_at = storage.now_utc_iso()
    review_id = storage.generate_review_id()
    record = {
        "review_id": review_id,
        "created_at": created_at,
        "username": username,
        "cafe_name": cafe_name,
        "description": description,
        "rating": rating,
        "date_visited": date_visited,
    }

    # save to disk
    path = storage.save_review(record)
    print(f"Saved review to: {path}")

def list_reviews_flow(username_filter: str | None = None) -> None:
    rows = storage.list_summaries()
    if username_filter:
        uf = username_filter.lower()
        rows = [r for r in rows if r[1].lower() == uf]  # r = (created_at, username, cafe, rating)

    if not rows:
        if username_filter:
            print(f"No reviews found for {username_filter}.")
        else:
            print("No reviews found.")
        return

    for created_at, username, cafe, rating in rows:
        print(f"{created_at} | {username} | {cafe} | {rating}/5")

def main() -> None:
    # usage:
    #   python cli.py               add a review
    #   python cli.py list          list all reviews
    #   python cli.py list <user>   list reviews for one user
    if len(sys.argv) > 1 and sys.argv[1].lower() == "list":
        username_filter = sys.argv[2] if len(sys.argv) > 2 else None
        list_reviews_flow(username_filter)
    else:
        add_review_flow()

if __name__ == "__main__":
    main()
