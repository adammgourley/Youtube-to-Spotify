import os, json, pickle, pprint
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

### TODO:
###   - Do all formatting of titles in 'youtube.py' instead of 'main.py'

class Youtube:
    def __init__(self, url):
        self.API_KEY = os.getenv('API_KEY') if os.getenv('API_KEY') is not None else input('Enter Youtube API Key: ')
        self.credentials = None
        self.set_credentials()
        self.youtube = build("youtube", "v3", developerKey=self.API_KEY)
        self.url = url.split("?list=")
        self.titles = []
        self.playlist_title = ""
        self.get_titles(self.url)
        self.get_playlist_title(self.url)

    def set_credentials(self):
        if os.path.exists('token.pickle'):
            print('Loading Credentials from File')
            with open('token.pickle', 'rb') as token:
                self.credentials = pickle.load(token)

        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                print('Refreshing Access Token...')
                self.credentials.refresh(Request())
            else:
                print('Fetching New Tokens...')
                flow = InstalledAppFlow.from_client_secrets_file(
                    'client_secrets.json',
                    scopes=['https://www.googleapis.com/auth/youtube.readonly'],
                )
                flow.run_local_server(port=8080, prompt='consent', authorization_prompt_message='')
                self.credentials = flow.credentials

                # Save for the next run
                with open('token.pickle', 'wb') as f:
                    print('Saving Credentials for Future Use...')
                    pickle.dump(self.credentials, f)
    
    def get_titles(self, url, next_page=None):
        request = self.youtube.playlistItems().list(part=['snippet'], playlistId=url[-1], pageToken=next_page)
        response = request.execute()

        for video in response['items']:
            self.titles.append(video['snippet']['title'])
        
        if "nextPageToken" in response:
            self.get_titles(url, response['nextPageToken'])

    def get_playlist_title(self, url):
        playlist_title_request = self.youtube.playlists().list(part='snippet', id=url[-1])
        title_response = playlist_title_request.execute()
        self.playlist_title = title_response['items'][0]['snippet']['title']