from src.services.models.users import UserService

def get_user_service() -> UserService:
    return UserService()
