import time
from flask import Flask, request, redirect, render_template, session
from flask_session import Session
import spotipy
from dotenv import load_dotenv

from helpers import (
    AUDIO_FEATURES,
    KEY_MAP,
    MODE_MAP,
    NoTracksError,
    create_spotify_oauth,
    fetch_all_tracks,
    process_tracks,
    calculate_average_audio_feature,
)

load_dotenv()

# Configure application
app = Flask(__name__)
TOKEN_INFO = 'token_info'

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Custom Jinja filters
@app.template_filter('is_number')
def is_number(value):
    return isinstance(value, (int, float))

@app.template_filter('key_to_name')
def key_to_name(key_value):
    return KEY_MAP.get(key_value, 'Unknown Key')

@app.template_filter('mode_to_name')
def mode_to_name(mode_value):
    return MODE_MAP.get(mode_value, 'Unknown Mode')

@app.template_filter('duration_format')
def duration_format(milliseconds):
    total_seconds = int(milliseconds) // 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f'{minutes}:{seconds:02d}'


def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        return redirect('/login')
    now = int(time.time())

    is_expired = token_info['expires_at'] - now < 60
    if is_expired:
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info


@app.route('/')
def login():
    """Log user in"""

    # Redirect user to Spotify authorisation URL
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@app.route('/callback')
def callback():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect('/playlists')


@app.route('/playlists')
def playlists():
    """Display user's playlists"""

    # Retrieve token
    try:
        token_info = get_token()
    except spotipy.SpotifyException:
        print('Please log in')
        return redirect('/')
    except:
        return 'Non-token-related issues are afoot. Please contact issheng4 on GitHub.'

    # Initialise Spotipy variables
    sp = spotipy.Spotify(auth=token_info['access_token'])
    playlists = sp.current_user_playlists(limit=50)['items']

    playlist_details = []
    for index, playlist in enumerate(playlists, start=1):
        try:
            # Fetch playlist metadata
            playlist_id = playlist['id']
            name = playlist['name']
            image_url = playlist['images'][0]['url'] if playlist['images'] else 'imageless'
            total_tracks = playlist['tracks']['total']
            visibility = 'Public' if playlist['public'] else 'Private'

            # Fetch the tracks for the current playlist
            tracks = sp.playlist_tracks(playlist_id, fields='items(track(id, name, popularity))')['items']

            # Maxmimum total tracks for spotipy calls is 100
            total_tracks_upper_bound = len(tracks)

            # Extract track IDs
            track_ids = [track['track']['id'] for track in tracks]

        except:
            pass

        # Get audio features for the track IDs
        try:
            audio_feature_values = sp.audio_features(tracks=track_ids)
        except:
            pass

        # Calculate the average popularity of the playlist's tracks
        if total_tracks > 0:
            popularity_total = sum(track['track']['popularity'] for track in tracks if track['track'])
            average_popularity = popularity_total / total_tracks_upper_bound
        else:
            average_popularity = -99.999

        # Calculate the average values for each audio feature
        try:
            average_audio_values = {
                feature: calculate_average_audio_feature(audio_feature_values, feature, total_tracks_upper_bound)
                for feature in AUDIO_FEATURES
            }
        except NoTracksError:
            # Handle the case when there are no tracks
            average_audio_values = {feature: -99.999 for feature in AUDIO_FEATURES}

        # Construct list of dictionaries of playlist details
        playlist_details.append({
            'playlist_id': playlist_id,
            'index': index,
            'name': name,
            'image_url': image_url,
            'total_tracks': total_tracks,
            'visibility': visibility,
            'popularity': average_popularity,
            **average_audio_values
        })

    # Sort the playlist details by average value
    sort_value = request.args.get('sort', 'index') # Get the sort value from the query parameter
    reverse_bool = sort_value not in ['index', 'name', 'image_url']
    playlist_details.sort(key=lambda x: x[sort_value], reverse=reverse_bool)

    return render_template('playlists.html', playlist_details=playlist_details)


@app.route('/playlists/')
def playlist_with_slash():
    return redirect('/playlists')

@app.route('/playlists/<playlist_id>')
def get_playlist_details(playlist_id):
    """Display metadata and audio feature data of a playlist's tracks"""
    # Retrieve token
    try:
        token_info = get_token()
    except spotipy.SpotifyException:
        print('Please log in')
        return redirect('/')
    except:
        return 'Non-token-related issues are afoot. Please contact issheng4 on GitHub.'

    # Initialise Spotipy variables
    sp = spotipy.Spotify(auth=token_info['access_token'])
    playlist = sp.playlist(playlist_id)

    # Fetch playlist metadata
    playlist_name = playlist['name']
    playlist_image_url = playlist['images'][0]['url']
    playlist_description = playlist['description']
    playlist_creator = playlist['owner']['display_name']
    total_tracks = playlist['tracks']['total']

    # Fetch all tracks and organise their features
    all_tracks = fetch_all_tracks(sp, playlist_id)
    track_details = process_tracks(all_tracks, sp)

    # Sort the playlist details by average value
    sort_value = request.args.get('sort', 'index')  # Get the sort value from the query parameter
    reverse_bool = sort_value not in ['index', 'name', 'artists', 'key']
    track_details.sort(key=lambda x: x[sort_value], reverse=reverse_bool)

    return render_template(
        'playlist_details.html',
        playlist_name=playlist_name,
        playlist_image_url=playlist_image_url,
        playlist_description=playlist_description,
        playlist_creator=playlist_creator,
        total_tracks=total_tracks,
        track_details=track_details
    )


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/faqs')
def faqs():
    return render_template('faqs.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    """Search for any Spotify playlist"""

    # Retrieve token
    try:
        token_info = get_token()
    except spotipy.SpotifyException:
        print('Please log in')
        return redirect('/')
    except:
        return 'Non-token-related issues are afoot. Please contact issheng4 on GitHub.'

    sp = spotipy.Spotify(auth=token_info['access_token'])

    if request.method == 'POST':
        # Fetch playlist name from user's input
        playlist_name = request.form.get('playlist_name')

        # Search for the playlist by name
        results = sp.search(q=playlist_name, type='playlist')
        playlists = results['playlists']['items']

        if playlists:
            # Get the ID of the first matching playlist
            playlist_id = playlists[0]['id']
            return redirect(f'/playlists/{playlist_id}')

        else:
            return render_template('search.html')

    else:
        return render_template('search.html')



@app.route('/logout')
def logout():
    """Log out user via Spotify's own logout page"""
    return render_template('logout.html')


if __name__ == '__main__':
    app.run()
