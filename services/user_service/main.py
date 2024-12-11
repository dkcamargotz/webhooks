from flask import Flask
from flask_restful import Api
from src.controllers import UsersController, UserController, UserByIdController
from src.repositories import UserDatabaseRepository
from dotenv import load_dotenv
from os import environ

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
    '/user',
    resource_class_kwargs={
        "repository": user_repository
    }
)
api.add_resource(
    UserByIdController, 
    '/user/<string:user_id>',
    resource_class_kwargs={
        "repository": user_repository
    }
)

if __name__ == '__main__':
    app.run(
        debug=True,
        host=environ.get('USERS_HOST'),
        port=environ.get('USERS_PORT')
    )
