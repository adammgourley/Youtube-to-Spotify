# Youtube to Spotify - Playlist Transfer


## Getting Started

#### First things first...
- Set your Youtube playlist's privacy to "Unlisted" or "Public." The script will fail otherwise.

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

## Running These Scripts

First off, you need to set your environment variables. (If running on Windows, "export" should be changed to "set")

    $ export API_KEY=[YOUR GOOGLE API KEY]
    $ export SPOTIPY_CLIENT_ID=[YOUR SPOTIFY CLIENT ID]
    $ export SPOTIPY_CLIENT_SECRET=[YOUR SPOTIFY CLIENT SECRET KEY]
    $ export SPOTIPY_REDIRECT_URI=[REDIRECT URI SET ON SPOTIFY API DASHBOARD]

After that, run the script. You will need to input the Youtube playlist URL and your Spotify username.

    $ python3 main.py

The first time the application is run, it will open a browser to the redirect URI set on your Spotify API dashboard. Copy and paste the whole URL from the browser into the terminal.