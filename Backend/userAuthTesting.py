import spotipy
import os
from spotipy.oauth2 import SpotifyOAuth

os.environ["SPOTIPY_CLIENT_ID"] = '0fcd6809776648a39887d531b7c31653'
os.environ["SPOTIPY_CLIENT_SECRET"] = 'aa476771bb4b4a96a8f5f648a39e3ef3'
os.environ["SPOTIPY_REDIRECT_URI"] = 'http://localhost:8080'

scope = "user-library-read"

SPOTIFY_CLIENT_ID = '0fcd6809776648a39887d531b7c31653'
SPOTIFY_CLIENT_SECRET = 'aa476771bb4b4a96a8f5f648a39e3ef3'

sp = spotipy.Spotify(
            client_credentials_manager=spotipy.SpotifyClientCredentials(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET))
# https://open.spotify.com/playlist/7z5f1KNRDcUhs9lLoLhWqh?si=d97787c6fca649a8
playlist = sp.playlist("37i9dQZF1DX82uM9F4qTjN")
print(playlist)