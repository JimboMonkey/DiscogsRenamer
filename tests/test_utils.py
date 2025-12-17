from gui.utils import extract_file_extension


def test_extract_file_extension():
    file_extension = extract_file_extension("/test/dir/test_track.mp3")
    assert file_extension == ".mp3"
