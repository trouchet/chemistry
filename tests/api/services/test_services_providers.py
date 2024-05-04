import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.services.providers import ProviderService
from src.db.schemas import Provider


async def test_register_provider_with_strong_password(mocker):
    """Tests successful registration with a strong password."""
    strong_password = "StrongPassword1!"
    provider_data = {"username": "test_user", "password": strong_password}

    # Mock is_password_strong to return True
    mocker.patch("src.api.utils.security.is_password_strong", return_value=True)

    # Mock the AsyncSession
    mock_session = mocker.AsyncMock(spec=AsyncSession)
    provider = await ProviderService().register(provider_data, session=mock_session)

    assert isinstance(provider, Provider)
    assert provider.prov_username == provider_data["username"]
    # Don't assert password directly (security reasons)
    assert provider.prov_hashed_password != provider_data["password"]


async def test_register_provider_with_weak_password(mocker):
    """Tests raising WeakPasswordException for a weak password."""
    weak_password = "weakpass"
    provider_data = {"username": "test_user", "password": weak_password}

    mock_session = mocker.AsyncMock(spec=AsyncSession)

    with pytest.raises(HTTPException) as excinfo:
        await ProviderService().register(provider_data, mock_session)

    assert excinfo.type == HTTPException


async def test_register_provider_with_missing_username(mocker):
    """Tests raising error for missing username."""
    provider_data = {"password": "StrongPassword1!"}

    # Mock the AsyncSession
    mock_session = mocker.AsyncMock(spec=AsyncSession)

    with pytest.raises(KeyError):
        await ProviderService().register(provider_data, session=mock_session)


async def test_register_provider_with_missing_password(mocker):
    """Tests raising error for missing password."""
    provider_data = {"username": "test_user"}

    mock_session = mocker.AsyncMock(spec=AsyncSession)

    with pytest.raises(KeyError):
        await ProviderService().register(provider_data, mock_session)
