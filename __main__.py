#!/usr/bin/env python3
import requests
import json
import time
import lyricsgenius

SPOTIFY_TOKEN = ''
GENIUS_TOKEN = ''
# Get oauth token from https://developer.spotify.com/console/get-users-currently-playing-track

headers_Get = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

def song_data():
    headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + SPOTIFY_TOKEN,
    }

    response = requests.get('https://api.spotify.com/v1/me/player/currently-playing', headers=headers)
    json_data = json.loads(response.text)
    try:
        ARTIST = json_data["item"]["artists"][0]["name"]
        SONG = json_data["item"]["name"]
        return ARTIST, SONG
    except KeyError:
        return None

def get_Song_Lyrics_genius(song, artist):
    genius = lyricsgenius.Genius(GENIUS_TOKEN)
    song = genius.search_song(song, artist)
    return song.lyrics

def main():
    lastSong = None
    while True:
        currentSong = song_data()
        if currentSong:
            if currentSong != lastSong:
                lastSong = currentSong
                print("Song: {}, artist: {}".format(currentSong[0], currentSong[1]))
                print(get_Song_Lyrics_genius(*currentSong))
        else:
            print("Could not get song data")
        time.sleep(10)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Quitting..')
        try:
            quit()
        except SystemExit:
            quit()
