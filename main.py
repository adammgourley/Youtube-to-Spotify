# https://spotipy.readthedocs.io/en/2.16.1/#api-reference
import spotipy, pprint
from spotipy.oauth2 import SpotifyOAuth
import os, json
import youtube

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


def get_playlist_id(username, title, offset_count=0):
    details = sp.user_playlists(username, limit=50, offset=offset_count)
    for i in details['items']:
        if i['name'] == title and int(i['tracks']['total']) == 0:
            return i['id']
    offset_count += 50
    get_details(username, offset_count)



def build_playlist(URIs, username, title):
    sp.user_playlist_create(username, title, public=False, description=f"{title} - Created with Youtube to Spotify")
    playlist_id = get_playlist_id(username, title)
    sp.playlist_add_items(playlist_id, URIs)
    print(f"Completed Playlist Transfer!")


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
    url = input("Enter Youtube Playlist URL: ")
    username = input("Enter Spotify username: ")
    yt = youtube.Youtube(url)
    build_playlist(get_URIs(yt.titles), username, yt.playlist_title)


if __name__ == '__main__':
    main()