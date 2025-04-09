import enum
from datetime import datetime
from typing import List

from pydantic import BaseModel, field_validator


class CurrencyEnumSchema(str, enum.Enum):
    USD = "USD"
    BRL = "BRL"
    EUR = "EUR"
    JPY = "JPY"
    KRW = "KRW"


class UserInfoSchema(BaseModel):
    """
    Defines how a new user login should be represented for insertion.
    """
    username: str = "ChocolateCookie" # The users user
    password: str= "password123"  # The users password


class UserInfoSearchSchema(BaseModel):
    username: str


class UserInfoGoalSearchSchema(BaseModel):
    username: str
    goal_id: int


class UserInfoUpdateUsernameSchema(BaseModel):
    new_username: str


class UserInfoUpdateSalarySchema(BaseModel):
    new_salary: float


class UpdateSalarySchema(BaseModel):
    """
    Defines something
    """
    username: str = "ChocolateCookie"
    salary: int = 0


class UserInfoViewSchema(BaseModel):
    """
    Defines how a saving goal will be returned with full data.
    """
    username: str
    password: str
    goal_ids: List[str]
    salary: int
    created_at: datetime

    class Config:
        orm_mode = True

    @field_validator("created_at")
    @classmethod
    def convert_datetime(cls, v):
        """
        Converts the datetime object to a formatted string.
        """
        return v.strftime("%Y-%m-%d %H:%M:%S") if isinstance(v, datetime) else v


class SavingGoalSchema(BaseModel):
    """
    Defines how a saving goal will be returned with full data.
    """
    goal_name: str = "Pretty dress" # Name of the saving goal
    goal_currency: CurrencyEnumSchema = "USD" # Currency of the saving goal
    goal_value: float = 300.00 # Total value to be saved for the goal
    monthly_savings: float = 100.0 # Savings per month of the salary to be saved


class SavingGoalViewSchema(BaseModel):
    """
    Defines how a saving goal will be returned with full data.
    """
    id: int
    goal_name: str
    goal_currency: str
    goal_value: float
    monthly_savings: float
    converted_value: float
    created_at: datetime

    class Config:
        orm_mode = True

    @field_validator("created_at")
    @classmethod
    def convert_datetime(cls, v):
        """
        Converts the datetime object to a formatted string.
        """
        return v.strftime("%Y-%m-%d %H:%M:%S") if isinstance(v, datetime) else v


class UserInfoSavingGoalSchema(BaseModel):
    """
    Defines how a user information and saving goal will be returned with full data.
    TODO improve the comment!
    """
    username: str
    password: str
    goals: List[SavingGoalViewSchema]
    salary: int
    total_savings: float
    created_at: datetime
