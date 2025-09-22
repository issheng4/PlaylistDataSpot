# PlaylistDataSpot

PlaylistDataSpot is a tool designed to provide Spotify users with detailed insights into the music within their playlists. With this app, you can explore the metadata and audio characteristics of each track in your Spotify playlists and even discover what's inside public playlists found through the app's search function.


## Contents
- [Video Demo](#video-demo)
- [Features](#features)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)


## Video Demo
https://youtu.be/BGrnnscAJKU

[![Watch the video demo](https://img.youtube.com/vi/BGrnnscAJKU/0.jpg)](https://youtu.be/BGrnnscAJKU)


## Features

- **Playlist Exploration:** Access data from your Spotify playlists effortlessly, displaying metadata and averages of its tracks' audio features.

- **View Metadata:** Access detailed information about each playlist and track, including track popularity, track name, artist, and more.

- **Audio Feature Data:** Discover audio characteristics of each track in a playlist, such as danceability, positivity, key, BPM and more.

- **Sorting Data:** Sort playlists based on track metadata and track audio features.

- **Public Playlist Search:** Search for public playlists and view their track metadata and track audio features.

- **User-Friendly Interface:** A user-friendly interface makes it simple to navigate and enjoy the app's features.

- **Neat track-detail list of dictionaries:** For developers, all the track details are neatly packed into a list of dictionaries. This app displays them in HTML templates, but you can use them for further development.


## Getting Started

### Installation

1. Clone this repository to your local machine using Git. Open your IDE or terminal and run the following command:

   ```
   git clone https://github.com/issheng4/playlist-data-spot.git
   ```

3. Ensure you have the following dependencies installed:

    - [Python](https://www.python.org/downloads/) (version 3.7 or higher)
    - [Flask](https://pypi.org/project/Flask/)
    - [Flask-Session](https://pypi.org/project/Flask-Session/)
    - [Spotipy](https://pypi.org/project/spotipy/)
    - [python-dotenv](https://pypi.org/project/python-dotenv/)

    You can install these dependencies using `pip`:

    ```
    pip install Flask Flask-Session spotipy python-dotenv
    ```

### Setting Up Your Spotify Developer App

1. **Visit and log into the Spotify for Developers website:** Log into the [Spotify for Developers](https://developer.spotify.com/) website.

2. **Go to user dashboard:** Head to your Dashboard, found in the drop-down menu after clicking your name in the top-right corner.

3. **Create a new app:** Click on the 'Create App' button.

4. **Fill in app details:**
   - **App Name:** Choose a name for your app (e.g. 'PlaylistDataSpot replica').
   - **App Description:** Provide a brief description of your app.
   - **Website:** You can leave this blank or provide your project's website if you have one.
   - **Redirect URIs:** Enter the URI where Spotify will redirect users after authentication. For a local development environment, you can use `http://localhost:5000/callback`, or use your IDE's port followed by `/callback`, or use another URI you plan to use in your project.
   - **Accept Developer Terms:** Review and accept the Spotify Developer Terms of Service.

5. **Finish creating that app:** Click the 'Save' button.

7. **Go to app settings:** Once your app is created, you'll be taken to the app's dashboard. Click on 'Settings' to find your 'Client ID' and 'Client Secret'.

### Setting Up Your Environment Variables

1. **Create the .env file:** Create a `.env` file in your project's root directory. It can simply be called '.env'. Copy and paste the following into the file:

   ```
   CLIENT_ID = ''
   CLIENT_SECRET = ''
   REDIRECT_URI = ''
   ```

2. **Input the client values:** In the quotation marks of 'CLIENT_ID' and 'CLIENT_SECRET', input the Client ID and Client Secret that you found in your app's dashboard on the Spotify for Developers website. Do not share the Client Secret with anyone.

3. **Input the Redirect URI:** In the quotation marks of 'REDIRECT_URI', enter the Redirect URI you used when creating the app on the Spotify for Developers website.

4. **Save the .env file:** Make sure to save the file if it does not save automatically.

### Run the App

1. **Run the app:** In your terminal, run the Flask app:

    ```
    flask run
    ```

3. **Access the app:** Head to the server via the link displayed in your terminal. Note: it gives a warning that this is a development server. At this stage, only those who clone this code can run the app.

You should now be able to use the PlaylistDataSpot app!


## Usage

1. **Exploring Playlists:** Log in with your Spotify account to access your playlists or search for public playlists through the app's search function.

2. **Viewing Track Details:** Click on one of your playlists' names - or search a public playlist - to view detailed information about each track, including metadata and audio features.

3. **Sorting:** Click on table headings to sort data. Explore what the data means in the 'About' page.

### Common Usage Patterns
Here are some common usage patterns:
- DJs and music producers can use the app to identify song keys and BPM for seamless mixes.
- Playlist curators can create playlists based on track popularity and audio features, and learn about their current playlists.
- Software developers interested in audio analysis programming and music can learn about Spotify's audio analysis algorithm from its musical misanalysis.
- Curious listeners can learn more about their tastes.


## Project Structure

- `/templates`: Stores HTML templates used for rendering web pages.
- `/static`: Contains static assets like CSS files and images.
- `helpers.py`: Contains utility function code and constants.
- `app.py`: The main application file.
- `.env`: **You need to create this file.** Configuration settings for the app.
- `user_guide.md`: A markdown version of the 'About' and 'FAQs' pages, provided for easy reference and improved readability without the need to load the app.


## Contributing

Contributions from the community to improve PlaylistDataSpot are welcome and appreciated! See the FAQs section in `user_guide.md` for current known issues that could be fixed.
