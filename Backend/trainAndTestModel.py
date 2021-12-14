import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from Backend.Utils import readDataSetFromFile, getTestDataset
import numpy as np
from sklearn.linear_model import LogisticRegression
import pickle

SPOTIFY_CLIENT_ID = '********************************'
SPOTIFY_CLIENT_SECRET = '********************************'

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET))


dangerous_x, dangerous_y = readDataSetFromFile('dangerous')
safe_x, safe_y = readDataSetFromFile('safe')

x = np.concatenate((dangerous_x, safe_x), axis=0)
y = np.concatenate((dangerous_y, safe_y), axis=0)

logisticRegression = LogisticRegression()
logisticRegression.fit(x, y.ravel())

test_x, test_y = getTestDataset(spotify, 'Songs/test_songs')

print("The accuracy score is {0}...".format(logisticRegression.score(test_x, test_y)))

pickle.dump(logisticRegression, open("../model.sav", 'wb'))
