import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import configparser

class APIConn:
    def __init__(self):
        self.spotify = self._create_spotify_client()

    def _create_spotify_client(self):
        config = configparser.ConfigParser()
        config.read('dashfy/spotifyextract/config.ini')

        # Spotify API credentials
        client_id = config['credentials']['client_id']
        client_secret = config['credentials']['client_secret']

        # Create Spotify API client
        client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        return spotipy.Spotify(client_credentials_manager=client_credentials_manager)
