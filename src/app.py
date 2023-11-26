"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planets, Films, Favorites 
import json
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_all_users():
    users = User.query.all()
    if len(users) < 1:
        return jsonify({"msg": "not found"}), 404
    serialized_users = list(map(lambda x: x.serialize(), users))
    return serialized_users , 200

@app.route('/user/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"msg": f"user with id {user_id} not found"}), 404
    serialized_user = user.serialize()
    return serialized_user, 200

@app.route('/user', methods=['POST'])
def create_one_user():
    body = json.loads(request.data)
    new_user = User(
        name = body["name"],
        email = body["email"],
        password = body["password"],
        is_active = True
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "user created succesfull", "user_added": new_user}), 200

@app.route('/character', methods=['GET'])
def get_all_characters():
    characters = Character.query.all()
    if len(characters) < 1:
        return jsonify({"msg": "not found"}), 404
    serialized_characters = list(map(lambda x: x.serialize(), characters))
    return serialized_characters, 200

@app.route('/character/<int:character_id>', methods=['GET'])
def get_one_user(character_id):
    character = Character.query.get(character_id)
    if character is None:
        return jsonify({"msg": f"user with id {character_id} not found"}), 404
    serialized_character = character.serialize()
    return serialized_character, 200

@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planets.query.all()
    if len(planets) < 1:
        return jsonify({"msg": "not found"}), 404
    serialized_planets = list(map(lambda x: x.serialize(), planets))
    return serialized_planets, 200

@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_one_user(planets_id):
    planet = Planets.query.get(planets_id)
    if planet is None:
        return jsonify({"msg": f"user with id {planets_id} not found"}), 404
    serialized_planets = planet.serialize()
    return serialized_planets, 200

@app.route('/films', methods=['GET'])
def get_all_films():
    films = Films.query.all()
    if len(films) < 1:
        return jsonify({"msg": "not found"}), 404
    serialized_films = list(map(lambda x: x.serialize(), films))
    return serialized_films, 200

@app.route('/films/<int:films_id>', methods=['GET'])
def get_one_user(films_id):
    film = Films.query.get(films_id)
    if film is None:
        return jsonify({"msg": f"user with id {films_id} not found"}), 404
    serialized_films = film.serialize()
    return serialized_films, 200

@app.route('/favorites', methods=['GET'])
def get_all_favorites():
    favorites = Favorites.query.all()
    if len(favorites) < 1:
        return jsonify({"msg": "not found"}), 404
    serialized_favorites = list(map(lambda x: x.serialize(), favorites))
    return serialized_favorites, 200

@app.route('/favorites', methods=['POST'])
def add_favorites():
    body = request.json 
    new_favorite = Favorites(
        user_id = body["user_id"],
        planets_id = body["planets_id"],
        character_id = body["character_id"],
        films_id = body["films_id"] 
    )
    if new_favorite.planets_id is None and new_favorite.character_id is None and new_favorite.films_id is None:
      return jsonify({"msg": "eres boludo"}), 400
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"msg": "sos un capo", "added_favorite": new_favorite})

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
