from discogs_client import Client, Release, Track

from token_manager import TokenManager


class DiscogsManager:
    def __init__(self):
        token_manager = TokenManager()
        token = token_manager.load_token()
        if token:
            self._client = Client("DiscogsRenamer/1.0", user_token=token)
        else:
            print("No token found. Please set a valid token.")

    def get_release(self, release_id: int) -> Release | None:
        try:
            release = self._client.release(release_id)
            return release
        except Exception as e:
            print(f"Failed to fetch release {release_id}: {e}")
            return None

    def get_tracklist(self, release: Release) -> list[Track]:
        return release.tracklist

    def get_track_titles(tracklist: list[Track]) -> list[str]:
        return [track.title for track in tracklist]


# release
# <Release 654888 'Illclectica'>
# [<Track '1' 'Hole In The Sky'>, <Track '2' 'Scars'>, <Track '3' 'Light Shower'>, <Track '4' "Nicola's Song">, <Track '5' 'Dream Keepa'>, <Track '6' 'Kaos'>, <Track '7' 'No No'>, <Track '8' 'Maybe'>, <Track '9' 'Pacify'>, <Track '10' 'Unsticking'>, <Track '11' 'Tongue Kung Fu'>, <Track '12' 'Wan, Chu'>]
# [<Artist 23863 'Roger Robinson'>]
