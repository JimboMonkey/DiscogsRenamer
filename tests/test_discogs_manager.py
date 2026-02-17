import pytest
from unittest.mock import patch
from discogs_manager import DiscogsManager
from discogs_client import Release, Track, Client
from discogs_client.exceptions import HTTPError


# DiscogsManager won't attempt to make a client if
# there is no token, so patch a mock_token to every test
@pytest.fixture(autouse=True)
def patch_load_token():
    with patch("discogs_manager.TokenManager.load_token", return_value="mock_token"):
        yield


def test_get_release_success(
    mock_discogs_client: Client, mock_discogs_release: Release
) -> None:
    mock_client = mock_discogs_client
    mock_client.release.return_value = mock_discogs_release
    release_id = 12345

    with (patch("discogs_manager.Client", return_value=mock_client),):
        discogs_manager = DiscogsManager()
        result = discogs_manager.get_release(release_id)

    mock_client.release.assert_called_once_with(release_id)
    assert result is mock_discogs_release


def test_get_release_failure(mock_discogs_client: Client) -> None:
    mock_client = mock_discogs_client
    mock_client.release.side_effect = HTTPError("Failed to fetch release", 404)
    release_id = 54321

    with (patch("discogs_manager.Client", return_value=mock_client),):
        discogs_manager = DiscogsManager()
        result = discogs_manager.get_release(release_id)

    mock_client.release.assert_called_once_with(release_id)
    assert result is None


def test_get_tracklist(mock_discogs_release: Release) -> None:
    discogs_manager = DiscogsManager()
    tracklist = discogs_manager.get_tracklist(mock_discogs_release)

    assert isinstance(tracklist, list)
    assert len(tracklist) == 3
    assert all(isinstance(track, Track) for track in tracklist)


def test_get_track_titles(mock_discogs_release: Release) -> None:
    discogs_manager = DiscogsManager()
    tracklist = discogs_manager.get_tracklist(mock_discogs_release)
    track_titles = discogs_manager.get_track_titles(tracklist)
    assert isinstance(track_titles, list)
    assert len(track_titles) == 3
    assert track_titles == ["Track 1", "Track 2", "Track 3"]


def test_get_release_artists(mock_discogs_release: Release) -> None:
    discogs_manager = DiscogsManager()
    artists = discogs_manager.get_release_artists(mock_discogs_release)
    assert artists == "DJ Mock"


def test_get_release_title(mock_discogs_release: Release) -> None:
    discogs_manager = DiscogsManager()
    title = discogs_manager.get_release_title(mock_discogs_release)
    assert title == "Mock & Test"
