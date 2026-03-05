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
