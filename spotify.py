import json
from dotenv import load_dotenv
import os
import base64
from requests import post, get

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_headers(token):
    return {
        "Authorization": f"Bearer {token}",
    }   

def search_for_artist(token, artist_name):
    url = f"https://api.spotify.com/v1/search"
    headers = get_auth_headers(token)
    query = f"?q={artist_name}&type=artist&limit=10"
    url = url + query
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artist found")
        return
    # print(json_result[0]["name"])
    return json_result[0]

def get_songs_of_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?Country=IN?limit=15"
    headers = get_auth_headers(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    # print(json_result["tracks"])
    return json_result["tracks"]

def get_artist_albums(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums/?limit=50&include_groups=album"
    headers = get_auth_headers(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    # print(json_result["items"])
    return json_result["items"]

def get_album_songs(token, album_id):
    url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
    headers = get_auth_headers(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    # print(json_result["items"])
    return json_result["items"]

def get_artist_songs_by_album(token, singer_name):
    result = search_for_artist(token, singer_name)
    artist_id = result["id"]
    albums = get_artist_albums(token, artist_id)
    for index, album in enumerate(albums):
        print(index+1,": ",album["name"])
        songs = get_album_songs(token, album['id'])
        for inx,song in enumerate(songs):
            print("\t",inx+1,": ",song["name"])

# token = get_token()
# get_artist_songs_by_album(token, "Arijit Singh")


