-- schema.sql
-- Defines the three tables used by ForestWatch.

CREATE TABLE IF NOT EXISTS forests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    lat REAL NOT NULL,              -- centre of the forest (latitude)
    lon REAL NOT NULL,              -- centre of the forest (longitude)
    radius_km REAL NOT NULL,        -- rough size of the forest
    nir_before REAL,                -- near-infrared band, earlier satellite scan
    red_before REAL,                -- red band, earlier scan
    nir_now REAL,                   -- near-infrared band, latest scan
    red_now REAL                    -- red band, latest scan
);

CREATE TABLE IF NOT EXISTS incidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    channel TEXT NOT NULL,          -- 'web' or 'sms'
    phone TEXT,                     -- reporter's phone (optional)
    activity TEXT NOT NULL,         -- logging, charcoal, fire, clearing, other
    description TEXT,
    lat REAL NOT NULL,
    lon REAL NOT NULL,
    forest_id INTEGER REFERENCES forests(id),
    canopy_loss_pct REAL,           -- satellite loss for that forest
    risk_score REAL,                -- AI score 0-100
    risk_level TEXT,                -- LOW, MED, HIGH, CRIT
    status TEXT DEFAULT 'new',      -- new, verified, dispatched, dismissed
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dispatches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    incident_id INTEGER NOT NULL REFERENCES incidents(id),
    language TEXT NOT NULL,         -- 'en' or 'sw'
    message TEXT NOT NULL,          -- the SMS text that was sent
    delivery TEXT,                  -- simulated, sent, or failed
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
