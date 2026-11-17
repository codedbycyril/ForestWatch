# routes/pages.py
# Connects page URLs to HTML templates in the templates/ folder.
import secrets
from hmac import compare_digest

from flask import (
    Blueprint,
    abort,
    current_app,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash

from services.ranger_auth import ranger_required

bp = Blueprint("pages", __name__)


@bp.context_processor
def security_context():
    token = session.get("_csrf_token")
    if token is None:
        token = secrets.token_urlsafe(32)
        session["_csrf_token"] = token
    return {"csrf_token": token}


@bp.get("/lab")
def lab():
    return render_template("lab.html")


@bp.get("/")
def overview():
    return render_template("overview.html")


@bp.get("/report")
def report():
    return render_template("report.html")


@bp.get("/dashboard")
@ranger_required
def dashboard():
    return render_template("dashboard.html")


@bp.route("/ranger/login", methods=["GET", "POST"])
def ranger_login():
    if session.get("ranger_authenticated") is True:
        return redirect(url_for("pages.dashboard"))

    password_hash = current_app.config["RANGER_PASSWORD_HASH"]
    error = None

    if request.method == "POST":
        submitted_token = request.form.get("csrf_token", "")
        expected_token = session.get("_csrf_token", "")
        if not expected_token or not compare_digest(submitted_token, expected_token):
            abort(400)

        if not password_hash:
            return render_template(
                "ranger_login.html",
                configured=False,
                error=None,
            ), 503

        password = request.form.get("password", "")
        if check_password_hash(password_hash, password):
            session.clear()
            session.permanent = True
            session["ranger_authenticated"] = True
            return redirect(url_for("pages.dashboard"))

        error = "That password didn't match. Please try again."

    return render_template(
        "ranger_login.html",
        configured=bool(password_hash),
        error=error,
    ), 401 if error else 200


@bp.post("/ranger/logout")
@ranger_required
def ranger_logout():
    submitted_token = request.form.get("csrf_token", "")
    expected_token = session.get("_csrf_token", "")
    if not expected_token or not compare_digest(submitted_token, expected_token):
        abort(400)
    session.clear()
    return redirect(url_for("pages.ranger_login"))


@bp.get("/architecture")
def architecture():
    return render_template("architecture.html")
