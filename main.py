from cmu_112_graphics import *
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import math
import time

# user authorization to access spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='10c87e65ef3646d39329868d5b83bc05',
                                               client_secret='e51482fbfd50429094e5dae4caa1e108',
                                               redirect_uri="https://www.google.com/",
                                               scope="user-read-currently-playing"))


# selects the information from audio file used in shape
def create_shape(song):
    store = dict()
    count = 0
    temp = sp.audio_analysis(song)
    total = temp['track']['duration']
    title = sp.track(song)['name']

    for x in temp['segments']:
        store[count] = list()
        store[count].append(x['confidence'])
        store[count].append(x['duration'])
        store[count].append(abs(x['loudness_max']))
        store[count].append(abs(x['loudness_start']))
        store[count].append(x['start'])
        count += 1
    return store, total, title


# appstarted
def appStarted(app):
    print("search a song")
    temp = input()
    results = sp.search(q=str(temp), limit=10)
    store = dict()
    for idx, track in enumerate(results['tracks']['items']):
        store[idx] = [track['id']]
        store[idx].append(track['artists'][0]['name'])
        print(idx, track['name'], track['artists'][0]['name'])

    print("select a song ")
    song = input()

    app.song = store[int(song)][0]
    app.name = store[int(song)][1]

    print('name a color palette (blue, green, purple')
    color = input()

    if color.upper() == "BLUE":
        app.color = ['midnight blue', 'navy', 'blue', 'RoyalBlue', 'DodgerBlue', 'SteelBlue', 'DeepSkyBlue', 'cyan',
                     'turquoise', 'cornflower blue']
    if color.upper() == "GREEN":
        app.color = ['dark green', 'dark olive green', 'dark sea green', 'sea green', 'pale green', 'spring green',
                     'lawn green', 'lime green', 'yellow green', 'olive drab']
    if color.upper() == "PURPLE":
        app.color = ['DarkOrchid1', 'DarkOrchid2', "DarkOrchid3", "DarkOrchid4", "purple1", "purple2", "purple3",
                     "purple4", "MediumPurple1", "MediumPurple2", "MediumPurple3", "MediumPurple4"]
    app.start_time = time.perf_counter()


# creates the fractal pattern
def drawTree(app, canvas, level, x, y, size, angle, color, width, d):
    rad = angle * math.pi / 180
    delta = d * math.pi / 180
    currx, curry = x + size * math.cos(rad), y - size * math.sin(rad)
    right = (currx + size * math.cos(rad - delta), curry - size * math.sin(rad - delta))
    left = (currx + size * math.cos(rad + delta), curry - size * math.sin(rad + delta))
    if level == 0:
        canvas.create_line(x, y, currx, curry, width=width, fill=color)
        canvas.create_line(currx, curry, right[0], right[1], width=width, fill=color)
        canvas.create_line(currx, curry, left[0], left[1], width=width, fill=color)
    else:
        drawTree(app, canvas, level - 1, x, y, size, angle, color, width, d)
        drawTree(app, canvas, level - 1, right[0], right[1], size / 2, angle, color, width / 1.5, d)
        drawTree(app, canvas, level - 1, left[0], left[1], size / 2, angle, color, width / 1.5, d)


# determines the depth of fractal
def drawLevel(app, canvas, level, angle, color, width, d):
    size = 100
    x, y = app.width // 2, app.height // 2
    drawTree(app, canvas, level, x, y, size, angle, color, width, d)


#redrawAll
def redrawAll(app, canvas):
    song = app.song
    temp = create_shape(song)
    shape = temp[0]
    duration = temp[1]
    title = temp[2]
    angle = 0
    #canvas.create_text(100, 100, text=f'Timer: {time.perf_counter() - app.start_time}', fill='black')
    #canvas.create_text(900, 100, text=f'{title} by {app.name}', fill='black')
    for x in shape:
        #if (time.perf_counter() - app.start_time) // 1 >= shape[x][4] // 1:
        angle += (shape[x][1] / duration) * 360
        level = (shape[x][0] * 10) // 2
        color = app.color[int(shape[x][2] // 1) % 10]
        width = 1
        d = shape[x][3]
        drawLevel(app, canvas, level, angle, color, width, d)


runApp(width=1000, height=1000)

