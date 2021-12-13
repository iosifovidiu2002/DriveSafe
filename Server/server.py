import socket
import threading
import struct
from Backend.Utils import playListAnalysis
import spotipy

from Server.LRUcache import LRUCache

SPOTIFY_CLIENT_ID = '0fcd6809776648a39887d531b7c31653'
SPOTIFY_CLIENT_SECRET = 'aa476771bb4b4a96a8f5f648a39e3ef3'

spotify = spotipy.Spotify(client_credentials_manager=spotipy.SpotifyClientCredentials(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET))
dataCache = LRUCache(50)


def worker(client, address):
    try:
        while True:
            result = None
            lenBuff = client.recv(2)
            playlist_id_len = struct.unpack("!H", lenBuff)[0]
            playlist_id = client.recv(playlist_id_len).decode('ascii')
            print(f"Client {address} send {playlist_id}")
            if dataCache.get(playlist_id) is None:
                try:
                    result = playListAnalysis(spotify, playlist_id, "../model.sav")[1]
                    dataCache.set(playlist_id, result)
                except:
                    result = -1
            else:
                result = dataCache.get(playlist_id)
            client.send(struct.pack("!d", result))
            print(f"For playlist id {playlist_id} sent user {address} result {result}")
    except Exception as e:
        print(e)
        print(f"Client {address} disconnected")


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(('192.168.100.4', 6969))
s.listen(5)

while True:
    print("Listening for connections...")
    client_socket, addr = s.accept()
    print(f"Connected client -> {addr}")
    client_thread = threading.Thread(target=worker, args=(client_socket, addr))
    client_thread.start()
