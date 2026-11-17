# database.py
# Helpers for opening, closing and setting up the SQLite database.
import sqlite3
from pathlib import Path
from flask import g, current_app


def get_db():
    """Return this request's database connection, opening it if needed."""
    # `g` is a Flask object that lives for one request. We store the
    # connection on it so the same request reuses one connection.
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        # Lets us read columns by name: row["lat"] instead of row[3].
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    """Close the connection at the end of the request."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Create the tables from schema.sql, then add demo data."""
    db = get_db()
    schema_path = Path(__file__).with_name("schema.sql")
    db.executescript(schema_path.read_text())

    # Imported here (not at the top) so this file works before seed.py exists.
    from seed import seed_if_empty
    seed_if_empty(db)


def init_app(app):
    """Connect the database helpers to the Flask app."""
    app.teardown_appcontext(close_db)   # run close_db after every request
    with app.app_context():             # init_db needs an app context
        init_db()
