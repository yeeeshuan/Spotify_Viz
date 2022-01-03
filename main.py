

import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='10c87e65ef3646d39329868d5b83bc05',
                                               client_secret='e51482fbfd50429094e5dae4caa1e108',
                                               redirect_uri="https://www.google.com/",
                                               scope="user-read-currently-playing"))

results = sp.currently_playing(market=None)

for x in results:
    print(x)

print(results['item']['name'])

