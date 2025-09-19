# app/web.py
from flask import Flask, render_template, request, redirect, url_for, flash
from app import models
from app import storage_db as storage  # swap to file storage if you prefer

def create_app():
    app = Flask(__name__)
    app.secret_key = "dev-key"   # needed for flash messages

    @app.get("/reviews")
    def reviews_list():
        user = request.args.get("user")  # optional filter
        rows = storage.list_summaries(user)
        return render_template("reviews_list.html", rows=rows, user=user)

    @app.get("/reviews/new")
    def new_review_form():
        return render_template("new_review.html")

    @app.post("/reviews/new")
    def new_review_submit():
        try:
            username = models.validate_username(request.form.get("username", ""))
            cafe_name = models.validate_cafe_name(request.form.get("cafe_name", ""))
            description = models.validate_description(request.form.get("description", ""))
            rating = models.parse_rating(request.form.get("rating", ""))
            date_visited = models.parse_date_visited(request.form.get("date_visited", ""))
        except ValueError as e:
            flash(str(e))
            return redirect(url_for("new_review_form"))

        record = {
            "review_id": storage.generate_review_id(),
            "created_at": storage.now_utc_iso(),
            "username": username,
            "cafe_name": cafe_name,
            "description": description,
            "rating": rating,
            "date_visited": date_visited,
        }
        storage.save_review(record)
        flash("Saved your review")
        return redirect(url_for("reviews_list"))

    return app

# allow flask run to find the app object
app = create_app()
