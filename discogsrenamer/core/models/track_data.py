from dataclasses import dataclass

from discogsrenamer.core.models.release_data import ReleaseData


@dataclass
class TrackData:
    release: ReleaseData
    track_position: str
    track_artists: str
    track_title: str

    def original_filename(self) -> str:
        if self.track_artists:
            return f"{self.track_artists} - {self.track_title}"
        return self.track_title
