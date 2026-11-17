# routes/sms_webhook.py
# Receives reports sent by SMS. Africa's Talking forwards each incoming
# text to this URL as form data with the fields `from` and `text`.
from flask import Blueprint, request
from database import get_db
from services.incident_service import create_incident

bp = Blueprint("sms_webhook", __name__, url_prefix="/api/webhooks")

ACTIVITIES = {"logging", "charcoal", "fire", "clearing"}
HELP = "Format: LOG <logging|charcoal|fire|clearing> <lat> <lon>"


@bp.post("/sms")
def inbound():
    """POST /api/webhooks/sms -> parse an SMS like 'LOG logging -0.58 35.55'."""
    sender = request.values.get("from", "")
    parts = request.values.get("text", "").strip().split()

    try:
        # Expect exactly: LOG <activity> <lat> <lon>
        if parts[0].upper() != "LOG":
            raise ValueError("missing LOG keyword")
        activity = parts[1].lower()
        lat, lon = float(parts[2]), float(parts[3])

        if activity not in ACTIVITIES:
            raise ValueError("unknown activity")
        if not (-5 <= lat <= 5 and 33 <= lon <= 42):
            raise ValueError("outside Kenya")
    except (IndexError, ValueError):
        # Anything malformed: reply with the correct format instead of crashing.
        return HELP, 200

    create_incident(get_db(), "sms", sender, activity, "Reported by SMS", lat, lon)
    return "Asante! Your report was received.", 200
