from flask import Flask, request
from flask_restful import Resource, Api
import sqlite3
from dataclasses import dataclass, field
from uuid import UUID, uuid4
from typing import List
from json import loads
from abc import ABC, abstractmethod


app = Flask(__name__)
api = Api(app)


@dataclass
class User:
    name: int
    password: int
    id: UUID = field(default_factory=uuid4)

    def to_json(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "password": self.password
        }

    @classmethod
    def from_json(cls, json: dict):
        json_id = json.get('id')

        return cls(
            name=json['name'],
            password=json['password'],
            id=UUID(json_id) if json_id else uuid4()
        )


class UserRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[User]:
        pass
    
    @abstractmethod
    def get(self, id: UUID) -> User | None:
        pass
    @abstractmethod
    def add(self, user: User) -> UUID:
        pass

class UserDatabaseRepository(UserRepository):
    # TODO
    def __init__(self):
        raise NotImplementedError('TODO')

class UserMemoryRepository(UserRepository):
    def __init__(self):
        self.users: List[User] = [
            User(
                name='Douglas',
                password='camargo1508',
            ),
            User(
                name="Sol",
                password="fredes1606",
            )
        ]

    def get_all(self) -> List[User]:
        return self.users
    
    def get(self, id: UUID) -> User | None:
        for user in self.users:
            if user.id == id:
                return user
        return None
    
    def add(self, user: User) -> UUID:
        self.users.append(user)
        return user.id

class UserResource(Resource):
    def __init__(self, repository: UserRepository):
        super().__init__()
        self.repository: UserRepository = UserMemoryRepository()

class UsersController(UserResource):
    def get(self) -> List[User]:
        return [
            user.to_json() for user in self.repository.get_all()
        ]

class UserController(UserResource):
    def get(self, user_id: str) -> User:
        return self.repository.get(
            id=UUID(user_id)
        ).to_json()

    def post(self) -> None:
        user_json = request.get_json()
        self.repository.add(
            User.from_json(
                json=user_json
            )
        )


api.add_resource(UsersController, '/users')
api.add_resource(UserController, '/user', '/user/<string:user_id>')

if __name__ == '__main__':
    app.run(
        debug=True,
        host='localhost',
        port='5000'
    )
