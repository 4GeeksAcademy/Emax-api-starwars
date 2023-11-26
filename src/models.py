from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites = db.relationship("Favorites", backref = "user")

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    eye_color = db.Column(db.String(80), unique=False, nullable=False)
    hair_color = db.Column(db.String(100), unique=False, nullable=False)
    favorites = db.relationship("Favorites", backref = "character")

    def __repr__(self):
        return '<Character %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "eye_color": self.eye_color,
            "hair_color": self.hair_color,
        }
    
class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    gravity = db.Column(db.String(80), unique=False, nullable=False)
    climate = db.Column(db.String(100), unique=False, nullable=False)
    poblation = db.Column(db.String(100), unique=False, nullable=False)
    rotation_period = db.Column(db.String(100), unique=False, nullable=False)
    favorites = db.relationship("Favorites", backref = "planets")

    def __repr__(self):
        return '<Planets %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gravity": self.gravity,
            "climate": self.climate,
            "poblation": self.poblation,
        }
    
class Films(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    created = db.Column(db.String(80), unique=False, nullable=False)
    edited = db.Column(db.String(100), unique=False, nullable=False)
    producer = db.Column(db.String(100), unique=False, nullable=False)
    title = db.Column(db.String(100), unique=False, nullable=False)
    director= db.Column(db.String(100), unique=False, nullable=False)
    favorites = db.relationship("Favorites", backref = "films")

    def __repr__(self):
        return '<Films %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "created": self.created,
            "edited": self.edited,
            "producer": self.producer,
            "title": self.title,
            "director": self.director,
        }
    
class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    planets_id = db.Column(db.Integer, db.ForeignKey("planets.id"), nullable=True)
    character_id = db.Column(db.Integer, db.ForeignKey("character.id"), nullable=True)
    films_id = db.Column(db.Integer, db.ForeignKey("films.id"), nullable=True)

    def __repr__(self):
        return '<Favorites %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planets_id": self.planets_id,
            "films_id": self.films_id,
        }