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
from models import db, User, Favourites, Planets, Vehicles, Characters
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

@app.route('/users', methods=['GET'])
def get_users_list():
    users = User.query.all()
    response_body = [user.serialize() for user in users]
    return jsonify(response_body), 200

@app.route('/users/favourites', methods=['GET'])
def get_favourites():
    favourites = Favourites.query.all()
    response_body = [favourite.serialize() for favourite in favourites]
    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def get_characters():
    characters_list = Characters.query.all()
    response_body = [character.serialize() for character in characters_list]
    return jsonify(response_body), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_single_character(character_id):
    character = Characters.query.filter_by(id=character_id)
    return jsonify(character.serialize()), 200

@app.route('/planets', methods=['GET'])
def get_planets_list():
    planets_list = Planets.query.all()
    response_body = [planet.serialize() for planet in planets_list]
    return jsonify(response_body), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    planet = Planets.query.filter_by(id=planet_id)
    return jsonify(planet.serialize()), 200
    
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def post_favourite_planet(planet_id):  
    user_id = request.json.get('user_id') 
    new_favourite_planet = Favourites(  
        type='planets',   
        planet_id=planet_id,
        user_id=user_id
    )   
    db.session.add(new_favourite_planet)  
    db.session.commit() 
    return jsonify({"msg": "Favorite planet added successfully!", "favorite": new_favourite_planet.serialize()}), 201 

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def post_favourite_character(character_id):
    user_id = request.json.get('user_id')
    new_favourite_character = Favourites(
        type='characters',
        character_id=character_id,
        user_id=user_id
    )
    db.session.add(new_favourite_character)
    db.session.commit()
    return jsonify({"msg": "Favourite character added succesfully!", "favourite": new_favourite_character.serialize()}), 201

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favourite_planet(planet_id):
    user_id=request.json.get('user_id')
    delete_favourite= Favourites.query.filter_by(type='planets', planet_id=planet_id, user_id=user_id).first()
    if delete_favourite:
        db.session.delete(delete_favourite)
        db.session.commit()
        return jsonify({"msg": "Favourite planet removed succesfully!"}), 200
    return jsonify({"msg": "Favourite planet not found!"}), 404

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favourite_haracter(character_id):
    user_id=request.json.get('user_id')
    delete_favourite= Favourites.query.filter_by(type='characters', character_id=character_id, user_id=user_id).first()
    if delete_favourite:
        db.session.delete(delete_favourite)
        db.session.commit()
        return jsonify({"msg": "Favourite character removed succesfully!"}), 200
    return jsonify({"msg": "Favourite character not found!"}), 404


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)


  

