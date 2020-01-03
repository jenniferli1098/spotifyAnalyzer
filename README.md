# spotifyAnalyzer
 Web app to browse a user's playlist and to analyze songs and playlists.
 This project relies on Python, Flask, and HTML
### Set up
##### Installation
 Install all necessary packages
```python
pip install flask
pip install spotipy
```
##### Spotify Authorization Key
If on Linux/MacOS
```
export SPOTIPY_CLIENT_ID='your-spotify-client-id'
export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
export SPOTIPY_REDIRECT_URI='your-app-redirect-url'
```
If on Windows
```
SET SPOTIPY_CLIENT_ID='your-spotify-client-id'
SET SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
SET SPOTIPY_REDIRECT_URI='your-app-redirect-url'
```

### Run
In command terminal:
```
flask run
```