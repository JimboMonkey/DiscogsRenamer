import pytest
from unittest.mock import patch, MagicMock
from discogs_manager import DiscogsManager
from discogs_client import Release, Track, Client


@pytest.fixture
def mock_discogs_client() -> MagicMock:
    return MagicMock(spec_set=Client)


@pytest.fixture
def mock_discogs_release() -> MagicMock:
    mock_release = MagicMock(spec_set=Release)
    mock_release.tracklist = [
        MagicMock(spec_set=Track, title="Track 1"),
        MagicMock(spec_set=Track, title="Track 2"),
        MagicMock(spec_set=Track, title="Track 3"),
    ]
    return mock_release


def test_get_release_success(
    mock_discogs_client: Client, mock_discogs_release: Release
) -> None:
    mock_client = mock_discogs_client
    mock_client.release.return_value = mock_discogs_release
    release_id = 12345

    with patch("discogs_manager.Client", return_value=mock_client):
        discogs_manager = DiscogsManager()
        result = discogs_manager.get_release(release_id)

    mock_client.release.assert_called_once_with(release_id)
    assert result is mock_discogs_release


def test_get_release_failure(mock_discogs_client: Client) -> None:
    mock_client = mock_discogs_client
    mock_client.release.side_effect = Exception("Failed to fetch release")
    release_id = 54321

    with patch("discogs_manager.Client", return_value=mock_client):
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
