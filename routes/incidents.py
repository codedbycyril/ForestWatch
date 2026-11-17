# routes/incidents.py
# Endpoints for submitting and listing citizen reports.
from flask import Blueprint, request, jsonify
from database import get_db
from services.incident_service import create_incident
from services.ranger_auth import ranger_required

bp = Blueprint("incidents", __name__, url_prefix="/api")

# The only activity types we accept.
ACTIVITIES = {"logging", "charcoal", "fire", "clearing", "other"}


@bp.post("/incidents")
def submit():
    """POST /api/incidents -> validate, score and save a new report."""
    data = request.get_json(force=True)   # read the JSON sent by the browser

    # 1. Latitude and longitude must exist and be numbers.
    try:
        lat = float(data["lat"])
        lon = float(data["lon"])
    except (KeyError, ValueError, TypeError):
        return jsonify(error="lat and lon are required numbers"), 400

    # 2. The point must be inside Kenya (roughly).
    if not (-5 <= lat <= 5 and 33 <= lon <= 42):
        return jsonify(error="coordinates must be inside Kenya"), 400

    # 3. The activity must be one we know.
    activity = data.get("activity", "other")
    if activity not in ACTIVITIES:
        return jsonify(error=f"activity must be one of {sorted(ACTIVITIES)}"), 400

    # 4. All good: run the pipeline from incident_service.py.
    incident_id, forest, loss, score, level = create_incident(
        get_db(), "web", data.get("phone"), activity,
        data.get("description", ""), lat, lon,
    )

    # 201 = "Created". Send back the result so the page can show it.
    return jsonify(
        id=incident_id, forest=forest, canopy_loss_pct=loss,
        risk_score=score, risk_level=level,
    ), 201


@bp.get("/incidents")
@ranger_required
def list_all():
    """GET /api/incidents -> every report, newest first."""
    rows = get_db().execute(
        "SELECT * FROM incidents ORDER BY created_at DESC"
    ).fetchall()
    return jsonify([dict(row) for row in rows])


@bp.get("/map/incidents")
def map_markers():
    """Return coarse, non-identifying markers for the public overview map."""
    rows = get_db().execute(
        "SELECT lat, lon, risk_level FROM incidents WHERE status != 'dismissed'"
    ).fetchall()
    return jsonify([
        {
            "lat": round(row["lat"], 2),
            "lon": round(row["lon"], 2),
            "risk_level": row["risk_level"],
        }
        for row in rows
    ])
