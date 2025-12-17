from dataclasses import is_dataclass, asdict
import os

from track_data import TrackData


def to_dict(obj) -> dict:
    """Flatten dataclass objects into a dict, including nested release."""
    if is_dataclass(obj):
        d = asdict(obj)
        # If there's a nested release, merge its fields into the top-level dict
        if "release" in d and isinstance(d["release"], dict):
            release_fields = d.pop("release")
            d.update(release_fields)
        return d


def format_filename(template: str, track_data: TrackData, track_num: str) -> str:
    flat_dict = to_dict(track_data)
    flat_dict["track_num"] = track_num
    safe = (
        template.replace("%release_track_num", "{track_position}")
        .replace("%artist", "{track_artists}")
        .replace("%title", "{track_title}")
        .replace("%num", "{track_num}")
    )
    return safe.format(**flat_dict)


def extract_file_extension(file_path: str) -> str:
    _, file_extension = os.path.splitext(file_path)
    return file_extension
