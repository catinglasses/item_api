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

    def update_user(self, user_data: User) -> User:
        """Update existing user in the db"""
        self.db_session.commit()
        return user_data

    def _get_user(self, criteria) -> User:
        """Private method to retrieve a user based on a given criteria"""
        stmt = select(User).where(criteria)
        result = self.db_session.execute(stmt).scalars().one_or_none()
        if result is None:
            raise NoResultFound("User not found")

    def get_user_by_id(self, user_id: Uuid) -> User:
        return self._get_user(User.user_id == user_id)

    def get_user_by_username(self, username: str) -> User:
        return self._get_user(User.username == username)
