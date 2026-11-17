from functools import wraps

from flask import jsonify, redirect, request, session, url_for


def ranger_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if session.get("ranger_authenticated") is True:
            return view(*args, **kwargs)

        if request.path.startswith("/api/"):
            return jsonify(error="Ranger sign-in required"), 401
        return redirect(url_for("pages.ranger_login"))

    return wrapped
