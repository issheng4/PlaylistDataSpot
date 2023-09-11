import os
from flask import Flask
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)

# Spotify's defined audio features
AUDIO_FEATURES = [
    'tempo', 'valence', 'danceability', 'energy', 'acousticness',
    'instrumentalness', 'liveness', 'loudness',
    'speechiness', 'key', 'mode', 'time_signature', 'duration_ms'
]

# Key map for converting Spotify's numerical categorisation to Western music notation
KEY_MAP = {
    -1: 'No Key',
    0: 'C',
    1: 'C♯',
    2: 'D',
    3: 'E♭',
    4: 'E',
    5: 'F',
    6: 'F♯',
    7: 'G',
    8: 'A♭',
    9: 'A',
    10: 'B♭',
    11: 'B'
}

# Mode map for converting Spotify's numerical categorisation to Western music notation
MODE_MAP = {0: 'Minor', 1: 'Major'}


# Custom exception for when a playlist has no tracks
class NoTracksError(Exception):
    pass


# Utility functions
def create_spotify_oauth():
    """Authorises app via Spotify"""

    return SpotifyOAuth(
        client_id=os.getenv('CLIENT_ID'),
        client_secret=os.getenv('CLIENT_SECRET'),
        redirect_uri=os.getenv('REDIRECT_URI'),
        scope='user-library-read playlist-read-private'
    )


def fetch_all_tracks(sp, playlist_id):
    """Fetches all tracks in a playlist"""

    all_tracks = []
    offset = 0
    limit = 100

    while True:
        # Retrieves tracks in blocks of 100
        tracks = sp.playlist_tracks(
            playlist_id, offset=offset, limit=limit,
            fields='items(track(id, name, artists, popularity, album(images)))'
        )['items']
        if not tracks:
            break
        all_tracks.extend(tracks)
        offset += limit

    return all_tracks


def process_tracks(tracks, sp):
    """Creates dictionaries contatining features of a list of tracks"""

    track_details = []

    for index, track in enumerate(tracks, start=1):
        try:
            # Fetch track metadata
            track_id = track['track']['id']
            image_url = track['track']['album']['images'][0]['url'] if track['track']['album']['images'] else 'imageless'
            track_name = track['track']['name']
            track_artists = [artist['name'] for artist in track['track']['artists']]

            track_popularity = track['track']['popularity']
        except:
            continue

        # Fetch audio feature values of each track
        audio_feature_values = sp.audio_features(tracks=track_id)[0]

        # Skips over podcast episodes and local files
        if audio_feature_values is None:
            continue

        # Create dictionary of audio features of each track
        track_audio_values = {feature: audio_feature_values[feature] for feature in AUDIO_FEATURES}

        # Create dictionary combining the metadata and audio features
        track_details.append({
            'track_id': track_id,
            'index': index,
            'image_url': image_url,
            'name': track_name,
            'artists': track_artists,
            'popularity': track_popularity,
            **track_audio_values
        })

    return track_details


def calculate_average_audio_feature(audio_feature_values, feature_name, total_tracks):
    """Calculates averages of each audio feature for a list of tracks"""

    if total_tracks == 0:
        raise NoTracksError('No tracks available for average calculation')

    # Creates list of tracks with audio features (i.e. not podcast episodes or local files)
    valid_audio_features = [feature[feature_name] for feature in audio_feature_values if feature is not None]

    if valid_audio_features:
        total = sum(valid_audio_features)
        return total / total_tracks
    else:
        return 0
    