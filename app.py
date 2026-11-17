# app.py
# Creates and starts the ForestWatch Flask app.
from flask import Flask
from config import Config
import database


def create_app():
    """App factory: builds and returns a configured Flask app."""
    app = Flask(__name__)
    app.config.from_object(Config)   # load settings from config.py
    database.init_app(app)           # open/close DB, build tables, seed data

    # Each routes/ file is a Blueprint (a group of related URLs).
    # Importing them here avoids circular imports.
    from routes import pages, incidents, triage, dispatches, sms_webhook, telemetry
    for module in (pages, incidents, triage, dispatches, sms_webhook, telemetry):
        app.register_blueprint(module.bp)

    return app


if __name__ == "__main__":
    # Runs only when you type `python app.py`, not when imported.
    create_app().run(debug=True)
