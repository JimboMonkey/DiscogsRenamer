import keyring
import pytest

from keyring.errors import PasswordDeleteError

from constants import APP_NAME, TOKEN_KEY


from token_manager import TokenManager


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
