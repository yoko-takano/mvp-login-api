from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.attributes import flag_modified
from logger import logger
from models import Session
from models.user_info import UserInfo
from schemas.user_info import UserInfoSchema, UserInfoUpdateUsernameSchema, UserInfoUpdateSalarySchema, \
    SavingGoalSchema, SavingGoalViewSchema, UserInfoSavingGoalSchema
from services import SavingGoalService


class UserInfoService:
    """
    Service class for managing user information and their saving goals.
    Includes management of saving goals stored in the secondary API.
    """

    @staticmethod
    def post_user_information(user_info: UserInfoSchema):
        """
        Creates a new user in the database.
        Returns user data or an error message if it fails.
        """
        logger.info(f"Adding saving goal with name: '{user_info.username}'")
        user_info = UserInfo(
            username=user_info.username,
            password=user_info.password,
            salary=0.0,
        )

        session = None
        try:
            session = Session()
            session.add(user_info)
            session.commit()
            logger.info("User added successfully")
            return user_info.to_dict(), 200

        except IntegrityError:
            session.rollback()
            error_msg = "User with the same username already exists in the database."
            logger.warning(f"Error adding user info '{user_info.username}', {error_msg}")
            return {"message": error_msg}, 409

        except Exception as e:
            error_msg = "Could not save the new user info."
            logger.warning(f"Error adding user info '{user_info.username}', {error_msg}: {str(e)}")
            return {"message": error_msg}, 400

        finally:
            if session:
                session.close()

    @staticmethod
    def get_user_information(username: str):
        """
        Return the user information with goals using the Secondary API.
        """
        session = None
        try:
            session = Session()

            # Find the user information by username
            user_info = session.query(UserInfo).filter(UserInfo.username == username).first()

            if not user_info:
                error_msg = f"User with username {username} not found."
                logger.warning(error_msg)
                return {"message": error_msg}, 404

            saving_goals: List[SavingGoalViewSchema] = []
            total_savings: float = 0.0
            for goal_id in user_info.goal_ids:
                saving_goal_data = SavingGoalService.get_saving_goal_by_id(goal_id)

                if not saving_goal_data:
                    logger.warning(f"Saving goal with ID {goal_id} not found.")
                    continue

                total_savings += saving_goal_data["monthly_savings"]
                saving_goal_instance = SavingGoalViewSchema(
                    id=saving_goal_data["id"],
                    goal_name=saving_goal_data["goal_name"],
                    goal_currency=saving_goal_data["goal_currency"],
                    goal_value=saving_goal_data["goal_value"],
                    monthly_savings=saving_goal_data["monthly_savings"],
                    converted_value=saving_goal_data["converted_value"],
                    created_at=saving_goal_data["created_at"],
                )
                saving_goals.append(saving_goal_instance)

            user_info_goal_instance = UserInfoSavingGoalSchema(
                username=user_info.username,
                password=user_info.password,
                goals=saving_goals,
                salary=user_info.salary,
                total_savings=total_savings,
                created_at=user_info.created_at,
            )

            logger.info(f"{username}")
            return user_info_goal_instance.model_dump(), 200

        except Exception as e:
            error_msg = f"Could not {username}."
            logger.warning(f"Error {username}: {str(e)}")
            return {"message": error_msg}, 400

        finally:
            if session:
                session.close()

    @staticmethod
    def delete_user_information(username: str):
        """
        Deletes a specific user by its username.
        """
        logger.info(f"Deleting saving goal with ID: '{username}'")

        session = None
        try:
            session = Session()

            # Find the user by its username
            user_info = session.query(UserInfo).filter(UserInfo.username == username).first()

            if not user_info:
                error_msg = f"User with username {username} not found."
                logger.warning(error_msg)
                return {"message": error_msg}, 404

            # Delete the user
            session.delete(user_info)
            session.commit()
            logger.info(f"User with username {username} deleted successfully")

            return {"message": f"User with username {username} deleted successfully"}, 200

        except Exception as e:
            error_msg = f"Error deleting user with username {username}."
            logger.error(f"{error_msg}: {str(e)}")
            return {"message": error_msg}, 400

        finally:
            if session:
                session.close()

    @staticmethod
    def put_user_username(username: str, update_username: UserInfoUpdateUsernameSchema):
        """
        Updates the username of an existing user.
        Returns updated user data or an error message.
        """
        new_username = update_username.new_username
        logger.info(f"Updating username with username: '{username}'")

        session = None
        try:
            session = Session()

            # Find the user information by username
            user_info = session.query(UserInfo).filter(UserInfo.username == username).first()

            if not user_info:
                error_msg = f"User with username {username} not found."
                logger.warning(error_msg)
                return {"message": error_msg}, 404

            # Check if the new username already exists
            existing_user = session.query(UserInfo).filter(UserInfo.username == new_username).first()
            if existing_user:
                error_msg = f"User with username {new_username} already exists."
                logger.warning(error_msg)
                return {"message": error_msg}, 409

            # Update the username
            user_info.username = new_username

            session.commit()
            logger.info(f"Username for user with username {username} updated successfully to {new_username}")
            return user_info.to_dict(), 200

        except Exception as e:
            error_msg = f"Could not update username for user with username {username}."
            logger.warning(f"Error updating username for user with username {username}: {str(e)}")
            return {"message": error_msg}, 400

        finally:
            if session:
                session.close()

    @staticmethod
    def put_user_salary(username: str, update_salary: UserInfoUpdateSalarySchema):
        """
        Updates the salary of an existing user.
        Returns updated user data or an error message.
        """
        new_salary = round(update_salary.new_salary, 2)
        logger.info(f"Updating salary with username: '{username}'")

        session = None
        try:
            session = Session()

            # Find the username by username
            user_info = session.query(UserInfo).filter(UserInfo.username == username).first()

            if not user_info:
                error_msg = f"User with username {username} not found."
                logger.warning(error_msg)
                return {"message": error_msg}, 404

            # Update the salary
            user_info.salary = new_salary
            session.commit()
            logger.info(f"Salary for user with username {username} updated successfully to {new_salary}")
            return user_info.to_dict(), 200

        except Exception as e:
            error_msg = f"Could not update salary for user with username {username}."
            logger.warning(f"Error updating salary for user with username {username}: {str(e)}")
            return {"message": error_msg}, 400

        finally:
            if session:
                session.close()

    @staticmethod
    def post_goal_for_user(username: str, saving_goal: SavingGoalSchema):
        """
        Creates a specific saving goal for a user.
        This creates the goal data in the secondary API.
        """
        goal_data = saving_goal.model_dump()
        goal_data['goal_currency'] = goal_data['goal_currency'].value
        logger.info(f"goal_data: {goal_data}")
        logger.info(f"Adding saving goal for user: {username}")

        session = None
        try:
            session = Session()
            user_info = session.query(UserInfo).filter(UserInfo.username == username).first()

            if not user_info:
                error_msg = f"User with username {username} not found."
                logger.warning(error_msg)
                return {"message": error_msg}, 404

            if user_info.goal_ids is None:
                user_info.goal_ids = []

            goal_instance = SavingGoalSchema(**goal_data)
            secondary_api_response = SavingGoalService.post_saving_goal(goal_instance)
            if not secondary_api_response:
                return {"message": "Failed to create goal in secondary API."}, 400

            goal_id = secondary_api_response.get("id")
            if not goal_id:
                return {"message": "Goal ID not found in the response."}, 400

            user_info.goal_ids.append(goal_id)
            logger.info(f"user_info: {user_info}")
            flag_modified(user_info, "goal_ids")  # Forces SQLAlchemy to detect the change
            session.commit()
            logger.info(f"Goal with ID {goal_id} added to user with username {username} successfully")

            return user_info.to_dict(), 200

        except Exception as e:
            error_msg = f"Could not add saving goal for user with username {username}."
            logger.warning(f"Error adding saving goal for user with username {username}: {str(e)}")
            return {"message": error_msg}, 400

        finally:
            if session:
                session.close()


    @staticmethod
    def get_goal_for_user(username: str, goal_id: int):
        """
        Retrieves a specific saving goal for a user using the secondary API.
        """
        logger.info(f"Fetching goal with ID {goal_id} for user {username}")

        session = None
        try:
            session = Session()
            user_info = session.query(UserInfo).filter(UserInfo.username == username).first()

            if not user_info:
                error_msg = f"User with username {username} not found."
                logger.warning(error_msg)
                return {"message": error_msg}, 404

            if not user_info.goal_ids or goal_id not in user_info.goal_ids:
                error_msg = f"Goal ID {goal_id} not found for user {username}."
                logger.warning(error_msg)
                return {"message": error_msg}, 404

            goal_data = SavingGoalService.get_saving_goal_by_id(goal_id)

            if not goal_data:
                error_msg = f"Goal ID {goal_id} not found in secondary API."
                logger.warning(error_msg)
                return {"message": error_msg}, 404

            logger.info(f"Goal retrieved successfully for user {username}: {goal_data}")
            return goal_data, 200

        except Exception as e:
            error_msg = f"Could not retrieve goal with ID {goal_id} for user {username}."
            logger.warning(f"Error fetching goal: {str(e)}")
            return {"message": error_msg}, 400

        finally:
            if session:
                session.close()

    @staticmethod
    def delete_goal_for_user(username: str, goal_id: int):
        """
        Deletes a specific saving goal for a user.
        This removes the reference from the user's `goal_ids` and deletes the goal in the secondary API.
        """
        logger.info(f"Deleting goal with ID {goal_id} for user {username}")

        session = None
        try:
            session = Session()
            user_info = session.query(UserInfo).filter(UserInfo.username == username).first()

            if not user_info:
                error_msg = f"User with username {username} not found."
                logger.warning(error_msg)
                return {"message": error_msg}, 404

            if not user_info.goal_ids or goal_id not in user_info.goal_ids:
                error_msg = f"Goal ID {goal_id} not found for user {username}."
                logger.warning(error_msg)
                return {"message": error_msg}, 404

            # Remove goal from secondary API
            secondary_api_response = SavingGoalService.delete_saving_goal_by_id(goal_id)
            if not secondary_api_response:
                return {"message": "Failed to delete goal in secondary API."}, 400

            # Remove goal from user's list and update in DB
            user_info.goal_ids.remove(goal_id)
            flag_modified(user_info, "goal_ids")  # Forces SQLAlchemy to detect the change
            session.commit()

            logger.info(f"Goal with ID {goal_id} deleted successfully for user {username}")
            return {"message": f"Goal {goal_id} deleted successfully."}, 200

        except Exception as e:
            error_msg = f"Could not delete goal with ID {goal_id} for user {username}."
            logger.warning(f"Error deleting goal: {str(e)}")
            return {"message": error_msg}, 400

        finally:
            if session:
                session.close()

    @staticmethod
    def put_goal_for_user(username: str, goal_id: int, goal: SavingGoalSchema):
        """
        Updates a specific saving goal for a user.
        This updates the goal data in the secondary API.
        """
        goal_data = goal.model_dump()
        goal_data['goal_currency'] = goal_data['goal_currency'].value
        logger.info(f"Updating goal with ID {goal_id} for user {username} with data: {goal_data}")

        session = None
        try:
            session = Session()
            user_info = session.query(UserInfo).filter(UserInfo.username == username).first()

            if not user_info:
                error_msg = f"User with username {username} not found."
                logger.warning(error_msg)
                return {"message": error_msg}, 404

            if not user_info.goal_ids or goal_id not in user_info.goal_ids:
                error_msg = f"Goal ID {goal_id} not found for user {username}."
                logger.warning(error_msg)
                return {"message": error_msg}, 404

            goal_instance = SavingGoalSchema(**goal_data)
            secondary_api_response = SavingGoalService.put_saving_goal_by_id(goal_id, goal_instance)
            if not secondary_api_response:
                return {"message": "Failed to update goal in secondary API."}, 400

            logger.info(f"Goal with ID {goal_id} updated successfully for user {username}")
            return secondary_api_response, 200

        except Exception as e:
            error_msg = f"Could not update goal with ID {goal_id} for user {username}."
            logger.warning(f"Error updating goal: {str(e)}")
            return {"message": error_msg}, 400

        finally:
            if session:
                session.close()
