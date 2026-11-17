# services/satellite_service.py
# Turns satellite band values into a canopy-loss percentage.


def ndvi(nir, red):
    """Normalized Difference Vegetation Index.

    NIR = near-infrared reflectance, Red = red reflectance.
    Healthy leaves reflect lots of NIR and absorb red, so a higher
    result (closer to 1) means greener, denser vegetation.
    """
    total = nir + red
    if total == 0:          # avoid dividing by zero
        return 0.0
    return (nir - red) / total


def canopy_loss_pct(forest):
    """Percentage drop in NDVI between the earlier and the latest scan."""
    before = ndvi(forest["nir_before"], forest["red_before"])
    now = ndvi(forest["nir_now"], forest["red_now"])

    if before <= 0:         # no vegetation to lose
        return 0.0

    loss = (before - now) / before * 100
    return round(max(0.0, loss), 1)   # never negative; 1 decimal place


# Upgrade path: replace the stored bands with live Sentinel-2 data from
# Google Earth Engine (B8 = NIR, B4 = Red). These two functions stay the same.
