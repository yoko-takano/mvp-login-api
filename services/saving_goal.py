import requests
from typing import Any, Dict, Optional
from schemas.user_info import SavingGoalViewSchema, SavingGoalSchema
from logger import logger


class SavingGoalService:
    """
    Service class for managing saving goals.
    """
    BASE_URL = "http://secondary-api:5000"

    @staticmethod
    def get_saving_goal_by_id(goal_id: int) -> Optional[SavingGoalViewSchema]:
        url = f"{SavingGoalService.BASE_URL}/goals/goal_id?goal_id={goal_id}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.info(f"Erro ao buscar o goal {goal_id}: {e}")
            return None

    @staticmethod
    def post_saving_goal(goal_data: SavingGoalSchema) -> Optional[SavingGoalViewSchema]:
        url = f"{SavingGoalService.BASE_URL}/goals"
        data = {
            'goal_currency': goal_data.goal_currency,
            'goal_name': goal_data.goal_name,
            'goal_value': goal_data.goal_value,
            'monthly_savings': goal_data.monthly_savings
        }
        try:
            response = requests.post(url, data=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.info(f"Erro ao adicionar saving goal: {e}")
            return None

    @staticmethod
    def put_saving_goal_by_id(goal_id: int, goal_data: SavingGoalSchema) -> Optional[SavingGoalViewSchema]:
        url = f"{SavingGoalService.BASE_URL}/goals/goal_id?goal_id={goal_id}"
        data = {
            'goal_currency': goal_data.goal_currency,
            'goal_name': goal_data.goal_name,
            'goal_value': goal_data.goal_value,
            'monthly_savings': goal_data.monthly_savings
        }
        try:
            response = requests.put(url, data=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.info(f"Erro ao atualizar saving goal {goal_id}: {e}")
            return None

    @staticmethod
    def delete_saving_goal_by_id(goal_id: int) -> Optional[str]:
        url = f"{SavingGoalService.BASE_URL}/goals/goal_id?goal_id={goal_id}"
        try:
            response = requests.delete(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.info(f"Erro ao deletar saving goal {goal_id}: {e}")
            return None
