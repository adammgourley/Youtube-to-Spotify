# https://spotipy.readthedocs.io/en/2.16.1/#api-reference
import spotipy, pprint
from spotipy.oauth2 import SpotifyOAuth
import os, json
import pickle
import pprint
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


def strip_common_words(title):
    # (Official, Official, (Lyrics, Lyrics, Video, Video), (Music
    common_words = ["(official music video)", "(official lyric video)", "(lyrics)", "(bass boosted)"]
    for i in common_words:
        if i in title:
            title = title.replace(i, "")
    return title
    

def format_title(title):
    try:
        title = title.split(' - ')
        artist = title[0]
        title = title[1]
        return artist, title
    except:
        return "", title


def create_playlist(sp, URIs):
    username = input("Enter Spotify username: ")
    playlist_name = "Test"
    sp.user_playlist_create(username, playlist_name, public=False)
    playlists = sp.current_user_playlists()

    for i in playlists['items']:
        if i['name'] == playlist_name:
            playlist_id = i['id']
    
    add_songs_to_playlist(sp, URIs, playlist_id)


def add_songs_to_playlist(sp, URIs, playlist_id):
    sp.playlist_add_items(playlist_id, URIs)


def get_URIs(sp):
    URIs = []
    songs = ['Jason Aldean - Rearview Town (Official Music Video)', "Jason Aldean - Burnin' It Down", 'J. Cole - MIDDLE CHILD']
    for song in songs:
        song = strip_common_words(song.lower())
        search_results = sp.search(song, type="track", limit=1)

        # Try to change the format of the search in order to get results
        if len(search_results['tracks']['items']) == 0:
            song_artist, song_title = format_title(song)
            search_results = sp.search(q=f'name:{song_title} artist:{song_artist}', type="track", limit=1)

            if len(search_results['tracks']['items']) == 0:
                print(f"----  WARNING: '{song.title()}' not found on Spotify.  ----")
                continue

        # Get name of song, also where we should get the track ID
        top_three = [i['name'] for i in search_results['tracks']['items']]
        URIs.append(search_results['tracks']['items'][0]['uri'])
    
    create_playlist(sp, URIs)

def main():
    get_URIs(sp)


if __name__ == '__main__':
    main()