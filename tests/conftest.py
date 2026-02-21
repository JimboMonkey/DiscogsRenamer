import pytest
from unittest.mock import MagicMock
from discogs_client import Release, Track, Client
from typing import Optional


@pytest.fixture
def mock_discogs_client() -> MagicMock:
    return MagicMock(spec_set=Client)


@pytest.fixture
def mock_discogs_release() -> MagicMock:
    mock_release = MagicMock(spec_set=Release)
    mock_release.artists = ["DJ Mock"]
    mock_release.title = "Mock & Test"
    mock_release.tracklist = [
        MagicMock(spec_set=Track, title="Track 1"),
        MagicMock(spec_set=Track, title="Track 2"),
        MagicMock(spec_set=Track, title="Track 3"),
    ]
    return mock_release


@pytest.fixture(autouse=True)
def mock_keyring(monkeypatch: pytest.MonkeyPatch):
    mock_keyring: dict[tuple[str, str], str] = {}

    def mock_set_password(service_name: str, username: str, password: str) -> None:
        mock_keyring[(service_name, username)] = password

    def mock_get_password(service_name: str, username: str) -> Optional[str]:
        return mock_keyring.get((service_name, username))

    def mock_delete_password(service_name: str, username: str) -> Optional[str]:
        return mock_keyring.pop((service_name, username), None)

    monkeypatch.setattr("keyring.set_password", mock_set_password)
    monkeypatch.setattr("keyring.get_password", mock_get_password)
    monkeypatch.setattr("keyring.delete_password", mock_delete_password)
