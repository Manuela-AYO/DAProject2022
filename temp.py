"""
This scrpte was created to interact with spotify's 
API using spotipy so genre can be extracted using the track id of 
the songs.
Author: Gloria Isedu

"""

import requests
import time
import pandas as pd
import spotipy
import multiprocessing as mp
import numpy as np
from ratelimit import limits, sleep_and_retry
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import csv

# SPOTIFY_CLIENT_ID = "23e8e96161074036a9c0f0fb1122bd09"
# SPOTIFY_CLIENT_ID = "f80793a6271143edb48a6e87bfb76f75"
SPOTIFY_CLIENT_ID = "8eb0d26b8e7348f58b46cfe969415a41"
# SPOTIFY_CLIENT_SECRET = "7454bf675f3140c3a7abeabdd16e142b"
# SPOTIFY_CLIENT_SECRET = "3edbce5e45e0453abc780a13cae3d2e2"
SPOTIFY_CLIENT_SECRET = "96ca3ef07a4444dc87dacab27ab48cb3"
SPOTIPY_REDIRECT_URI = "http://localhost/"
SCOPE = "playlist-modify-private playlist-modify-pubic"
AUTH_URL = 'https://accounts.spotify.com/api/token'
# base URL of all Spotify API endpoints
BASE_URL = 'https://api.spotify.com/v1/'


def get_access_token():
    """
    get access token for spotify to make a get request by using requests.post
    """
 
    auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': SPOTIFY_CLIENT_ID,
    'client_secret': SPOTIFY_CLIENT_SECRET,
    })

    # convert the response to JSON
    auth_response_data = auth_response.json()


    # save the access token
    access_token = auth_response_data['access_token']

    return access_token


@sleep_and_retry
@limits(calls=150, period=30)
def get_sp_track(access_token,track_ids):
    """
    Gets a track with all its information from spotify api
    Args:
        access_token: access token from spotify
        track_ids: a list of tuples with (song, track_id)
    Returns:
        genres, songs without genres in spotify
    """
    # make get requst header with access token
    print('making header')
    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }
    print('finished making header')

    genres = []
    songs_w_o_genres = []
    count = 0

    # genre_df = pd.DataFrame(track_ids, columns=['songs', 'artists', 'track_ids', 'genres'])
    # genre_df.to_csv('songs_artists_track_ids_and_genres.csv')

    print('start iterating ids')
    # for artist in artists :
    with open("genres.csv", "a") as file :
        csv_writer = csv.writer(file)
        for track_id in track_ids:
            if count % 100 == 0:
                time.sleep(10)
            count += 1
            print("get response")
            response = requests.get(BASE_URL + 'tracks/' + track_id, headers=headers)
            print("finished get response")
            print(response.status_code)
            data = response.json()
            print('Now getting info to check genre....')
            try:
                ids = []
                temp = data['artists']
                # get the ids of the artists
                for item in temp : 
                    ids.append(item["id"])
                print(f"Ids : {ids}")
                genres = []
                for item in ids:
                    response = requests.get(BASE_URL + "artists/" + item, headers=headers)
                    datas = response.json()
                    print(datas)
                    for genre in datas["genres"] :
                        if not genre in genres:
                            genres.append(genre)
                print(f"Genres : {genres}")
                if len(genres) == 0:
                    genres.append("none")
                # store in a file
                csv_writer.writerow(genres)
                
            except KeyError:
                # print(f" {songs} doesn't have a genre in Spotify. Skipped.")
                # song_pair = (songs[i], track_ids[i])
                # songs_w_o_genres.append(song_pair)
                continue
                song_uris.append(song_uri)




df = pd.read_csv('spotify_data.csv')
df = df[16796:]
id = df.id

print("Getting access token.......")
access_token = get_access_token()
print("Finished getting aceess token.......")

print("Getting genres.......")
get_sp_track(access_token=access_token, track_ids=id)
print("Finished getting genres.......")