import pickle

import numpy as np
import socket

global featureNumber
global features
features = ['danceability', 'energy', 'loudness']
featureNumber = len(features)


def url_to_uri(url):
    uri = url.split('/')[-1].split('?')[0]
    return uri


def get_songs_from_playlist(spotify, playlist):
    song_ids = []
    songs = spotify.playlist_tracks(playlist)
    songs = songs['items']
    for s in songs:
        # DO NOT MODIFY THIS, LOOKED AT A LOT OF SCRABBLED JSON TO FIGURE IT OUT
        song_ids.append(s['track']['uri'].split(':')[2])
    return song_ids


def get_songs_from_files(spotify, files):
    songs = []
    for file in files:
        f = open(file, "r")
        for line in f.readlines():
            songs += get_songs_from_playlist(spotify, url_to_uri(line))
    return songs


def scrape_songs_from_playlists(spotify, playlist_file, status_message=False):
    songs = get_songs_from_files(spotify, [playlist_file])
    songs = set(songs)
    if status_message:
        print("Fetched {0} songs from {1} file.".format(len(songs), playlist_file))
    song_file = playlist_file.split("_")[0] + "_songs"
    f = open("Songs/" + song_file.split("/")[-1], "w")
    i = 0
    for s in songs:
        if i != len(songs) - 1:
            f.write(s + "\n")
        else:
            f.write(s)
        i += 1
    f.close()
    return len(songs)


def songIdsFromFiles(files):
    songIds = []
    for file in files:
        f = open(file)
        for line in f.readlines():
            if line.strip() != '':
                songIds.append(line.strip())
        print("Done with file ", file, "...")
    return list(set(songIds))


def songIdToSongData(spotify, song_ids):
    songs = []
    for id in song_ids:
        song = spotify.audio_features(id)
        if song is not None:
            songs += song
        else:
            print("We got none!")
    return songs


def getDataset(song_list, status):
    x = np.zeros((len(song_list), featureNumber), dtype=np.float32)
    if status == 1:
        y = np.ones((len(song_list), 1), dtype=np.float32)
    elif status == 0:
        y = np.zeros((len(song_list), 1), dtype=np.float32)
    else:
        raise Exception("Invalid status!")

    for i in range(len(song_list)):
        global features
        if song_list[i] is not None:
            for j in range(len(features)):
                x[i][j] = song_list[i][features[j]]
            y[i][0] = status
    print("Dataset ready for status ", status)
    return x, y


def getTestDataset(spotify, filename):
    global featureNumber
    with open(filename, 'r') as f:
        count = int(f.readline())
        test_x = np.zeros((count, featureNumber), dtype=np.float32)
        test_y = np.zeros((count, 1), dtype=np.float32)
        for i in range(count):
            args = f.readline().split()
            song = url_to_uri(args[0])
            status = float(args[1])
            song_features = getDataForPrediction(spotify, song)
            for j in range(len(song_features)):
                test_x[i][j] = song_features[j]
            test_y[i][0] = status

        return test_x, test_y


def writeDataSetToFile(dset, filename):
    x, y = dset
    datasetLength, featureNo = x.shape
    f = open(filename, 'w')
    f.write(str(datasetLength))
    f.write(" ")
    f.write(str(featureNo))
    f.write("\n")
    for i in range(0, len(x)):
        for j in range(0, featureNo):
            f.write(str(x[i][j]))
            f.write(" ")
        f.write(str(y[i][0]))
        if i != len(x) - 1:
            f.write("\n")


def readDataSetFromFile(filename):
    global featureNumber
    with open(filename, 'r') as f:
        line = f.readline().split()
        datasetLength, featureNo = int(line[0]), int(line[1])
        x = np.zeros((datasetLength, featureNo), dtype=np.float32)
        y = np.zeros((datasetLength, 1), dtype=np.float32)
        i = 0
        for line in f.readlines():
            features = line.split()
            for j in range(featureNumber):
                x[i][j] = float(features[j])
            y[i][0] = float(features[featureNumber])
            i += 1
    return x, y


# def getDataForPrediction(spotify, song):
#     global features
#     song_features = spotify.audio_features(song)[0]
#     return [song_features[f] for f in features]

def getDataForPrediction(spotify, songs):
    global features
    offset = 0
    raw_features = []
    songs = list(songs)
    while offset + 51 < len(songs):
        raw_features.extend(spotify.audio_features(filter(lambda x: x is not None, songs[offset:offset + 51])))
        offset += 51
    raw_features.extend(spotify.audio_features(filter(lambda x: x is not None, songs[offset:])))
    print(len(raw_features))
    songs_features = []
    for song_feature in raw_features:
        result = []
        for f in features:
            result.append(song_feature[f])
        songs_features.append(result)
    return songs_features


def millisecondsToMinSecFormat(m):
    sec = str((int(m * 0.001) % 60))
    if int(m * 0.001) % 60 < 10:
        sec = "0" + sec
    return str(int((int(m) * 0.001) // 60)) + ":" + sec


def searchResultsSongs(spotify, search, limit):
    results = []
    for track in spotify.search(search, limit=limit, type='tracks,albums')['tracks']['items']:
        artists = [x['name'] for x in track['artists']]
        results.append([track['name'], ", ".join(artists), track['duration_ms'], track['id']])
    return results


def searchResultsPlaylists(spotify, search, limit):
    results = []
    for playlist in spotify.search(search, limit=limit, type="playlist")['playlists']['items']:
        if not playlist['collaborative']:
            results.append(
                [playlist['name'], playlist['owner']['display_name'], playlist['tracks']['total'], playlist['id']])
    return results


def getIdsFromPlaylist(spotify, playlist):
    offset = 0
    fetched = 0
    to_fetch = 100
    ids = set()
    total = spotify.playlist_items(playlist)['total']
    while fetched < total:
        for item in spotify.playlist_items(playlist, offset=fetched, limit=to_fetch)['items']:
            if item['track'] is not None:
                ids.add(item['track']['id'])
            fetched += 1
    return ids


def filterOutGarbage(songs):
    return songs


def playListAnalysis(spotify, playlist, model_location):
    ids = getIdsFromPlaylist(spotify, playlist)
    model = pickle.load(open(model_location, 'rb'))
    danger_index = 0
    danger_proba = 0
    song_features = getDataForPrediction(spotify, ids)
    song_features = filterOutGarbage(song_features)
    for feature in song_features:
        prediction = model.predict(np.array([feature]))[0]
        proba_prediction = model.predict_proba(np.array([feature]))[0][1]
        danger_index += prediction
        danger_proba += proba_prediction
    return danger_index / len(ids), danger_proba / len(ids)
