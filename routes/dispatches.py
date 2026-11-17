# routes/dispatches.py
# Sends an SMS alert to a ranger for one report, and logs it.
from flask import Blueprint, request, jsonify, current_app
from database import get_db
from services.alert_service import build_alert
from services.sms_service import send_sms
from services.ranger_auth import ranger_required

bp = Blueprint("dispatches", __name__, url_prefix="/api/dispatch")


@bp.post("/<int:incident_id>")
@ranger_required
def dispatch(incident_id):
    """POST /api/dispatch/1 with {"language": "sw"} -> send the alert."""
    # Language is optional. silent=True means "no body" gives None instead of an error.
    body = request.get_json(silent=True) or {}
    language = body.get("language", "en")

    db = get_db()

    # 1. Find the report, together with its forest's name.
    incident = db.execute(
        "SELECT incidents.*, forests.name AS forest"
        " FROM incidents"
        " JOIN forests ON forests.id = incidents.forest_id"
        " WHERE incidents.id = ?",
        (incident_id,),
    ).fetchone()

    if incident is None:
        return jsonify(error="incident not found"), 404

    # 2. Write the message, then send it to the ranger's phone.
    message = build_alert(incident, incident["forest"], language)
    delivery = send_sms(current_app.config["RANGER_PHONE"], message)

    # 3. Keep a record of what was sent, and mark the report as dispatched.
    db.execute(
        "INSERT INTO dispatches (incident_id, language, message, delivery)"
        " VALUES (?, ?, ?, ?)",
        (incident_id, language, message, delivery),
    )
    db.execute("UPDATE incidents SET status = 'dispatched' WHERE id = ?", (incident_id,))
    db.commit()

    return jsonify(message=message, delivery=delivery)
