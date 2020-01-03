import sys
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

#song: 1mVKWLlNKn7lgasPVhxQjD
#playlist: 37i9dQZF1DX70RN3TfWWJh

def print_saved_tracks():
    results = sp.current_user_saved_tracks()
    for item in results['items']:
        track = item['track']
        print (f"{track['name']} {track['artists'][0]['name']}")
    return

def print_playlists():
    results = sp.current_user_playlists()
    for item in results['items']:
        print(f"{item['name']} \n {item['description']}\n")
    # print(results)
    
    get_playlist_tracks(results['items'][0]['id'])
    
    return

def get_playlist_tracks(id):
    results = sp.user_playlist(username, id, fields="tracks,next")
    return results

def get_track_features(id):
    features = sp.audio_features(id)
    #print(features)
    return features

def search_track(search_str):
    result = sp.search(q=search_str,type="track", limit=20)
    for i in range(0,20):
        print(result['tracks']['items'][i]['name'])
    
    

if __name__ == '__main__':
    scope = 'user-library-read'

    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        printf(f"Usage: {sys.argv[0]} username")
        sys.exit()

    #SET SPOTIPY_CLIENT_ID='
    #SET SPOTIPY_CLIENT_SECRET=
    #SET SPOTIPY_REDIRECT_URI='https://google.com/'
    #token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
    token = util.prompt_for_user_token(username, scope)
    print("hi")
    if not token:
        print (f"Can't get token for {username}")
    
    else:
        sp = spotipy.Spotify(auth=token)
        get_playlist_tracks('37i9dQZF1DX70RN3TfWWJh')

