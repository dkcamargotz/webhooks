from typing import List, Generic, TypeVar
import sqlite3
from uuid import UUID
from src.models import Confirmation, ConfirmationStatus, WebhookSubscription
from abc import ABC, abstractmethod
from os import environ

T = TypeVar('T')
class Repository(ABC, Generic[T]):
    @abstractmethod
    def get_all(self) -> List[T]:
        pass
    @abstractmethod
    def get(self, id: UUID) -> T | None:
        pass
    @abstractmethod
    def add(self, confirmation: T) -> UUID:
        pass
    @abstractmethod
    def delete(self, confirmation: T) -> UUID:
        pass
    @abstractmethod
    def update(self, user_id: UUID, updated_confirmation: T) -> True:
        pass

class ConfirmationDatabaseRepository(Repository[Confirmation]):
    def __init__(self):
        self.db = environ['MAIL_SQLITE_DATABASE_PATH']

    def get_all(self) -> List[Confirmation]:
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT uuid, user_id, confirmation_code, status FROM confirmations")
            rows = cursor.fetchall()
            return [
                Confirmation(
                    id=UUID(row[0]),
                    user_id=UUID(row[1]),
                    confirmation_code=row[2],
                    status=ConfirmationStatus(row[3])
                ) for row in rows
            ]

    def get(self, id: UUID) -> Confirmation | None:
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT uuid, user_id, confirmation_code, status FROM confirmations WHERE uuid = ?", (str(id),))
            row = cursor.fetchone()
            if row:
                return Confirmation(
                    id=UUID(row[0]),
                    user_id=UUID(row[1]),
                    confirmation_code=row[2],
                    status=ConfirmationStatus(row[3])
                )
            return None

    def add(self, confirmation: Confirmation) -> UUID:
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO confirmations (uuid, user_id, confirmation_code, status) VALUES (?, ?, ?, ?)",
                (str(confirmation.id), str(confirmation.user_id), confirmation.confirmation_code, confirmation.status.value)
            )
            conn.commit()
            return confirmation.id

    def delete(self, confirmation: Confirmation) -> UUID:
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM confirmations WHERE uuid = ?", (str(confirmation.id),))
            conn.commit()
            return confirmation.id

    def update(self, user_id: UUID, updated_confirmation: Confirmation) -> Confirmation:
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE confirmations
                SET confirmation_code = ?, status = ?, user_id = ?
                WHERE uuid = ?
                """,
                (updated_confirmation.confirmation_code, updated_confirmation.status.value, str(user_id), str(updated_confirmation.id))
            )
            conn.commit()
            return updated_confirmation



class WebhookSubscriptionDatabaseRepository(Repository[WebhookSubscription]):
    def __init__(self):
        self.db = environ['MAIL_SQLITE_DATABASE_PATH']

    def get_all(self) -> List[WebhookSubscription]:
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT uuid, confirmation_id, hook_endpoint FROM webhook_subscriptions")
            rows = cursor.fetchall()
            return [
                WebhookSubscription(
                    id=UUID(row[0]),
                    confirmation_id=UUID(row[1]),
                    hook_endpoint=row[2]
                ) for row in rows
            ]

    def get(self, id: UUID) -> WebhookSubscription | None:
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT uuid, confirmation_id, hook_endpoint FROM webhook_subscriptions WHERE uuid = ?", (str(id),))
            row = cursor.fetchone()
            if row:
                return WebhookSubscription(
                    id=UUID(row[0]),
                    confirmation_id=UUID(row[1]),
                    hook_endpoint=row[2]
                )
            return None

    def add(self, subscription: WebhookSubscription) -> UUID:
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO webhook_subscriptions (uuid, confirmation_id, hook_endpoint) VALUES (?, ?, ?)",
                (str(subscription.id), str(subscription.confirmation_id), subscription.hook_endpoint)
            )
            conn.commit()
            return subscription.id

    def delete(self, subscription: WebhookSubscription) -> UUID:
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM webhook_subscriptions WHERE uuid = ?", (str(subscription.id),))
            conn.commit()
            return subscription.id

    def update(self, id: UUID, updated_subscription: WebhookSubscription) -> WebhookSubscription:
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE webhook_subscriptions
                SET confirmation_id = ?, hook_endpoint = ?
                WHERE uuid = ?
                """,
                (str(updated_subscription.confirmation_id), updated_subscription.hook_endpoint, str(id))
            )
            conn.commit()
            return updated_subscription
