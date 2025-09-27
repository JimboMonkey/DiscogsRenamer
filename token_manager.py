import keyring
import discogs_client

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
    def verify_token(self, token: str) -> tuple[bool, str]:
        if token:
            try:
                client = discogs_client.Client("DiscogsRenamer/1.0", user_token=token)
                user = client.identity()
                message = f"Authenticated as {user.username}"
                return True, message
            except Exception:
                message = f"Token verification failed"
                return False, message
        else:
            message = f"No token provided"
            return False, message
