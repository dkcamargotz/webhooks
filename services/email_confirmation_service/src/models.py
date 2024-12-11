from dataclasses import dataclass, field
from uuid import UUID, uuid4
from enum import Enum
from typing import Self
import string
import random

def generate_new_confirmation_code() -> str:
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

class ConfirmationStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    PROCESSED = "processed"
    ERROR = "error"

@dataclass
class Confirmation:
    user_id: UUID
    id: UUID = field(default_factory=uuid4)
    confirmation_code: str = field(default_factory=generate_new_confirmation_code)
    status: ConfirmationStatus = ConfirmationStatus.PENDING

    def to_json(self) -> dict:
        return {
            "user_id": str(self.user_id),
            "id": str(self.id),
            "confirmation_code": self.confirmation_code,
            "status": self.status.name
        }

@dataclass
class WebhookSubscription:
    confirmation_id: UUID
    hook_endpoint: str
    id: UUID = field(default_factory=uuid4)
    
    def to_json(self) -> dict:
        return {
            "id": str(self.id),
            "hook_endpoint": self.hook_endpoint,
            "confirmation_id": str(self.confirmation_id)
        }

@dataclass
class WebhookSubscriptionBody:
    user_id: UUID
    email: str
    hook_endpoint: str

    @classmethod
    def from_json(cls, json: dict) -> Self | None:
        user_id = json.get('user_id')
        email = json.get('email')
        hook_endpoint = json.get('hook_endpoint')

        # validating json
        if user_id and email and hook_endpoint:
            return cls(
                user_id=user_id,
                email=email,
                hook_endpoint=hook_endpoint
            )
        return None

@dataclass
class ConfirmationBody:
    confirmation_code: str

    @classmethod
    def from_json(cls, json: dict) -> Self | None:
        confirmation_code = json.get('confirmation_code')


        # validating json
        if confirmation_code and len(confirmation_code) == 6:
            return cls(
                confirmation_code=confirmation_code,
            )
        return None