"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
import json
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, FavCharacter, FavPlanet
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


# [GET] /people
@app.route('/people', methods=['GET'])
def handle_people():
    people_query = Character.query.all()
    people_list = list(map(lambda x: x.serialize(), people_query))

    response_body = {
        "msg": "Hello, this is your #[GET] /people response ",
        "characters": people_list
    }

    return jsonify(response_body), 200


# [GET] /people/<int:people_id>
@app.route('/people/<int:id>', methods=['GET'])
def get_character():
    character = Character.query.get(id).serialize()
    print(character)

    response_body = {
        "msg": "Hello, this is your #[GET] /people/<int:people_id> response ",
        "character": character
    }

    return jsonify(response_body), 200


# [GET] /planets
@app.route('/planets/', methods=['GET'])
def get_planets():
    planets_query = Planet.query.all()
    planets_query = list(map(lambda x: x.serialize(), planets_query))
    print(planets_query)

    response_body = {
        "msg": "Hello, this is your #[GET] /planets response ",
        "planets": planets_query
    }

    return jsonify(response_body), 200


# [GET] /planets/<int:planet_id>
@app.route('/planets/<int:id>', methods=['GET'])
def get_planet():
    planet = Planet.query.get(id)
    if planet is None:
        return "No planet found", 404
    planet = planet.serialize()
    print(planet)

    response_body = {
        "msg": "Hello, this is your #[GET] /planets/<int:planet_id> response ",
        "planet": planet
    }

    return jsonify(response_body), 200


#[GET] /users
@app.route('/users/', methods=['GET'])
def get_users():
    users_query = User.query.all()
    users_query = list(map(lambda x: x.serialize(), users_query))
    print(users_query)

    response_body = {
        "msg": "Hello, this is your #[GET] /users response ",
        "users": users_query
    }

    return jsonify(response_body), 200


#[GET] /users/favorites 
@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_favs_each_user(user_id):
    user_query = User.query.get(user_id)

    user_characters = user_query.favorites()['characters']
    user_planets = user_query.favorites()['planets']

    user_characters = list(map(lambda x: x.serialize(), user_characters))
    user_planets = list(map(lambda x: x.serialize(), user_planets))

    if user_query is None:
        return 'No favs found, pick some!', 404

    response_body = {
        "msg": "Hello, this is your #[GET] /users/favorites ",
        "fav_characters": user_characters,
        "fav_planets": user_planets
    }

    return jsonify(response_body), 200


#[POST] /users/favorites 
@app.route('/users/<int:user_id>/favorites', methods=['POST'])
def post_fav(user_id):
    body = request.get_json()
    if body["type"].lower() == "character":
        fav = FavCharacter(type_fav=body["type"], user_id=body['user_id'], character_id=body['character_id'], name= body['name'])
        db.session.add(fav)
        db.session.commit()

        response_body = {
            "state": "character + 1"
    }
    elif body["type"].lower() == "planet":
        fav = FavPlanet(type_fav=body["type"], user_id=body['user_id'], planet_id=body['planet_id'], name= body['name'])
        db.session.add(fav)
        db.session.commit()

        response_body = {
            "state": "planet + 1"
    }

    return jsonify('registering favs'), 200


#[DELETE] /users/favorites 
@app.route('/users/<int:user_id>/favorites', methods=['DELETE'])
def delete_fav(user_id):
    user_query = User.query.get(user_id)
    character_id = request.json.get('character_id')
    planet_id = request.json.get('planet_id')

    if not character_id and not planet_id:
        return "nothing to delete"

    if character_id:
        char = FavCharacter.query.filter_by(userID=user_id, characterID=character_id).first()
        db.session.delete(char)
        db.session.commit()

        print(char)

        return 'char deleted', 200

    if planet_id:
        pla = FavPlanet.query.filter_by(userID=user_id, planetID=planet_id).first()
        db.session.delete(pla)
        db.session.commit()

        print(pla)

        return "pla deleted", 200

    return jsonify ('favs deleted'), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
