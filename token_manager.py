import keyring
import discogs_client
from auth_data_class import AuthenticationResult

from constants import APP_NAME, TOKEN_KEY


class TokenManager:
    # Fetch the token from the keyring
    def load_token(self) -> str | None:
        return keyring.get_password(APP_NAME, TOKEN_KEY)

    # Save the token to the keyring
    def save_token(self, token: str) -> None:
        keyring.set_password(APP_NAME, TOKEN_KEY, token)

    # Verify a token by checking if it authenticates
    # Return a message to display on the token entry dialog
    def verify_token(self, token: str | None) -> AuthenticationResult:
        def result(
            state: bool, username: str | None, message: str
        ) -> AuthenticationResult:
            return AuthenticationResult(state, username, message)

        if not token:
            return result(False, None, "No token provided")

        try:
            client = discogs_client.Client("DiscogsRenamer/1.0", user_token=token)
            user = client.identity()
            username = str(user.username)
            return result(
                True,
                username,
                f"Authenticated as {username}",
            )
        except Exception:
            return result(
                False,
                None,
                "Token verification failed",
            )
