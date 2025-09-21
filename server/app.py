# server/app.py

import os
from flask import Flask, jsonify
from flask_migrate import Migrate
from models import db, Earthquake

# Create migrate instance
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Use DATABASE_URL if provided, otherwise SQLite in instance/
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "sqlite:///app.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # ---------------- ROUTES ---------------- #

    @app.route("/")
    def index():
        return jsonify(message="Earthquake API"), 200

    @app.route("/earthquakes/<int:id>")
    def get_earthquake(id):
        quake = Earthquake.query.filter_by(id=id).first()
        if quake:
            return jsonify(quake.to_dict()), 200
        return jsonify(message=f"Earthquake {id} not found."), 404

    @app.route("/earthquakes/magnitude/<float:magnitude>")
    def quakes_by_magnitude(magnitude):
        quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
        quakes_list = [q.to_dict() for q in quakes]
        return jsonify(count=len(quakes_list), quakes=quakes_list), 200

    return app


# Expose app for flask command
app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("FLASK_RUN_PORT", 5555)))
