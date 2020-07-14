import urllib.parse
from enum import Enum

import requests

import _pickle as pickle
import Levenshtein  # It uses Levenshtein algorithm that computes the minimum number of edits needed to transform one string into the other

# As an option I could use SequenceMatcher that uses Ratcliff/Obershelp algorithm it computes the doubled number of matching characters divided by the total number of characters in the two strings.
# from difflib import SequenceMatcher
# difflib.SequenceMatcher(None, 'hello world', 'hello').ratio()

TRACKS_FILE = 'tracks.pkl'
NOT_MATCHED_FILE = 'tracks_not_matched.pkl'
MATCHED_FILE = 'tracks_matched.pkl'
HEADERS = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': 'Bearer BQAxHPQ4-ZOly5OwxgJm9OibXgY27IhCQwsG-1n49t1tFsyUg5fehwCJY4lt7nEmtxnoMjNJz4RHrUTSR7vy_Pgo_4uveI43qVWmf6zGi58Hwy3qiyxE6QsxZHvX9kmwzRL5yFwixu4hoJyjhZaKXdUfLQ6Kkt4QeYbj5hsQ-0DclTQDH3a-9Ocv5aaRVIlq5yUm-kDvzb9K3oHUZ5Lo6W7QQEu367ISeZlOaR90lx7pRNSpuZoLIKK-dCZNi2ctSOCJn_W9Dr6VHQneVw'}

class Source(Enum):
    API = 1
    FILE = 2

class Track(object):
    def __init__(self, name, artist, album):
        self.name = name
        self.artist = artist
        self.album = album

def request_tracks():
    tracks = []
    batch_url = 'https://api.spotify.com/v1/playlists/0UKmQJJmXskgC40T4gaFtm/tracks?offset=0&limit=100'
    
    print('Getting tracks')
    while batch_url:
        resp = requests.get(url=batch_url, headers=HEADERS)
        json_tracks = resp.json()
        print('{offset} of {total}'.format(offset=json_tracks['offset'], total=json_tracks['total']))
        
        for track in json_tracks['items']:
            tracks.append(Track(
                name = track['track']['name'],
                artist = track['track']['artists'][0]['name'],
                album = track['track']['album']['name']))

        batch_url = json_tracks['next']
    
    return tracks

def dump(item, filename):
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(item, output, protocol=1)

def get_tracks(source, filename = TRACKS_FILE):
    if source == Source.API:
        return request_tracks()
    elif source == Source.FILE:
        with open(filename, "rb") as f:
            return  pickle.load(f)

def url_encode(text):
    return urllib.parse.quote(text)

def search_tracks(tracks):
    matched = []
    not_matched = []
    list_size = len(tracks)
    track_number = 0
    for track in tracks:
        track_number += 1
        match = find_match(track)        
        if match:
            print('{}/{} MATCHED'.format(track_number, list_size))
            matched.append(match)
        else:
            print('{track_number}/{list_size} NO MATCH FOUND for name: {trackName} artist: {trackArtist}'.format(trackName=track.name, trackArtist=track.artist, track_number=track_number, list_size=list_size))
            not_matched.append(track)

    return matched, not_matched

def find_match(track):
    highest_popularity = 0
    highest_ratio_avg = 0
    best_match = None
    search_url = 'https://api.spotify.com/v1/search?q={}&type=track'.format(url_encode(track.name))
    resp = requests.get(url=search_url, headers=HEADERS)
    search_response = resp.json()
    for candidate_track in search_response["tracks"]["items"]:
        track_name_ratio = Levenshtein.ratio(track.name, candidate_track['name'])
        artist_name_ratio = Levenshtein.ratio(track.artist, candidate_track['artists'][0]['name'])
        ratio_avg = (track_name_ratio + artist_name_ratio) / 2
        if ratio_avg > 0.3 and ratio_avg > highest_ratio_avg and candidate_track["popularity"] > highest_popularity:
            highest_popularity = candidate_track["popularity"]
            highest_ratio_avg = ratio_avg
            best_match = candidate_track
    
    return best_match

def get_tracks_uris(matches):
    uris = []
    for match in matches:
        uris.append(match['uri'])

    return uris

def add_to_playlist(playlist, tracks_uris):
    url = 'https://api.spotify.com/v1/playlists/{}/tracks'.format(playlist)
    r = requests.post(url = url, json = {'uris': tracks_uris }, headers = HEADERS) 
    return r.status_code == 201

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]