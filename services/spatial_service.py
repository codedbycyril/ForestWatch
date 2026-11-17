# services/spatial_service.py
# Distance calculations between points on the Earth.
from math import radians, sin, cos, asin, sqrt


def haversine_km(lat1, lon1, lat2, lon2):
    """Distance in km between two lat/lon points (the haversine formula)."""
    # Convert degrees to radians, which the trig functions need.
    lat1, lon1, lat2, lon2 = map(radians, (lat1, lon1, lat2, lon2))

    a = sin((lat2 - lat1) / 2) ** 2 + cos(lat1) * cos(lat2) * sin((lon2 - lon1) / 2) ** 2
    return 6371 * 2 * asin(sqrt(a))   # 6371 km = Earth's radius


def nearest_forest(db, lat, lon):
    """Find the closest forest to a point.

    Returns (forest_row, edge_distance_km).
    A negative distance means the point is INSIDE the forest.
    """
    best, best_d = None, None
    for forest in db.execute("SELECT * FROM forests"):
        # Distance to the forest centre, minus its radius = distance to its edge.
        d = haversine_km(lat, lon, forest["lat"], forest["lon"]) - forest["radius_km"]
        if best is None or d < best_d:
            best, best_d = forest, d
    return best, best_d
