import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from database.models import *
from datetime import datetime
from auth.auth import *


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app, database_path)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    '''
    GET all available actors.
    '''
    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(jwt):
        actors = Actor.query.order_by(Actor.id).all()

        formatted_actors = [actor.format() for actor in actors]

        if len(formatted_actors) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'actors': formatted_actors,
            'total_actors': len(formatted_actors)
        })

    '''
    GET all available movies.
    '''
    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(jwt):

        movies = Movie.query.order_by(Movie.id).all()

        formatted_movies = [movie.format() for movie in movies]

        if len(formatted_movies) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'movies': formatted_movies,
            'total_movies': len(formatted_movies)
        })

    '''
    GET the actor by id.
    '''
    @app.route('/actors/<int:id>')
    @requires_auth('get:actors')
    def get_actor_by_id(jwt, id):
        actor = Actor.query.filter(Actor.id == id).one_or_none()

        if actor is None:
            abort(404)

        formatted_actors = [actor.format()]

        return jsonify({
            'success': True,
            'actors': formatted_actors,
            'total_actors': len(formatted_actors)
        })

    '''
    GET the movie by id.
    '''
    @app.route('/movies/<int:id>')
    @requires_auth('get:movies')
    def get_movie_by_id(jwt, id):
        movie = Movie.query.filter(Movie.id == id).one_or_none()

        if movie is None:
            abort(404)

        formatted_movies = [movie.format()]

        return jsonify({
            'success': True,
            'movies': formatted_movies,
            'total_movies': len(formatted_movies)
        })

    '''
    DELETE the actor by id.
    '''
    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor_by_id(jwt, id):
        actor = Actor.query.filter(Actor.id == id).one_or_none()

        if actor is None:
            abort(404)

        try:
            actor.delete()
        except:
            abort(422)


        return jsonify({
            'success': True,
            'deleted': actor.format(),
        })

    '''
    DELETE the movie by id.
    '''
    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie_by_id(jwt, id):
        movie = Movie.query.filter(Movie.id == id).one_or_none()

        if movie is None:
            abort(404)

        try:
            movie.delete()
        except:
            abort(422)


        return jsonify({
            'success': True,
            'deleted': movie.format(),
        })

    '''
    Add an actor.
    '''
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actor(jwt):
        body = request.get_json()
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)

        if name is None:
            abort(400)

        try:
            new_actor = Actor(name=name, age=age, gender=gender)
            new_actor.insert()
        except:
            abort(422)

        return jsonify({
            'success': True,
            'added': new_actor.format(),
        })

    '''
    Add a movie.
    '''
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movie(jwt):
        body = request.get_json()
        title = body.get('title', None)
        release_date = body.get('release_date', None)

        if title is None:
            abort(400)

        if release_date is not None:
            try:
                release_date_datetime = datetime.strptime(release_date, "%Y-%m-%d")
            except:
                abort(422)

        try:
            new_movie = Movie(title=title, release_date=release_date_datetime)
            new_movie.insert()
        except:
            abort(422)

        return jsonify({
            'success': True,
            'added': new_movie.format(),
        })

    '''
    Update an actor.
    '''
    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(jwt, id):
        actor = Actor.query.filter(Actor.id == id).one_or_none()

        if actor is None:
            abort(404)

        body = request.get_json()
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)

        if name is not None:
            actor.name = name

        if age is not None:
            actor.age = age

        if gender is not None:
            actor.gender = gender

        try:
            actor.update()
        except:
            abort(422)

        return jsonify({
            'success': True,
            'updated': actor.format(),
        })

    '''
    Update a movie.
    '''
    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(jwt, id):
        movie = Movie.query.filter(Movie.id == id).one_or_none()

        if movie is None:
            abort(404)

        body = request.get_json()
        title = body.get('title', None)
        release_date = body.get('release_date', None)

        if title is not None:
            movie.title = title

        if release_date is not None:
            try:
                movie.release_date = datetime.strptime(release_date, "%Y-%m-%d")
            except:
                abort(422)

        try:
            movie.update()
        except:
            abort(422)

        return jsonify({
            'success': True,
            'updated': movie.format(),
        })

    '''
    Error handlers
    '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    return app




if __name__ == '__main__':
    APP = create_app()
    APP.run(host='127.0.0.1', port=5000, debug=True)
