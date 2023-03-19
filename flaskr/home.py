from flask import Blueprint, render_template, session

from flaskr.db import get_db

bp = Blueprint("home", __name__)

@bp.route("/", methods=("GET", "POST"))
@bp.route("/home", methods=("GET", "POST"))
def home():
    db = get_db()
    users = None
    if session.get("is_admin"):
        try:
            users = db.execute("Select * from user").fetchall()
            for row in users:
                print(*row)
        except db.IntegrityError:
            pass

    return render_template(
        "home.html",
        user=session.get("user"),
        is_admin=session.get("is_admin"),
        users=users,
    )
