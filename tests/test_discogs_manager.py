import pytest
from unittest.mock import patch, MagicMock
from discogs_manager import DiscogsManager


@pytest.fixture
def mock_discogs_client() -> MagicMock:
    return MagicMock()


@pytest.fixture
def mock_discogs_release() -> MagicMock:
    return MagicMock()


def test_get_release_success(
    mock_discogs_client: MagicMock, mock_discogs_release: MagicMock
) -> None:
    mock_client = mock_discogs_client
    mock_client.release.return_value = mock_discogs_release
    release_id = 12345

    with patch("discogs_manager.Client", return_value=mock_client):
        discogs_manager = DiscogsManager()
        result = discogs_manager.get_release(release_id)

    mock_client.release.assert_called_once_with(release_id)
    assert result is mock_discogs_release


def test_get_release_failure(mock_discogs_client: MagicMock) -> None:
    mock_client = mock_discogs_client
    mock_client.release.side_effect = Exception("Failed to fetch release")
    release_id = 54321

    with patch("discogs_manager.Client", return_value=mock_client):
        discogs_manager = DiscogsManager()
        result = discogs_manager.get_release(release_id)

    mock_client.release.assert_called_once_with(release_id)
    assert result is None
