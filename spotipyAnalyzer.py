import sys
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify()
username = ""



def get_playlists():
    results = sp.user_playlists(username)
    return results

def get_playlist(id):
    results = sp.user_playlist(username, id, fields="tracks,next")
    return results

def search_track(search_str):
    results = sp.search(q=search_str,type="track", limit=20)
    return results

def get_track_info(id):
    return sp.track(id)


def setUser(u):
    global username
    global sp

    username = u
    
    scope = 'user-library-read'
    #set values in the terminal
    #SET SPOTIPY_CLIENT_ID='
    #SET SPOTIPY_CLIENT_SECRET=
    #SET SPOTIPY_REDIRECT_URI='https://google.com/'
    token = util.prompt_for_user_token(username, scope)
    print("SetUser",username)
    if not token:
        print (f"Can't get token for {username}")
        return False
    
    else:
        sp = spotipy.Spotify(auth=token)
        return True


"""In progress"""
def filterInfoFromPlaylist(results):
    rows = []
    for i in range(0,min(len(results["tracks"]["items"]),100)):
        #track_id = results["tracks"]["items"][i]["track"]["id"]
        #row = filterInfoFromTrack(track_id)
        row = {}
        
        row["id"] = results["tracks"]["items"][i]["track"]["id"]
        row["name"] = results["tracks"]["items"][i]["track"]["name"]
        row["artist"] = results["tracks"]["items"][i]["track"]["artists"][0]["name"]
        row["imgUrl"] = results["tracks"]["items"][i]["track"]['album']['images'][0]['url']
        rows.append(row)
    return rows


def filterInfoFromSearch(results):
    rows = []
    for i in range(0, 20):
        track_id = results["tracks"]["items"][i]["id"]
        row = filterInfoFromTrack(track_id)
        rows.append(row)
    return rows

def filterInfoFromTrack(track_id):
    info = get_track_info(track_id)
    name = info["name"]
    artist = info["album"]["artists"][0]["name"]
    url = info['album']['images'][0]['url']

    # print(name,artist)

    row = {}
    row["artist"] = artist
    row["name"] = name
    row["id"] = track_id
    row["imgUrl"] = url

    return row

# for just one
def get_audio_features(sid):
    features = sp.audio_features(sid)
    return features

# audio features for several tracks
# https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/
def avgAudioFeatures(ids):
    features = sp.audio_features(ids)
    key = ['danceability','energy','key','mode','loudness','speechiness','acousticness','instrumentalness','liveness','valence','tempo']
    results = {}
    
    for i in key:
        results[i] = 0

    for i in key:
        for n in features:
            results[i] += n[i]

    for i in key:
        results[i] = round(results[i] / len(features),2)

    return results


