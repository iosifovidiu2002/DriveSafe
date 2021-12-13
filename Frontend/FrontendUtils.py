import struct


def ServerPlaylistAnalysis(server, playlist_id):
    server.send(struct.pack("!H", len(playlist_id)))
    server.send(playlist_id.encode('ascii'))
    result = struct.unpack("!d", server.recv(8))[0]

    return result


def searchResultsPlaylists(spotify, search, limit):
    results = []
    for playlist in spotify.search(search, limit=limit, type="playlist")['playlists']['items']:
        if not playlist['collaborative']:
            image_url = 'https://community.spotify.com/t5/image/serverpage/image-id/55829iC2AD64ADB887E2A5/image-size/large?v=v2&px=999'
            if len(playlist['images']) != 0:
                image_url = playlist['images'][0]['url']
            results.append(
                [playlist['name'], playlist['owner']['display_name'], playlist['tracks']['total'], playlist['id'], image_url])
    return results
