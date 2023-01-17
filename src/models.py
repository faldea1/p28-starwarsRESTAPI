from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    user_name = db.Column(db.String(60), unique=True, nullable=False)
    fav_characters = db.relationship('FavCharacter', lazy=True) ##lazy -> emite un select al cargar. Obtener detalle al seleccionar un character.
    fav_planets = db.relationship('FavPlanet', lazy=True) ##lazy -> emite un select al cargar. Obtener detalle al seleccionar un planet.

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "user_name": self.user_name,
            # do not serialize the password, its a security breach
        }

    def favs(self):
        return {
            "email": self.email,
            "characters": self.fav_characters,
            "planets": self.fav_planets
        }


class Character (db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True, nullable=False)
    gender = db.Column(db.String(70), unique=False, nullable=False)
    birth_year = db.Column(db.String(70), unique=False, nullable=False)
    height = db.Column(db.Integer, unique=False, nullable=False)
    mass = db.Column(db.Integer, unique=False, nullable=False)
    skin_color = db.Column(db.String(70), unique=False, nullable=False)
    hair_color = db.Column(db.String(70), unique=False, nullable=False)
    eye_color = db.Column(db.String(70), unique=False, nullable=False)

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "birth_year": self.birth_year,
            "height": self.height,
            "mass": self.mass,
            "skin_color": self.skin_color,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color
        }


class Planet (db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True, nullable=False)
    population = db.Column(db.Integer, unique=False, nullable=False)
    climate = db.Column(db.String(100), unique=False, nullable=False)
    terrain = db.Column(db.String(100), unique=False, nullable=False)
    surface_water = db.Column(db.Integer, unique=False, nullable=False)
    diameter = db.Column(db.Integer, unique=False, nullable=False) 
    gravity = db.Column(db.String(100), unique=False, nullable=False)
    orbital_period = db.Column(db.Integer, unique=False, nullable=False) 
    rotation_period = db.Column(db.Integer, unique=False, nullable=False) 

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "orbital_period": self.orbital_period,
            "rotation_period": self.rotation_period
        }


class FavCharacter (db.Model):
    __tablename__ = 'favcharacters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True, nullable=False)
    type_fav = db.Column(db.String(70), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))

    def __repr__(self):
        return '<FavCharacter %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "user_id": self.user_id,
            "character_id": self.character_id
        }


class FavPlanet (db.Model):
    __tablename__ = 'favplanets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True, nullable=False)
    type_fav = db.Column(db.String(70), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))

    def __repr__(self):
        return '<FavPlanet %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "user_id": self.user_id,
            "planet_id": self.planet_id
        }