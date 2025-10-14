import keyring
import pytest
from unittest.mock import patch, MagicMock
import os

from keyring.errors import PasswordDeleteError

from constants import APP_NAME, TOKEN_KEY
from token_manager import TokenManager
from auth_data_class import AuthenticationResult

# Use a plaintext keyring for CI environments where secure storage may not be available
if os.getenv("CI") == "true":
    try:
        from keyrings.alt.file import PlaintextKeyring

        keyring.set_keyring(PlaintextKeyring())
    except ImportError:
        raise RuntimeError("keyrings.alt must be installed for CI keyring fallback")


@pytest.fixture
def token_manager() -> TokenManager:
    return TokenManager()


def _delete_test_token():
    try:
        keyring.delete_password(APP_NAME, TOKEN_KEY)
    except PasswordDeleteError:
        pass


@pytest.fixture
def set_test_token_for_load() -> str:
    test_token = "test_token_abc_123"
    keyring.set_password(APP_NAME, TOKEN_KEY, test_token)
    yield test_token  # Pass token to the test
    _delete_test_token()


def test_load_token_returns_correct_value(
    token_manager: TokenManager, set_test_token_for_load: str
) -> None:
    assert token_manager.load_token() == set_test_token_for_load


def test_load_token_returns_none_if_missing(token_manager: TokenManager):
    _delete_test_token()
    assert token_manager.load_token() is None


@pytest.fixture
def set_test_token_for_save() -> str:
    test_token = "test_token_abc_123"
    yield test_token  # Pass token to the test
    _delete_test_token()


def test_save_token_stores_value(
    token_manager: TokenManager, set_test_token_for_save: str
):
    token_manager.save_token(set_test_token_for_save)
    assert set_test_token_for_save == keyring.get_password(APP_NAME, TOKEN_KEY)


@pytest.mark.parametrize(
    "token_input, side_effect, expected_response, expected_message",
    [
        (
            "valid_token",
            False,
            True,
            "Authenticated as test_user",
        ),
        ("invalid_token", True, False, "Token verification failed"),
        ("", False, False, "No token provided"),
    ],
    ids=["valid", "invalid", "empty"],
)
def test_verify_token(
    token_input: str,
    side_effect: bool,
    expected_response: bool,
    expected_message: str,
):

    with patch("discogs_client.Client") as mock_client_class:
        mock_user = MagicMock()
        mock_user.username = "test_user"

        mock_client_instance = mock_client_class.return_value
        if side_effect:
            mock_client_instance.identity.side_effect = Exception(
                "401: Invalid consumer token. Please register an app before making requests."
            )
        else:
            mock_client_instance.identity.return_value = mock_user

        token_manager = TokenManager()
        auth_result: AuthenticationResult = token_manager.verify_token(token_input)
        assert auth_result.status is expected_response
        assert auth_result.message == expected_message
