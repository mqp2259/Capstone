import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from database.models import *
from datetime import datetime


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    '''
    GET all available actors.
    '''
    @app.route('/actors')
    def get_actors():
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
    def get_movies():

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
    def get_actor_by_id(id):
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
    def get_movie_by_id(id):
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
    def delete_actor_by_id(id):
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
    def delete_movie_by_id(id):
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
    def add_actor():
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
    Add an movie.
    '''
    @app.route('/movies', methods=['POST'])
    def add_movies():
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

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='127.0.0.1', port=5000, debug=True)
