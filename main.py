# https://spotipy.readthedocs.io/en/2.16.1/#api-reference
import spotipy, pprint
from spotipy.oauth2 import SpotifyOAuth
import os, json

scope = "user-library-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

def strip_common_words(title):
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


def build_playlist(sp, URIs):
    username = input("Enter Spotify username: ")
    #### Need to get playlist name from youtube
    playlist_name = "Test"
    sp.user_playlist_create(username, playlist_name, public=False)
    playlists = sp.current_user_playlists()

    for i in playlists['items']:
        if i['name'] == playlist_name:
            playlist_id = i['id']
    
    sp.playlist_add_items(playlist_id, URIs)


def get_URIs(songs):
    URIs = []
    for song in songs:
        song = strip_common_words(song.lower())
        search_results = sp.search(song, type="track", limit=1)

        # Try to change the format of the search query in order to get results
        if len(search_results['tracks']['items']) == 0:
            song_artist, song_title = format_title(song)
            search_results = sp.search(q=f'name:{song_title} artist:{song_artist}', type="track", limit=1)

            if len(search_results['tracks']['items']) == 0:
                print(f"*****  WARNING: '{song.title()}' not found on Spotify.  *****")
                continue

        print(f"--- '{song.title()}' successfully added to playlist. ---")
        URIs.append(search_results['tracks']['items'][0]['uri'])

    return URIs

def main():
    build_playlist(get_URIs())


if __name__ == '__main__':
    main()