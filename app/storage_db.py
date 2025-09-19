# app/storage_db.py
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# database lives in instance/app.db; instance folder is outside version control
DB_PATH = Path(__file__).resolve().parents[1] / "instance" / "app.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(f"sqlite:///{DB_PATH}")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True)
    review_id = Column(String(48), unique=True, nullable=False)
    created_at = Column(String(20), nullable=False)   # ISO UTC string
    username = Column(String(64), nullable=False)
    cafe_name = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    rating = Column(Integer, nullable=False)
    date_visited = Column(String(10), nullable=False)  # YYYY-MM-DD

def create_all():
    Base.metadata.create_all(engine)

def now_utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def generate_review_id() -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    short = uuid4().hex[:6]
    return f"r-{ts}-{short}"

def save_review(record: dict):
    create_all()
    with SessionLocal() as s:
        row = Review(**record)
        s.add(row)
        s.commit()
        return row.review_id

def list_summaries(username_filter: str | None = None):
    create_all()
    with SessionLocal() as s:
        q = s.query(Review).order_by(Review.created_at.desc())
        if username_filter:
            q = q.filter(Review.username == username_filter)
        rows = q.all()
        return [(r.created_at, r.username, r.cafe_name, r.rating) for r in rows]
