from flask import Flask
from flask_restful import Api
from src.controllers import UsersController, UserController
from src.repositories import UserDatabaseRepository
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
api = Api(app)

user_repository = UserDatabaseRepository()

# rounting definitions
api.add_resource(
    UsersController, 
    '/users',
    resource_class_kwargs={
        "repository": user_repository
    }
)

api.add_resource(
    UserController, 
    '/user', '/user/<string:user_id>',
    resource_class_kwargs={
        "repository": user_repository
    }
)

if __name__ == '__main__':
    app.run(
        debug=True,
        host='127.0.0.1',
        port='5000'
    )
