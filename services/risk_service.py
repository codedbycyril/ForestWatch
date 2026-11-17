# services/risk_service.py
# Parametric risk model: a weighted sum of four factors, each scaled 0 to 1.

# How much each factor matters. The weights add up to 1.0 (100%).
WEIGHTS = {
    "loss": 0.40,           # satellite canopy loss
    "activity": 0.25,       # how serious the reported activity is
    "proximity": 0.20,      # how close the report is to the forest
    "corroboration": 0.15,  # other reports nearby in the last 7 days
}

# Seriousness of each activity type (0 to 1).
ACTIVITY = {
    "fire": 1.0,
    "logging": 0.9,
    "clearing": 0.8,
    "charcoal": 0.7,
    "other": 0.4,
}


def level(score):
    """Convert a 0-100 score into a label."""
    if score >= 75:
        return "CRIT"
    if score >= 50:
        return "HIGH"
    if score >= 25:
        return "MED"
    return "LOW"


def risk_score(canopy_loss_pct, activity, edge_distance_km, similar_reports):
    """Return (score, level, factors) for one report."""
    factors = {
        # 25% loss or more counts as the maximum
        "loss": min(canopy_loss_pct / 25, 1.0),
        # unknown activity types fall back to 0.4
        "activity": ACTIVITY.get(activity, 0.4),
        # inside the forest = 1.0, fading to 0 at 10 km outside
        "proximity": 1.0 if edge_distance_km <= 0 else max(0.0, 1 - edge_distance_km / 10),
        # 3 or more other reports nearby counts as the maximum
        "corroboration": min(similar_reports / 3, 1.0),
    }

    # Multiply each factor by its weight, add them up, scale to 0-100.
    score = round(100 * sum(WEIGHTS[name] * value for name, value in factors.items()), 1)
    return score, level(score), factors
