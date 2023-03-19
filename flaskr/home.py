from flask import (
    Blueprint,
    render_template,
    session,
)

from flaskr.db import get_db


bp = Blueprint("home", __name__)


@bp.route("/", methods=("GET", "POST"))
@bp.route("/home", methods=("GET", "POST"))
def home():
    return render_template(
        "home.html", user=session.get("user"), is_admin=session.get("is_admin")
    )
