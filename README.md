# Full Stack Developer NanoDegree Capstone Project

## Casting Agency Project

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies.

## Roles

There are three roles in this system and their corresponding permissions are shown:

1. Casting Assistant
  * Can view actors and movies: "get:actors", "get:movies"
2. Casting Director
  * All permissions a Casting Assistant has: "get:actors", "get:movies"
  * and add or delete an actor from the database: "post:actors", "delete:actors"
  * and modify actors or movies: "patch:actors", "patch:movies"
3. Executive Producer
  * All permissions a Casting Director has: "get:actors", "post:actors", "delete:actors", "patch:actors", "get:movies"， "patch:movies"
  * and add or delete a movie from the database:
  "post:movies"， "delete:movies"

## Authentication

Auth0 is used in this project for authentication. The configuration parameters for Auth0 is stored in /auth/config.py:
- AUTH0_DOMAIN = 'mqp2259.auth0.com'
- ALGORITHMS = ['RS256']
- API_AUDIENCE = 'capstone'

The JWT tokens generated from auth0 are stored in test_app.py file. They are:
- Casting Assistant: 
```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImNzR2xDMFB3VnIzaGNGV1AyWGE3aCJ9.eyJpc3MiOiJodHRwczovL21xcDIyNTkuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYWY4Mzc1NTRiMTRjMGMxMjczMzhjYyIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNTg4OTIwNjE3LCJleHAiOjE1ODkwMDcwMTcsImF6cCI6IkVnVWJBWWxtYXBiZ0xqZlExZ2hLbkhBYUxiRldwc3JVIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.Ykkjmbcisi9s1NGdkdyfpWK20e-7evkDCpxqSxT-5mL_zAt_W0FMUD8XKd6otnDHUJW73AvRJRLvgx3dNdmfOhi2pwoZPkKLTKsWCg3US6kej5-5xYRjzIkTD75eVB4wD8O9fDiZnNMs6RncCT0Nl86oIjxjv63C3rXT2ag-zuDQpJ-Prl_VKIsKaioWnz_iLXl8_KafyEuc6YW_kJmbx2Ci8v7lsNXIAZUwNk4Q6-8JBUHy-VwA4ta8ellGoKd37-SJ726W5VXT1Gae6Egfclg2wS6jD6F4ig7g63gUadO14wexiICbmDOa1EASxGnHDNPz6XOE1Egdpq5GCq20zw
```
- Casting Director:
```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImNzR2xDMFB3VnIzaGNGV1AyWGE3aCJ9.eyJpc3MiOiJodHRwczovL21xcDIyNTkuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYjFlY2Y0MWNjMWFjMGMxNDg5NjgxYiIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNTg4OTIwNzQ0LCJleHAiOjE1ODkwMDcxNDQsImF6cCI6IkVnVWJBWWxtYXBiZ0xqZlExZ2hLbkhBYUxiRldwc3JVIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.n3k1HKkeOdzo7f_LrPHNl4wG5BGZplpccqZjENfmyCjIzmLpl04YmDENSfVKKziAM-lbFMQ-VUA1EM0ZBux4cHZCykzt-_53RtH972WAUyamN7lWaNFFufYlGZOTRulidAF5n4qUnjG-GHH-8drGjVSt9vYKpVlsyhXOFIGvCFhtIIV8HBJ3e1ZzMJ39tYo1MXghGF7D8X5gBZsmGcRvlqe7iuNIeiy0B69Ltnhvg-_2PQZzAjCeLpfN6-UanRlperIIyY6yCG083KuSfjgDvJsbNZcrrFHNsi9zdg_y2y_1_sBpREI1iWKqSJazCEDYGlr6PCr-lS-p1-4XU39r7w
```
Executive Producer:
```
 eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImNzR2xDMFB3VnIzaGNGV1AyWGE3aCJ9.eyJpc3MiOiJodHRwczovL21xcDIyNTkuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYjUwMDQ4MWNjMWFjMGMxNDkyYmJkNyIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNTg4OTIwNjkyLCJleHAiOjE1ODkwMDcwOTIsImF6cCI6IkVnVWJBWWxtYXBiZ0xqZlExZ2hLbkhBYUxiRldwc3JVIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.V9VCmK0K3XWMTfDIbJ4kI_HKOYWN-bJVtnwvZFyzEuOw8wXuDXCXpnyF9I91safFw33ZNvjKQyDZ2BGMY8pKTEiB2ncp9U0u32BhETa5e0iBcUasjPwz8rtMzUn51_ju1XVNJnIgnWJ7dK1mED_FPsT1MFyYcfV198ki319R6PC4iINBIuqNi7d3beMr8ulSEB2NGSNybqFGk0NzvMqxO--P4ZZO0pl7dvjDj9Uybn6cWb4fvjkejzK4v65Y1vJ0tLu7AwmgJ8WuK79ZcB35umJpjL_vUZ7zJJqcVn0aN6GIABWQRrFillakJ0lmosqcsBiMyPskkvNYcV4p-4UnTg
 ```


## Run the project locally

All the requirements are stored in requirements.txt. The following command can be run to install the dependencies:
```
pip install -r requirements.txt
```

The main script is app.py. The server can be turned on by using the following commands:
```
set FLASK_APP = app.py
flask run
```
The project is tested using pytest and postman. The postman collection file is `capstone.postman_collection.json`. The py test file is `test_app.py`.
2### Backend

## API Reference

