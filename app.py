import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from database.models import *


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
    def get_actors_by_id(id):
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
    def get_movies_by_id(id):
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
    def delete_actors_by_id(id):
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
    DELETE the actor by id.
    '''
    @app.route('/movies/<int:id>', methods=['DELETE'])
    def delete_movies_by_id(id):
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
    DELETE the actor by id.
    '''
    @app.route('/actors/<int:id>', methods=['DELETE'])
    def delete_actors_by_id(id):
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
    DELETE the actor by id.
    '''
    @app.route('/movies/<int:id>', methods=['DELETE'])
    def delete_movies_by_id(id):
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

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='127.0.0.1', port=8080, debug=True)
