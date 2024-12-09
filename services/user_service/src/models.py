from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class User:
    name: str
    mail: str
    confirmed: bool
    id: UUID = field(default_factory=uuid4)

    def to_json(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "mail": self.mail,
            "confirmed": self.confirmed
        }

    @classmethod
    def from_json(cls, json: dict):
        json_id = json.get('id')
        json_confirmed = json.get('confirmed')
        return cls(
            confirmed=bool(json_confirmed),
            name=json['name'],
            mail=json['mail'],
            id=UUID(json_id) if json_id else uuid4()
        )

