from dataclasses import dataclass, field
from uuid import UUID, uuid4
from enum import Enum
from typing import Self

def generate_new_confirmation_code() -> str:
    return 'A1B2C3'

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

@dataclass
class WebhookSubscription:
    confirmation_id: UUID
    hook_endpoint: str
    id: UUID = field(default_factory=uuid4)

@dataclass
class ConfirmationBody:
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
