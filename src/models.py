from flask_sqlalchemy import SQLAlchemy
#import enum


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'    
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False, unique=False)
    first_name = db.Column(db.String(250))
    last_name = db.Column(db.String(250))
    email = db.Column(db.String(250), unique=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    favourites = db.relationship('Favourites', back_populates='user')
    is_active = db.Column(db.Boolean(), default=True, unique=False, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }

class Login(db.Model):
    __tablename__ = 'login'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False, unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Favourites(db.Model):
    __tablename__ = 'favourites'    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum("planets", "vehicles", "characters", name="favourite_type"), nullable=False)    
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)
    
    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "vehicle_id": self.vehicle_id,
            "planet_id": self.planet_id,
            "character_id": self.character_id
        }

class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    orbital_period = db.Column(db.Float)
    population = db.Column(db.Float)
    climate = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)
    favourites = db.relationship('Favourites')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "orbital_period": self.orbital_period,
            "population": self.population,
            "climate": self.climate            
        }

class Vehicles(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    model = db.Column(db.String(50))
    vehicle_class = db.Column(db.String(50))
    manufacturer = db.Column(db.String(50))
    cost_in_credits = db.Column(db.Numeric(6, 2))
    length = db.Column(db.Numeric(5, 1))
    crew = db.Column(db.Float)
    passengers = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)
    favourites = db.relationship('Favourites')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "vehicle_class": self.model,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "crew": self.crew,
            "passengers": self.passengers
        }

class Characters(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    birth_year = db.Column(db.String(50))
    eye_color = db.Column(db.Integer)
    films = db.Column(db.String(50))
    gender = db.Column(db.String(50))
    hair_color = db.Column(db.String(50))
    height = db.Column(db.Float(10))
    homeworld = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)
    favourites = db.relationship('Favourites')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "eye_color": self.eye_color,
            "films": self.films,
            "gender": self.gender,
            "height": self.height,
            "homeworld": self.homeworld
        }


    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }