# Youtube to Spotify - Playlist Transfer


## Getting Started

#### First things first...
- Set your Youtube playlist to "Unlisted" or "Public." The script will fail otherwise.

#### Install (or upgrade) required dependencies
    $ pip3 install google-api-python-client
    $ pip3 install google-auth-oauthlib google-auth-httplib2
    $ pip3 install spotipy

#### API Credentials You Will Need
- Google Dev API Key
- Google OAuth 2.0 Client JSON File (Store this file as 'client_secrets.json' in this directory)
- Spotify Client ID
- Spotify Client Secret
- Spotify Redirect URI (Set this on Spotify API Dashboard I used "http://example.com")

#### Setting Environment Variables (Use "set" on Windows)
    $ export API_KEY=[YOUR GOOGLE API KEY]
    $ export SPOTIFY_CLIENT_ID=[YOUR SPOTIFY CLIENT ID]
    $ export SPOTIFY_CLIENT_SECRET=[YOUR SPOTIFY CLIENT SECRET KEY]
    $ export SPOTIFY_REDIRECT_URI=[REDIRECT URI SET ON SPOTIFY API DASHBOARD]



## Running These Scripts
The script you need to run is "main.py"

    $ python3 main.py

The program will ask for the Youtube playlist URL and your Spotify username. Keep in mind, the playlist created on your spotify account will be titled the same as the playlist on Youtube. This may cause songs to be added to other playlists you have that are titled the same. In order to avoid this, make sure there are no playlists saved to your Spotify with the same name as the Youtube playlist being converted.
