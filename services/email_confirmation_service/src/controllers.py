from flask_restful import Resource
from flask import request
from typing import TypeVar, List, Generic
from uuid import UUID
import requests

from src.respositories import Repository, WebhookSubscriptionRepository
from src.models import Confirmation, ConfirmationStatus, ConfirmationBody, WebhookSubscription, WebhookSubscriptionBody
from src.email_handler import send_email
T = TypeVar('T')
U = TypeVar('U')
class Controller(Resource, Generic[T, U]):
    def __init__(self, confirmation_repository: T, subscription_repository: U):
        super().__init__()
        self.confirmation_repository: T = confirmation_repository
        self.subscription_repository: U = subscription_repository


class ConfirmationWebhook(Controller[Repository[Confirmation], WebhookSubscriptionRepository]):
    def get(self):
        return {
            "status": "ok"
        }
    
    def post(self):
        body = WebhookSubscriptionBody.from_json(request.get_json())
        if body:
            confirmation = Confirmation(body.user_id)
            self.confirmation_repository.add(confirmation)
            
            subscription = WebhookSubscription(
                confirmation_id=confirmation.id,
                hook_endpoint=body.hook_endpoint
            )
            self.subscription_repository.add(subscription)

            send_email(
                receiver_email=body.email,
                subject="Douglas App confirmation code",
                message_body=f"Your confirmation code is: {confirmation.confirmation_code} do not share with anybody."
            )

            return {
                "status": "ok",
                "subscription": subscription.to_json(),
                "confirmation": confirmation.to_json()
            }

        return (
            {"status": "err"}, 403, None
        )

class ConfirmationController(Controller[Repository[Confirmation], WebhookSubscriptionRepository]):
    def post(self, confirmation_id: str):
        confirmation_uuid = UUID(confirmation_id)
        body = ConfirmationBody.from_json(
            request.get_json()
        )
        if body:
            confirmation = self.confirmation_repository.get(confirmation_uuid)
            
            if confirmation and confirmation.confirmation_code == body.confirmation_code:
                confirmation.status = ConfirmationStatus.PROCESSED
                self.confirmation_repository.update(
                    confirmation_uuid,
                    confirmation
                )

                subscription: WebhookSubscription | None = self.subscription_repository.get_by_confirmation_id(confirmation_uuid)
                if subscription:
                    try:
                        response = requests.request(
                            method="POST", 
                            url=subscription.hook_endpoint
                        )
                        if not response.ok:
                            raise Exception('Request failed')
                        
                        return {
                            "status": "ok"
                        }
                    except Exception as e:
                        return (
                            {"status": "err", "msg": "webhook hook request failed", "subscription": subscription.to_json()},
                            503,
                            None
                        )
                else:
                    return {
                        "status": "ok",
                        "msg": "there's no hooks subscribed."
                    }
            else:
                return (
                    {"status": "err"}, 401, None
                )
        
        return (
            {"status": "err"}, 403, None
        )