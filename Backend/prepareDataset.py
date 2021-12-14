import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from Backend.Utils import scrape_songs_from_playlists, songIdsFromFiles, songIdToSongData, getDataset, writeDataSetToFile, readDataSetFromFile


SPOTIFY_CLIENT_ID = '********************************'
SPOTIFY_CLIENT_SECRET = '********************************'

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET))

dangerous_x, dangerous_y = getDataset(songIdToSongData(spotify, songIdsFromFiles(["Songs/metal_songs", "Songs/techno_songs", "Songs/rnb_songs", "Songs/hiphop_songs","Songs/unsafeclassical_songs","Songs/hard.country_songs"])), 1)
safe_x, safe_y = getDataset(songIdToSongData(spotify, songIdsFromFiles(["Songs/blues_songs", "Songs/soul_songs", "Songs/softhiphop_songs", "Songs/softrock_songs","Songs/safeclassical_songs","Songs/safe_songs","Songs/soft.country_songs"])), 0)

writeDataSetToFile((dangerous_x, dangerous_y), 'dangerous')
writeDataSetToFile((safe_x, safe_y), 'safe')
