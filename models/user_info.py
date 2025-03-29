from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from models import Base


class UserInfo(Base):
    """
    Model representing a user login, including username, password, salary,
    and an optional list of associated saving goals (IDs).
    """
    __tablename__ = "user_info"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    salary = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    goal_ids = Column(JSON, nullable=True)

    def __init__(self, username: str, password: str, salary: float, goal_ids: list = None, **kwargs):
        """
        Initializes a new user login with the provided parameters.

        :param username: The username for the login
        :param password: The password for the login (should be hashed)
        :param salary: The user's salary
        :param goal_ids: A list of goal IDs associated with the user (optional)
        """
        super().__init__(**kwargs)
        self.username = username
        self.password = password
        self.salary = salary
        self.goal_ids = goal_ids or []

    def to_dict(self):
        """
        Returns a dictionary representation of the UserLogin object.
        """
        return {
            "id": self.id,
            "username": self.username,
            "salary": self.salary,
            "goal_ids": self.goal_ids,  # Lista de IDs de goals
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }

    def __repr__(self):
        return f"UserInfo(id={self.id}, username='{self.username}', salary={self.salary}, goal_ids={self.goal_ids})"
