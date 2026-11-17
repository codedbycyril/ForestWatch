# seed.py
# Demo data inserted the first time the app runs.

# Each forest: (name, lat, lon, radius_km, nir_before, red_before, nir_now, red_now)
# The four band values are satellite reflectance (0 to 1).
# "before" = earlier scan, "now" = latest scan. We use them to compute NDVI.
FORESTS = [
    ("Mau Forest",     -0.60, 35.60, 25, 0.45, 0.06, 0.38, 0.09),
    ("Karura Forest",  -1.24, 36.83,  2, 0.42, 0.07, 0.41, 0.07),
    ("Arabuko Sokoke", -3.32, 39.95, 12, 0.44, 0.06, 0.34, 0.11),
]

# Each report: (channel, phone, activity, description, lat, lon)
INCIDENTS = [
    ("web", None,            "logging",  "Chainsaw noise and trucks at night", -0.58, 35.55),
    ("sms", "+254711000111", "charcoal", "Kilns spotted near river",           -3.30, 39.97),
    ("web", None,            "fire",     "Smoke on the ridge",                 -0.62, 35.63),
]


def seed_if_empty(db):
    """Insert demo data, but only if the forests table is empty."""
    already_seeded = db.execute("SELECT COUNT(*) FROM forests").fetchone()[0]
    if already_seeded:
        return

    db.executemany(
        "INSERT INTO forests (name, lat, lon, radius_km,"
        " nir_before, red_before, nir_now, red_now)"
        " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        FORESTS,
    )
    db.commit()

    # Imported here because incident_service.py is written in Phase 3.
    from services.incident_service import create_incident

    for channel, phone, activity, description, lat, lon in INCIDENTS:
        create_incident(db, channel, phone, activity, description, lat, lon)
