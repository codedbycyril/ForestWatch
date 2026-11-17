# routes/triage.py
# The ranger work queue: list reports by risk, and update their status.
from flask import Blueprint, request, jsonify
from database import get_db
from services.ranger_auth import ranger_required

bp = Blueprint("triage", __name__, url_prefix="/api/triage")

# The only statuses a report can have.
STATUSES = {"new", "verified", "dispatched", "dismissed"}


@bp.get("/queue")
@ranger_required
def queue():
    """GET /api/triage/queue -> active reports, highest risk first."""
    rows = get_db().execute(
        "SELECT incidents.*, forests.name AS forest"
        " FROM incidents"
        " JOIN forests ON forests.id = incidents.forest_id"
        " WHERE incidents.status != 'dismissed'"
        " ORDER BY incidents.risk_score DESC"
    ).fetchall()
    return jsonify([dict(row) for row in rows])


@bp.patch("/<int:incident_id>")
@ranger_required
def update(incident_id):
    """PATCH /api/triage/5 with {"status": "verified"} -> change its status."""
    status = request.get_json(force=True).get("status")

    if status not in STATUSES:
        return jsonify(error="invalid status"), 400

    db = get_db()
    db.execute("UPDATE incidents SET status = ? WHERE id = ?", (status, incident_id))
    db.commit()
    return jsonify(id=incident_id, status=status)
