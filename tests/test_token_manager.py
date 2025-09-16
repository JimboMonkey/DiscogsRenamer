import keyring
import pytest
import os

from keyring.errors import PasswordDeleteError

from constants import APP_NAME, TOKEN_KEY
from token_manager import TokenManager

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
