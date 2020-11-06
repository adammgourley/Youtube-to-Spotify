import os, json, pickle, pprint
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

class Youtube:
    def __init__(self):
        self.API_KEY = os.getenv('API_KEY') if os.getenv('API_KEY') is not None else input('Enter Youtube API Key: ')
        self.credentials = None
        self.set_credentials()
        self.youtube = build("youtube", "v3", developerKey=self.API_KEY)
        self.url = input("Enter Youtube Playlist URL: ").split("?list=")
        self.all_videos = []
        self.get_playlist(self.url)

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
    
    def get_playlist(self, url, next_page=None):
        request = self.youtube.playlistItems().list(part=['snippet'], playlistId=url[-1], pageToken=next_page)
        response = request.execute()

        for video in response['items']:
            self.all_videos.append(video['snippet']['title'])
        
        if "nextPageToken" in response:
            self.get_playlist(url, response['nextPageToken'])
    
    

yt = Youtube()
print(yt.all_videos)