from fastapi import APIRouter

from src.models import User, ErrorResponse, MessageResponse
from src.database.models import UserDB
from src.utils.constants import CREATED_201, BAD_REQUEST_400, INTERNAL_SERVER_ERROR_500
from src.utils.routes import make_json_response

router = APIRouter()


@router.post("/users", response_model=dict)
def create_user(user: User):
    db_user = UserDB(username=user.username, password=user.password)

    # Save the user to the database
    try:
        check_user = UserDB.query.filter_by(username=user.username).first()

        if check_user:
            db_user.save()

            success_message = MessageResponse(message="User created successfully")
            return make_json_response(CREATED_201, success_message)

        else:
            error_message = ErrorResponse(error="User already exists")
            return make_json_response(BAD_REQUEST_400, error_message)

    except Exception as e:
        error_message = ErrorResponse(error=str(e))
        return make_json_response(INTERNAL_SERVER_ERROR_500, error_message)
