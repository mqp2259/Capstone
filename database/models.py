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
    is_sqlite = database_path.startswith('sqlite:')
    migrate = Migrate(app, db, render_as_batch=is_sqlite)

'''
Movie
a persistent movie entity, extends the base SQLAlchemy Model
'''
class Movie(db.Model):
    __tablename__ = 'movies'
    # Autoincrementing, unique primary key
    id = db.Column(db.Integer(), primary_key=True)
    # Movie title
    title = db.Column(db.String(80), nullable=False)
    # Release date
    release_date = db.Column(db.DateTime())

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {"id": self.id,
                "title": self.title,
                "release_date": self.release_date.strftime("%Y-%m-%d")}

    def __repr__(self):
        return 'Movie: title=%s, release date=%s' % (self.title, self.release_date)

'''
Movie
a persistent actor entity, extends the base SQLAlchemy Model
'''
class Actor(db.Model):
    __tablename__ = 'actors'
    # Autoincrementing, unique primary key
    id = db.Column(db.Integer(), primary_key=True)
    # Name
    name = db.Column(db.String(80), nullable=False)
    # Age
    age = db.Column(db.Integer())
    # Gender
    gender = db.Column(db.String(80))

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {"id": self.id,
                "name": self.name,
                "age": self.age,
                "gender": self.gender}

    def __repr__(self):
        return 'Actor: name=%s, age=%d, gender=%s' % (self.name, self.age, self.gender)