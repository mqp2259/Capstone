import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from database.models import *
import shutil

CASTING_ASSISTANT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImNzR2xDMFB3VnIzaGNGV1AyWGE3aCJ9.eyJpc3MiOiJodHRwczovL21xcDIyNTkuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYWY4Mzc1NTRiMTRjMGMxMjczMzhjYyIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNTg4OTIwNjE3LCJleHAiOjE1ODkwMDcwMTcsImF6cCI6IkVnVWJBWWxtYXBiZ0xqZlExZ2hLbkhBYUxiRldwc3JVIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.Ykkjmbcisi9s1NGdkdyfpWK20e-7evkDCpxqSxT-5mL_zAt_W0FMUD8XKd6otnDHUJW73AvRJRLvgx3dNdmfOhi2pwoZPkKLTKsWCg3US6kej5-5xYRjzIkTD75eVB4wD8O9fDiZnNMs6RncCT0Nl86oIjxjv63C3rXT2ag-zuDQpJ-Prl_VKIsKaioWnz_iLXl8_KafyEuc6YW_kJmbx2Ci8v7lsNXIAZUwNk4Q6-8JBUHy-VwA4ta8ellGoKd37-SJ726W5VXT1Gae6Egfclg2wS6jD6F4ig7g63gUadO14wexiICbmDOa1EASxGnHDNPz6XOE1Egdpq5GCq20zw'
CASTING_DIRECTOR_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImNzR2xDMFB3VnIzaGNGV1AyWGE3aCJ9.eyJpc3MiOiJodHRwczovL21xcDIyNTkuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYjFlY2Y0MWNjMWFjMGMxNDg5NjgxYiIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNTg4OTIwNzQ0LCJleHAiOjE1ODkwMDcxNDQsImF6cCI6IkVnVWJBWWxtYXBiZ0xqZlExZ2hLbkhBYUxiRldwc3JVIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.n3k1HKkeOdzo7f_LrPHNl4wG5BGZplpccqZjENfmyCjIzmLpl04YmDENSfVKKziAM-lbFMQ-VUA1EM0ZBux4cHZCykzt-_53RtH972WAUyamN7lWaNFFufYlGZOTRulidAF5n4qUnjG-GHH-8drGjVSt9vYKpVlsyhXOFIGvCFhtIIV8HBJ3e1ZzMJ39tYo1MXghGF7D8X5gBZsmGcRvlqe7iuNIeiy0B69Ltnhvg-_2PQZzAjCeLpfN6-UanRlperIIyY6yCG083KuSfjgDvJsbNZcrrFHNsi9zdg_y2y_1_sBpREI1iWKqSJazCEDYGlr6PCr-lS-p1-4XU39r7w'
EXECUTIVE_PRODUCER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImNzR2xDMFB3VnIzaGNGV1AyWGE3aCJ9.eyJpc3MiOiJodHRwczovL21xcDIyNTkuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYjUwMDQ4MWNjMWFjMGMxNDkyYmJkNyIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNTg4OTIwNjkyLCJleHAiOjE1ODkwMDcwOTIsImF6cCI6IkVnVWJBWWxtYXBiZ0xqZlExZ2hLbkhBYUxiRldwc3JVIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.V9VCmK0K3XWMTfDIbJ4kI_HKOYWN-bJVtnwvZFyzEuOw8wXuDXCXpnyF9I91safFw33ZNvjKQyDZ2BGMY8pKTEiB2ncp9U0u32BhETa5e0iBcUasjPwz8rtMzUn51_ju1XVNJnIgnWJ7dK1mED_FPsT1MFyYcfV198ki319R6PC4iINBIuqNi7d3beMr8ulSEB2NGSNybqFGk0NzvMqxO--P4ZZO0pl7dvjDj9Uybn6cWb4fvjkejzK4v65Y1vJ0tLu7AwmgJ8WuK79ZcB35umJpjL_vUZ7zJJqcVn0aN6GIABWQRrFillakJ0lmosqcsBiMyPskkvNYcV4p-4UnTg'


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_filename = "database_test.db"
        shutil.copy(self.database_filename, './database/')
        self.project_dir = os.path.dirname(os.path.abspath(__file__))
        self.database_path = "sqlite:///{}".format(os.path.join(self.project_dir, 'database', self.database_filename))
        setup_db(self.app, self.database_path)

        self.new_movie = {
            "title": "Harry Potter",
            "release_date": "2020-05-07"
        }

        self.new_actor = {
            "name": "David",
            "age": 28,
            "gender": "Male"
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_actors(self):
        """Test get actors"""
        res = self.client().get('/actors', headers={'Authorization': "Bearer " + CASTING_ASSISTANT_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        self.assertTrue(data['total_actors'])

    def test_401_get_actors_no_authorization(self):
        """Test get actors with no authorization"""
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_get_movies(self):
        """Test get movies"""
        res = self.client().get('/movies', headers={'Authorization': "Bearer " + CASTING_ASSISTANT_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(data['total_movies'])

    def test_401_get_movies_no_authorization(self):
        """Test get movies with no authorization"""
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_get_actor_by_id(self):
        """Test get actor by id"""
        res = self.client().get('/actors/1', headers={'Authorization': "Bearer " + CASTING_ASSISTANT_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        self.assertTrue(data['total_actors'])

    def test_404_get_actor_by_id_no_exist(self):
        """Test get actor by id that does not exist"""
        res = self.client().get('/actors/1000', headers={'Authorization': "Bearer " + CASTING_ASSISTANT_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


    def test_401_get_actor_by_id_no_authorization(self):
        """Test get actor by id with no authorization"""
        res = self.client().get('/actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_get_movie_by_id(self):
        """Test get movie by id"""
        res = self.client().get('/movies/1', headers={'Authorization': "Bearer " + CASTING_ASSISTANT_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(data['total_movies'])

    def test_404_get_movie_by_id_no_exist(self):
        """Test get movie by id that does not exist"""
        res = self.client().get('/movies/1000', headers={'Authorization': "Bearer " + CASTING_ASSISTANT_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


    def test_401_get_movie_by_id_no_authorization(self):
        """Test get movie by id with no authorization"""
        res = self.client().get('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_add_actor(self):
        """Test add actor"""
        res = self.client().post('/actors', json=self.new_actor,  headers={'Authorization': "Bearer " + CASTING_DIRECTOR_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['added'])

    def test_add_actor_no_permission(self):
        """Test add actor with no permission"""
        res = self.client().post('/actors', json=self.new_actor,  headers={'Authorization': "Bearer " + CASTING_ASSISTANT_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_add_actor_no_name(self):
        """Test add actor with no name"""
        res = self.client().post('/actors', json={},  headers={'Authorization': "Bearer " + CASTING_DIRECTOR_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_add_movie(self):
        """Test add movie"""
        res = self.client().post('/movies', json=self.new_movie,  headers={'Authorization': "Bearer " + EXECUTIVE_PRODUCER_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['added'])

    def test_add_movie_no_permission(self):
        """Test add movie with no permission"""
        res = self.client().post('/movies', json=self.new_actor,  headers={'Authorization': "Bearer " + CASTING_DIRECTOR_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_add_movie_no_title(self):
        """Test add movie with no title"""
        res = self.client().post('/movies', json={},  headers={'Authorization': "Bearer " + EXECUTIVE_PRODUCER_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')


    # def test_retrieve_questions(self):
    #     res = self.client().get('/questions')
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['questions'])
    #     self.assertTrue(data['total_questions'])
    #     self.assertTrue(data['categories'])
    #
    # def test_404_retrieve_questions_beyond_valid_page(self):
    #     res = self.client().get('/questions?page=1000')
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'resource not found')
    #
    # def test_delete_question(self):
    #     res = self.client().delete('/questions/2')
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['deleted'])
    #     self.assertTrue(data['questions'])
    #     self.assertTrue(data['total_questions'])
    #     self.assertTrue(data['categories'])
    #
    # def test_422_delete_question_not_exsit(self):
    #     res = self.client().delete('/questions/1000')
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'unprocessable')
    #
    # def test_add_question(self):
    #     res = self.client().post('/questions', json=self.new_question)
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['created'])
    #     self.assertTrue(data['questions'])
    #     self.assertTrue(data['total_questions'])
    #     self.assertTrue(data['categories'])
    #
    # def test_422_add_question_failed(self):
    #     self.app.config["SQLALCHEMY_DATABASE_URI"] = ""
    #     res = self.client().post('/questions', json=self.new_question)
    #     data = json.loads(res.data)
    #     self.app.config["SQLALCHEMY_DATABASE_URI"] = self.database_path
    #
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'unprocessable')
    #
    # def test_search_questions(self):
    #     res = self.client().post('/questions', json={'searchTerm': 'which'})
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['questions'])
    #     self.assertTrue(data['total_questions'])
    #     self.assertTrue(data['categories'])
    #
    # def test_404_search_questions_not_exist(self):
    #     res = self.client().post('/questions', json={'searchTerm': 'Halloween'})
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'resource not found')
    #
    # def test_422_search_questions_failed(self):
    #     self.app.config["SQLALCHEMY_DATABASE_URI"] = ""
    #     res = self.client().post('/questions', json={'searchTerm': 'Halloween'})
    #     data = json.loads(res.data)
    #     self.app.config["SQLALCHEMY_DATABASE_URI"] = self.database_path
    #
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'unprocessable')
    #
    # def test_retrieve_questions_by_category(self):
    #     res = self.client().get('/categories/1/questions')
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['questions'])
    #     self.assertTrue(data['total_questions'])
    #     self.assertTrue(data['categories'])
    #     self.assertEqual(data['current_category'], 1)
    #
    # def test_404_retrieve_questions_by_category_category_not_exsit(self):
    #     res = self.client().get('/categories/100/questions')
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'resource not found')
    #
    # def test_422_retrieve_questions_by_category_failed(self):
    #     self.app.config["SQLALCHEMY_DATABASE_URI"] = ""
    #     res = self.client().get('/categories/1/questions')
    #     data = json.loads(res.data)
    #     self.app.config["SQLALCHEMY_DATABASE_URI"] = self.database_path
    #
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'unprocessable')
    #
    # def test_retrieve_quizzes(self):
    #     res = self.client().post('/quizzes', json={'previous_questions': [], 'quiz_category': {'id': 1}})
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['question'])
    #
    # def test_retrieve_quizzes_failed(self):
    #     res = self.client().post('/quizzes', json={'previous_questions': []})
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'unprocessable')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

