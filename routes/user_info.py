from flask_openapi3 import Tag, APIBlueprint
from schemas import ErrorSchema
from schemas.user_info import UserInfoViewSchema, UserInfoSchema, UserInfoSearchSchema, \
    UserInfoUpdateUsernameSchema, UserInfoUpdateSalarySchema, SavingGoalSchema, SavingGoalViewSchema, \
    UserInfoGoalSearchSchema, UserInfoSavingGoalSchema
from services.user_info import UserInfoService

users_tag = Tag(name="Users", description="Creation, retrieval, and management of users information in the database")
users = APIBlueprint("users", __name__, url_prefix="/users", abp_tags=[users_tag])


@users.post('', tags=[users_tag], responses={
    "200": UserInfoViewSchema,
    "409": ErrorSchema,
    "400": ErrorSchema})
def post_user_information(form:  UserInfoSchema):
    """
    Creates a new user in the database.
    Returns user data or an error message if it fails.
    """
    return UserInfoService.post_user_information(form)


@users.get('<username>', tags=[users_tag], responses= {
    "200": UserInfoSavingGoalSchema,
    "409": ErrorSchema,
    "400": ErrorSchema})
def get_user_information(path: UserInfoSearchSchema):
    """
    Return the information about the given user.
    Information that contains username, salary and total goals savings.
    """
    return UserInfoService.get_user_information(path.username)


@users.delete('<username>', tags=[users_tag], responses={
    "200": {"description": "Successfully deleted the user"},
    "409": ErrorSchema,
    "400": ErrorSchema})
def delete_user_information(path: UserInfoSearchSchema):
    """
    Deletes a specific user by its username.
    """
    return UserInfoService.delete_user_information(path.username)


@users.put('<username>/username', tags=[users_tag], responses= {
    "200": UserInfoViewSchema,
    "409": ErrorSchema,
    "400": ErrorSchema})
def put_user_username(path: UserInfoSearchSchema, form: UserInfoUpdateUsernameSchema):
    """
    Updates the username of an existing user.
    Returns updated user data or an error message.
    """
    return UserInfoService.put_user_username(path.username, form)


@users.put('<username>/salary', tags=[users_tag], responses= {
    "200": UserInfoViewSchema,
    "409": ErrorSchema,
    "400": ErrorSchema})
def put_user_salary(path: UserInfoSearchSchema, form: UserInfoUpdateSalarySchema):
    """
    Updates the salary of an existing user.
    Returns updated user data or an error message.
    """
    return UserInfoService.put_user_salary(path.username, form)


@users.post('/<username>/goal', tags=[users_tag], responses={
    "200": UserInfoViewSchema,
    "409": ErrorSchema,
    "400": ErrorSchema})
def post_goal_for_user(path: UserInfoSearchSchema, form: SavingGoalSchema):
    """
    Creates a specific saving goal for a user.
    This creates the goal data in the secondary API.
    """
    return UserInfoService.post_goal_for_user(path.username, form)


@users.get('/<username>/goal/<goal_id>', tags=[users_tag], responses={
    "200": SavingGoalViewSchema,
    "404": ErrorSchema,
    "400": ErrorSchema})
def get_goal_for_user(path: UserInfoGoalSearchSchema):
    """
    Retrieves a specific saving goal for a user using the secondary API.
    """
    return UserInfoService.get_goal_for_user(path.username, path.goal_id)


@users.delete('/<username>/goal/<goal_id>', tags=[users_tag], responses={
    "200": {"description": "Successfully deleted the goal"},
    "404": ErrorSchema,
    "400": ErrorSchema})
def delete_goal_for_user(path: UserInfoGoalSearchSchema):
    """
    Deletes a specific saving goal for a user.
    This removes the reference from the user's `goal_ids` and deletes the goal in the secondary API.
    """
    return UserInfoService.delete_goal_for_user(path.username, path.goal_id)


@users.put('/<username>/goal/<goal_id>', tags=[users_tag], responses={
    "200": SavingGoalViewSchema,
    "404": ErrorSchema,
    "400": ErrorSchema})
def put_goal_for_user(path: UserInfoGoalSearchSchema, form: SavingGoalSchema):
    """
    Updates a specific saving goal for a user.
    This updates the goal data in the secondary API.
    """
    return UserInfoService.put_goal_for_user(path.username, path.goal_id, form)
