# services/alert_service.py
# Builds the SMS text sent to rangers (English or Kiswahili).

# Message templates. The {names} in braces are filled in later.
TEMPLATES = {
    "en": "FORESTWATCH {level}: {activity} reported in {forest} at {lat},{lon}. "
          "Satellite canopy loss {loss}%. Risk {score}/100. Please respond.",
    "sw": "FORESTWATCH {level}: {activity} imeripotiwa {forest} katika {lat},{lon}. "
          "Upotevu wa miti (setilaiti) {loss}%. Hatari {score}/100. Tafadhali jibu.",
}

# Kiswahili names for each activity type.
ACTIVITY_SW = {
    "logging": "ukataji miti",
    "charcoal": "uchomaji makaa",
    "fire": "moto",
    "clearing": "usafishaji wa ardhi",
    "other": "shughuli",
}


def build_alert(incident, forest_name, language="en"):
    """Return the SMS text for one incident.

    incident: a database row (or dict) with activity, risk_level, lat, lon,
              canopy_loss_pct and risk_score.
    language: "en" or "sw".
    """
    activity = incident["activity"]
    if language == "sw":
        activity = ACTIVITY_SW.get(activity, activity)

    # Pick the template (default to English) and fill in the blanks.
    template = TEMPLATES.get(language, TEMPLATES["en"])
    return template.format(
        level=incident["risk_level"],
        activity=activity,
        forest=forest_name,
        lat=round(incident["lat"], 3),
        lon=round(incident["lon"], 3),
        loss=incident["canopy_loss_pct"],
        score=incident["risk_score"],
    )
