from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint
from app.models import db, Episode, Guest, Appearance


main = Blueprint('main', __name__)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


@main.route('/episodes', methods=['GET'])
def get_episodes():
    episodes = Episode.query.all()
    return jsonify([ep.to_dict() for ep in episodes]), 200

@main.route('/episodes/<int:id>', methods=['GET'])
def get_episode_by_id(id):
    episode = Episode.query.get(id)
    if not episode:
        return jsonify({"error": "Episode not found"}), 404

    ep_dict = episode.to_dict()
    ep_dict["appearances"] = [appearance.to_dict() for appearance in episode.appearances]
    return jsonify(ep_dict), 200

@main.route('/guests', methods=['GET'])
def get_guests():
    guests = Guest.query.all()
    return jsonify([g.to_dict() for g in guests]), 200

@main.route('/appearances', methods=['POST'])
def create_appearance():
    data = request.get_json()

    try:
        rating = int(data['rating'])
        guest_id = int(data['guest_id'])
        episode_id = int(data['episode_id'])

        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")

        guest = Guest.query.get(guest_id)
        episode = Episode.query.get(episode_id)

        if not guest or not episode:
            return jsonify({"error": "Guest or Episode not found"}), 404

        new_appearance = Appearance(
            rating=rating,
            guest_id=guest_id,
            episode_id=episode_id
        )
        db.session.add(new_appearance)
        db.session.commit()

        return jsonify(new_appearance.to_dict()), 201

    except Exception as e:
        return jsonify({"errors": [str(e)]}), 400
