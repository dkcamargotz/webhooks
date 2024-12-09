from flask_restful import Resource
from flask import request
from typing import TypeVar, List, Generic
from uuid import UUID

from .repositories import UserRepository
from .models import User

T = TypeVar('T')
class Controller(Resource, Generic[T]):
    def __init__(self, repository: T):
        super().__init__()
        self.repository: T = repository

class UsersController(Controller[UserRepository]):
    def get(self) -> List[User]:
        return [
            user.to_json() for user in self.repository.get_all()
        ]

class UserController(Controller[UserRepository]):
    def get(self, user_id: str):
        user = self.repository.get(
            id=UUID(user_id)
        )
        if user:
            return user.to_json()
        else:
            return {
                "status": "error",
                "msg": "this user does not exist"
            }
        


    def post(self):
        user_json = request.get_json()
        self.repository.add(
            User.from_json(
                json=user_json
            )
        )

        # TODO: call the mail service webhook here
        
        return {
            "status": "ok"
        }

    def put(self, user_id: str):
        user = self.repository.get(UUID(user_id))
        if not user:
            return {
                "status": "error",
                "msg": "this user does not exist"
            }
        
        user_json = request.get_json()
        updated_user = self.repository.update(
            user_id=user_id,
            updated_user=User.from_json(
                json=user_json
            )
        )
        return {
            "status": "ok",
            "updated_user": updated_user.to_json()
        }
    
    def delete(self, user_id: str):
        user = self.repository.get(UUID(user_id))
        if not user:
            return {
                "status": "error",
                "msg": "this user does not exist"
            }
        
        deleted_user_id = self.repository.delete(user)
        return {
            "status": "ok",
            "deleted_user_id": str(deleted_user_id)
        }