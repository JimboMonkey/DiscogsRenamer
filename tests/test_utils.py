from discogsrenamer.gui.utils import extract_file_extension

import pytest


@pytest.mark.parametrize(
    "test_path, expected_response",
    [
        ("/test/dir/test_track.mp3", ".mp3"),
        ("/test/dir/test_track.MP3", ".mp3"),
        ("/test/dir/test_README", ""),
    ],
)
def test_extract_file_extension(test_path: str, expected_response: str) -> None:
    file_extension = extract_file_extension(test_path)
    assert file_extension == expected_response
