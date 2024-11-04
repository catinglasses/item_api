from sqlalchemy import Uuid, select
from sqlalchemy.orm import Session

from src.models.users import User

class UserRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_user(self, user_data: User) -> User:
        self.db_session.add(user_data)
        self.db_session.commit()
        self.db_session.refresh(user_data)
        return user_data

    def get_user_by_id(self, user_id: Uuid) -> User:
        return self.db_session.select(User).where(User.user_id == user_id)

    def get_user_by_username(self, username: str) -> User:
        return self.db_session.select(User).where(User.username == username)
