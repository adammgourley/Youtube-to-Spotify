import os, json
import pickle
import pprint
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

credentials = None

if os.path.exists("token.pickle"):
    print("Loading Credentials from File...")
    with open("token.pickle", "rb") as token:
        credentials = pickle.load(token)

# If there are no valid credentials available, then either refresh the token or log in.
if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
        print('Refreshing Access Token...')
        credentials.refresh(Request())
    else:
        print('Fetching New Tokens...')
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secrets.json',
            scopes=[
                'https://www.googleapis.com/auth/youtube.readonly'],
            )

        flow.run_local_server(port=8080, prompt='consent',
                              authorization_prompt_message='')
        credentials = flow.credentials

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as f:
            print('Saving Credentials for Future Use...')
            pickle.dump(credentials, f)


API_KEY = os.getenv("API_KEY")
youtube = build("youtube", "v3", developerKey=API_KEY)
playlist_url = input("Playlist URL: ").split("?list=")
# playlist_url = ["local", "PLZlS83zsu3vwjGHfosK9Qxz34Yn28yUwv"]

all_videos = []
def get_playlist(url, next_page=None):
    request = youtube.playlistItems().list(part=["snippet"], playlistId=playlist_url[-1], pageToken=next_page)
    response = request.execute()

    for video in response['items']:
        all_videos.append(video['snippet']['title'])

    if "nextPageToken" in response:
        get_playlist(url, response['nextPageToken'])

get_playlist(playlist_url)

print(all_videos)