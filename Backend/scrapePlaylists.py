import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from Backend.Utils import scrape_songs_from_playlists, songIdsFromFiles, songIdToSongData, getDataset, writeDataSetToFile, readDataSetFromFile
import numpy as np
from sklearn.linear_model import LogisticRegression
import pickle

SPOTIFY_CLIENT_ID = '********************************'
SPOTIFY_CLIENT_SECRET = '********************************'

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET))

no_dangerous_songs = 0
no_dangerous_songs += scrape_songs_from_playlists(spotify, "Playlists/metal_playlists", status_message=True)
no_dangerous_songs += scrape_songs_from_playlists(spotify, "Playlists/techno_playlists", status_message=True)
no_dangerous_songs += scrape_songs_from_playlists(spotify, "Playlists/rnb_playlists", status_message=True)
no_dangerous_songs += scrape_songs_from_playlists(spotify, "Playlists/hiphop_playlists", status_message=True)
no_dangerous_songs += scrape_songs_from_playlists(spotify, "Playlists/unsafeclassical_playlists", status_message=True)
no_dangerous_songs += scrape_songs_from_playlists(spotify, "Playlists/hard.country_playlists")
print("Fetched {0} \"dangerous\" songs".format(no_dangerous_songs))

no_safe_songs = 0
no_safe_songs += scrape_songs_from_playlists(spotify, "Playlists/blues_playlists", status_message=True)
no_safe_songs += scrape_songs_from_playlists(spotify, "Playlists/soul_playlists", status_message=True)
no_safe_songs += scrape_songs_from_playlists(spotify, "Playlists/softhiphop_playlists", status_message=True)
no_safe_songs += scrape_songs_from_playlists(spotify, "Playlists/softrock_playlists", status_message=True)
no_safe_songs += scrape_songs_from_playlists(spotify, "Playlists/safeclassical_playlists", status_message=True)
no_safe_songs += scrape_songs_from_playlists(spotify, "Playlists/safe_compilation", status_message=True)
no_safe_songs += scrape_songs_from_playlists(spotify, "Playlists/soft.country_playlists",status_message=True)
print("Fetched {0} \"safe\" songs".format(no_safe_songs))