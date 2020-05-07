import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json
from flask_migrate import Migrate

database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)

'''
Movie
a persistent movie entity, extends the base SQLAlchemy Model
'''
class Movie(db.Model):
    __tablename__ = 'movies'
    # Autoincrementing, unique primary key
    id = db.Column(db.Integer(), primary_key=True)
    # Movie title
    title = db.Column(db.String(80), unique=True)
    # Release date
    release_time = db.Column(db.DateTime(), nullable=False)

    def __repr__(self):
        return 'Movie: title=%s, y=%s' % (self.title, self.release_time)

'''
Movie
a persistent actor entity, extends the base SQLAlchemy Model
'''
class Actor(db.Model):
    __tablename__ = 'actors'
    # Autoincrementing, unique primary key
    id = db.Column(db.Integer(), primary_key=True)
    # Name
    name = db.Column(db.String(80))
    # Age
    age = db.Column(db.Integer())
    # Gender
    gender = db.Column(db.String(80))

    def __repr__(self):
        return 'Actor: name=%s, age=%d, gender=%s' % (self.title, self.age, self.gender)