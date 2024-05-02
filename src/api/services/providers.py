from src.api.utils.security import is_password_strong 
from src.core.security import (
    hash_password, 
    create_access_token
)
from src.api.models import Provider
from src.api.models import (
    ProviderRequestModel, 
    WeakPasswordException
)
from uuid import uuid4

def register_provider(provider_data: dict) -> ProviderRequestModel:
    # Relevant data
    username = provider_data["username"]
    
    # Relevant data
    password = provider_data["password"]

    if not is_password_strong(password):
        raise WeakPasswordException(password)

    data = {
        "prov_username": username,
        "prov_password": password
    }
    access_token = create_access_token(data)

    # Hash the password using a secure algorithm (e.g., bcrypt)
    hashed_password = hash_password(password)

    # Create a new provider instance with the hashed password
    provider = Provider(
        prov_id = uuid4(),
        prov_name = username,
        prov_password = password,
        prov_hashed_password = hashed_password,
        prov_token_str = access_token,
    )

    return provider