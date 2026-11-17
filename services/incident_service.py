# services/incident_service.py
# Takes a raw report, cross-checks it, scores it, and saves it.
from .spatial_service import nearest_forest, haversine_km
from .satellite_service import canopy_loss_pct
from .risk_service import risk_score


def create_incident(db, channel, phone, activity, description, lat, lon):
    """Process and save one report.

    Returns (incident_id, forest_name, canopy_loss_pct, risk_score, risk_level).
    """
    # 1. Which forest is this report about, and how far from its edge?
    forest, edge_km = nearest_forest(db, lat, lon)

    # 2. What does the satellite say about that forest?
    loss = canopy_loss_pct(forest)

    # 3. How many reports in the last 7 days were within 2 km of this one?
    recent = db.execute(
        "SELECT lat, lon FROM incidents WHERE created_at >= datetime('now', '-7 days')"
    )
    similar = sum(
        1 for row in recent
        if haversine_km(lat, lon, row["lat"], row["lon"]) <= 2
    )

    # 4. Combine the evidence into a score and a label.
    score, level, _factors = risk_score(loss, activity, edge_km, similar)

    # 5. Save the report with its results.
    cursor = db.execute(
        "INSERT INTO incidents (channel, phone, activity, description, lat, lon,"
        " forest_id, canopy_loss_pct, risk_score, risk_level)"
        " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (channel, phone, activity, description, lat, lon,
         forest["id"], loss, score, level),
    )
    db.commit()

    return cursor.lastrowid, forest["name"], loss, score, level
