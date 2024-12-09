from typing import List
import sqlite3
from uuid import UUID
from src.models import User
from json import loads
from abc import ABC, abstractmethod
from os import environ


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
    @abstractmethod
    def delete(self, user: User) -> UUID:
        pass
    @abstractmethod
    def update(self, user_id: UUID, updated_user: User) -> User:
        pass

class UserDatabaseRepository(UserRepository):
    def __init__(self):
        self.db = environ['SQLITE_DATABASE_PATH']

    def get_all(self) -> List[User]:
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT uuid, name, mail, confirmed FROM users")
            rows = cursor.fetchall()
            return [User(id=UUID(row[0]), name=row[1], mail=row[2], confirmed=bool(row[3])) for row in rows]

    def get(self, id: UUID) -> User | None:
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT uuid, name, mail, confirmed FROM users WHERE uuid = ?", (str(id),))
            row = cursor.fetchone()
            if row:
                return User(id=UUID(row[0]), name=row[1], mail=row[2], confirmed=bool(row[3]))
            return None

    def add(self, user: User) -> UUID:
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (uuid, name, mail, confirmed) VALUES (?, ?, ?, ?)",
                (str(user.id), user.name, user.mail, user.confirmed)
            )
            conn.commit()
            return user.id
    
    def update(self, user_id: UUID, updated_user: User) -> User:
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET name=?, mail=?, confirmed=? WHERE uuid=?",
                ( updated_user.name, updated_user.mail, updated_user.confirmed, str(user_id))
            )
            conn.commit()
            updated_user.id = user_id   
            return updated_user

    def delete(self, user: User) -> UUID:
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM users WHERE uuid=?",
                (str(user.id),)
            )
            conn.commit()
            return user.id


class UserMemoryRepository(UserRepository):
    def __init__(self):
        self.users: List[User] = [
            User(
                name='Douglas',
                mail='camargo.douglas@icloud.com',
            ),
            User(
                name="Sol",
                mail="solcfredes@gmail.com",
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
    
    def update(self, user: User):
        raise NotImplementedError('This method was not implemented yet.')
    def delete(self, user: User):
        raise NotImplementedError('This method was not implemented yet.')