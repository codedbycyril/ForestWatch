# routes/telemetry.py
# Read-only endpoints that feed the overview page (map + stat cards).
from flask import Blueprint, jsonify
from database import get_db
from services.satellite_service import canopy_loss_pct

# A Blueprint groups related URLs. url_prefix is added to every route below.
bp = Blueprint("telemetry", __name__, url_prefix="/api")


@bp.get("/forests")
def forests():
    """GET /api/forests -> list of forests with their canopy loss."""
    result = []
    for forest in get_db().execute("SELECT * FROM forests"):
        data = dict(forest)                        # row -> normal dictionary
        data["canopy_loss_pct"] = canopy_loss_pct(forest)
        result.append(data)
    return jsonify(result)


@bp.get("/telemetry/stats")
def stats():
    """GET /api/telemetry/stats -> headline numbers."""
    db = get_db()

    def count(sql):
        # Run a COUNT query and return the single number it produces.
        return db.execute(sql).fetchone()[0]

    return jsonify(
        total_reports=count("SELECT COUNT(*) FROM incidents"),
        critical=count("SELECT COUNT(*) FROM incidents WHERE risk_level = 'CRIT'"),
        dispatched=count("SELECT COUNT(*) FROM incidents WHERE status = 'dispatched'"),
        forests_monitored=count("SELECT COUNT(*) FROM forests"),
    )