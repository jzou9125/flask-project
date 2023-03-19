import functools

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db
from .forms import LoginForm, RegisterForm


bp = Blueprint("auth", __name__)


@bp.route("/login", methods=("GET", "POST"))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = request.form["email"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute("SELECT * FROM user WHERE email = ?", (email,)).fetchone()
        is_admin = False

        if user is None:
            user = db.execute(
                "SELECT * FROM admin WHERE email = ?", (email,)
            ).fetchone()
            if user:
                is_admin = True
            if user is None:
                error = "Incorrect email."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."

        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            session["is_admin"] = is_admin
            return redirect(url_for("home.home"))
        flash(error)
    else:
        for field, errors in form.errors.items():
            for error in errors:
                print(f"{field}: {error}")

    return render_template("auth/login.html", form=form)


@bp.route("/register", methods=("GET", "POST"))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        db = get_db()

        try:
            db.execute(
                "INSERT INTO user (username, email, password) VALUES (?, ?, ?)",
                (username, email, generate_password_hash(password)),
            )
            db.commit()
        except db.IntegrityError:
            flash(f"Either the email or username is used already")
        else:
            return redirect(url_for("auth.login"))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                print(f"{field}: {error}")
    return render_template("auth/register.html", form=form)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
        )


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


def create_admin():
    db = get_db()
    try:
        db.execute(
            "INSERT INTO Admin (username, email, password) VALUES (?, ?, ?)",
            ("admin", "admin@admin", generate_password_hash("admin")),
        )
        db.commit()
    except db.IntegrityError:
        flash(f"Either the email or username is used already")
