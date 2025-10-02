from dataclasses import dataclass


@dataclass
class AuthenticationResult:
    status: bool
    username: str | None
    message: str
