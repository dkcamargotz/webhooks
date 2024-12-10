from flask_restful import Resource
from flask import request
from typing import TypeVar, List, Generic
from uuid import UUID

from src.respositories import Repository
from src.models import Confirmation, ConfirmationBody, WebhookSubscription

T = TypeVar('T')
U = TypeVar('U')
class Controller(Resource, Generic[T, U]):
    def __init__(self, confirmation_repository: T, subscription_repository: U):
        super().__init__()
        self.confirmation_repository: T = confirmation_repository
        self.subscription_repository: U = subscription_repository


class ConfirmationWebhook(Controller[Repository[Confirmation], Repository[WebhookSubscription]]):
    def get(self):
        return {
            "status": "ok"
        }
        
    def post(self):
        body = ConfirmationBody.from_json(request.get_json())
        if body:
            confirmation = Confirmation(body.user_id)
            self.confirmation_repository.add(confirmation)
            
            subscription = WebhookSubscription(
                confirmation_id=confirmation.id,
                hook_endpoint=body.hook_endpoint
            )
            self.subscription_repository.add(subscription)

            return {
                "status": "ok"
            }

        return (
            {"status": "err"}, 403, None
        )