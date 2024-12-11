from flask_restful import Resource
from flask import request
from typing import TypeVar, List, Generic
from uuid import UUID
import requests
import json
from os import environ

from src.repositories import UserRepository
from src.models import User

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
    def post(self):
        user = User.from_json(request.get_json())
        try:
            response = requests.request(
                method="POST", 
                url=f"http://{environ.get('MAIL_HOST')}:{environ.get('MAIL_PORT')}/webhook/confirmation", 
                headers={
                    'Content-Type': 'application/json'
                },
                data=json.dumps({
                    "user_id": str(user.id),
                    "email": user.mail,
                    "hook_endpoint": f"http://{environ.get('USERS_HOST')}:{environ.get('USERS_PORT')}/user/{str(user.id)}"
                })
            )
            if not response.ok:
                raise Exception('Request failed')
            
            self.repository.add(user)
            return {
                "status": "ok",
                "response": json.loads(response.text)
            }
        except Exception as e:
            return (
                {"status": "err", "msg": str(e)}, 503, None
            )

class UserByIdController(Controller[UserRepository]):
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
        


    def post(self, user_id: str):
        user = self.repository.get(user_id)
        user.confirmed = True
        self.repository.update(
            user_id=user_id,
            updated_user=user
        )
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