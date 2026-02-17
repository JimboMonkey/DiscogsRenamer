from discogs_client import Client, Release, Track, Artist
from discogs_client.exceptions import HTTPError, AuthorizationError

from token_manager import TokenManager
from gui.release_list_item import ReleaseListItem
from release_data import ReleaseData
from track_data import TrackData


class DiscogsManager:
    def __init__(self):
        token_manager = TokenManager()
        token = token_manager.load_token()
        if token:
            self._client = Client("DiscogsRenamer/1.0", user_token=token)
        else:
            print("No token found. Please set a valid token.")

    def get_release(self, release_id: int) -> Release | None:
        release = None
        try:
            release = self._client.release(release_id)
            # A Release object is always returned even if empty
            # To capture a failed fetch, the exception needs to
            # be forced by calling for non-existent data
            _ = release.title
        except AuthorizationError:
            # Subclass of HTTPError, so must be handled first
            return None
        except HTTPError:
            return None
        return release

    def get_release_artists(self, release: Release) -> str:
        return release.artists_sort

    def get_release_title(self, release: Release) -> str:
        return release.title

    def get_tracklist(self, release: Release) -> list[Track]:
        return list(release.tracklist)

    def get_track_artists(self, track: Track) -> list[Artist]:
        return list(track.artists)

    def format_track_artists(self, track_artists: list[Artist]) -> str:
        track_artists_parts: list[str] = []
        for artist in track_artists:
            # Include join only if it's non-empty
            if artist.join:
                track_artists_parts.append(f"{artist.name} {artist.join}")
            else:
                track_artists_parts.append(f"{artist.name}")
        return " ".join(track_artists_parts)

    def get_track_artists_and_titles(
        self, release: Release, tracklist: list[Track]
    ) -> list[ReleaseListItem]:
        artists_and_titles: list[ReleaseListItem] = []
        release_data = ReleaseData(
            release_artists=self.get_release_artists(release),
            release_title=self.get_release_title(release),
        )
        for track in tracklist:
            track_position = str(track.position)
            if track_position:
                track_title = str(track.title)
                unformatted_track_artists = self.get_track_artists(track)
                formatted_track_artists = self.format_track_artists(
                    unformatted_track_artists
                )

                track_data = TrackData(
                    release=release_data,
                    track_position=track_position,
                    track_artists=formatted_track_artists,
                    track_title=track_title,
                )

                release_list_item = ReleaseListItem(track_data)
                artists_and_titles.append(release_list_item)

        return artists_and_titles

# release
# <Release 654888 'Illclectica'>
# [<Track '1' 'Hole In The Sky'>, <Track '2' 'Scars'>, <Track '3' 'Light Shower'>, <Track '4' "Nicola's Song">, <Track '5' 'Dream Keepa'>, <Track '6' 'Kaos'>, <Track '7' 'No No'>, <Track '8' 'Maybe'>, <Track '9' 'Pacify'>, <Track '10' 'Unsticking'>, <Track '11' 'Tongue Kung Fu'>, <Track '12' 'Wan, Chu'>]
# [<Artist 23863 'Roger Robinson'>]