### Getting Started
- Base URL: At present this app is hosted at `https://castingagencycapstone.herokuapp.com/`
- Authentication: the tokens are provided above for test purposes. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 422,
    "message": "unprocessable"
}
```
The API will return two error types when requests fail:
- 400: Bad Request
- 401: Permission not found
- 404: Resource Not Found
- 422: Not Processable

### Endpoints 
#### GET /actors
- General:
    - Returns a list of actors, success value, and total number of actors
    - Bearer token should be added in the header to pass the authentication
    - Roles: Casting Assistant, Casting Director, Executive Producer
- Sample: `curl https://castingagencycapstone.herokuapp.com/actors`
``` 
{
    "actors": [
        {
            "age": 30,
            "gender": "Male",
            "id": 1,
            "name": "David"
        },
        {
            "age": 28,
            "gender": "Male",
            "id": 3,
            "name": "David"
        },
        {
            "age": 28,
            "gender": "Male",
            "id": 4,
            "name": "David"
        }
    ],
    "success": true,
    "total_actors": 3
}
```
#### GET /movies
- General:
    - Returns a list of movies, success value, and total number of movies
    - Bearer token should be added in the header to pass the authentication
    - Roles: Casting Assistant, Casting Director, Executive Producer
- Sample: `curl https://castingagencycapstone.herokuapp.com/movies`
``` 
{
    "movies": [
        {
            "id": 1,
            "release_date": "2020-05-20",
            "title": "Harry Potter 5"
        },
        {
            "id": 2,
            "release_date": "2020-05-07",
            "title": "Harry Potter"
        }
    ],
    "success": true,
    "total_movies": 2
}
```
#### GET /actors/{actor_id}
- General:
    - Returns a single actors by id, success value, and total number of actors (which is 1)
    - Bearer token should be added in the header to pass the authentication
    - Roles: Casting Assistant, Casting Director, Executive Producer
- Sample: `curl https://castingagencycapstone.herokuapp.com/actors/1`
``` 
{
    "actors": [
        {
            "age": 30,
            "gender": "Male",
            "id": 1,
            "name": "David"
        }
    ],
    "success": true,
    "total_actors": 1
}
```
#### GET /movies/{movie_id}
- General:
    - Returns a single movie by id, success value, and total number of movies (which is 1)
    - Bearer token should be added in the header to pass the authentication
    - Roles: Casting Assistant, Casting Director, Executive Producer
- Sample: `curl https://castingagencycapstone.herokuapp.com/movies/1`
``` 
{
    "movies": [
        {
            "id": 1,
            "release_date": "2020-05-20",
            "title": "Harry Potter 5"
        }
    ],
    "success": true,
    "total_movies": 1
}
```
#### DELETE /actors/{actor_id}
- General:
    - Deletes the actor for the given ID if it exists. Returns the info of the deleted actor and success value.
    - Bearer token should be added in the header to pass the authentication
    - Roles: Casting Director, Executive Producer
- Sample: `curl -X DELETE https://castingagencycapstone.herokuapp.com/actors/1`
```
{
    "deleted": {
        "age": 30,
        "gender": "Male",
        "id": 1,
        "name": "David"
    },
    "success": true
}
```
#### DELETE /movies/{movie_id}
- General:
    - Deletes the movie for the given ID if it exists. Returns the info of the deleted movie and success value.
    - Bearer token should be added in the header to pass the authentication
    - Roles: Executive Producer
- Sample: `curl -X DELETE https://castingagencycapstone.herokuapp.com/movies/1`
```
{
    "deleted": {
        "id": 2,
        "release_date": "2020-05-07",
        "title": "Harry Potter"
    },
    "success": true
}
```
#### POST /actors
- General:
    - Creates a new actor using the json string. It returns the added actor and success value. 
    - Bearer token should be added in the header to pass the authentication
    - Roles: Casting Director, Executive Producer
- Sample: `curl https://castingagencycapstone.herokuapp.com/actors -X POST -H "Content-Type: application/json" -d "{\"name\":\"David\", \"age\":28, \"gender\":\"Male\"}"`
```
{
    "added": {
        "age": 28,
        "gender": "Male",
        "id": 5,
        "name": "David"
    },
    "success": true
}
```
#### POST /movies
- General:
    - Creates a new movie using the json string. It returns the added movie and success value. 
    - Bearer token should be added in the header to pass the authentication
    - Roles: Executive Producer
- Sample: `curl https://castingagencycapstone.herokuapp.com/actors -X POST -H "Content-Type: application/json" -d "{\"title\":\"Harry Potter\", \"release_date\":\"2020-05-07\"}"`
```
{
    "added": {
        "id": 2,
        "release_date": "2020-05-07",
        "title": "Harry Potter"
    },
    "success": true
}
```
#### PATCH /actors/{actor_id}
- General:
    - Updates an actor by the given id using the json string. It returns the updated actor and success value. 
    - Bearer token should be added in the header to pass the authentication
    - Roles: Casting Director, Executive Producer
- Sample: `curl https://castingagencycapstone.herokuapp.com/actors/3 -X PATCH -H "Content-Type: application/json" -d "{\"name\":\"David\", \"age\":30, \"gender\":\"Male\"}"`
```
{
    "success": true,
    "updated": {
        "age": 30,
        "gender": "Male",
        "id": 3,
        "name": "David"
    }
}
```
#### PATCH /movies
- General:
    - Updates a movie by the given id using the json string. It returns the updated movie and success value. 
    - Bearer token should be added in the header to pass the authentication
    - Roles: Casting Director, Executive Producer
- Sample: `curl https://castingagencycapstone.herokuapp.com/movies/1 -X POST -H "Content-Type: application/json" -d "{\"title\":\"Harry Potter 5\", \"release_date\":\"2020-05-20\"}"`
```
{
    "success": true,
    "updated": {
        "id": 1,
        "release_date": "2020-05-20",
        "title": "Harry Potter 5"
    }
}
```

## Authors
The project was completed by Qipei Mei as the capstone project of the Udacity Fully Stack Developer Nanodegree