import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import cv2
import random
import time
import librosa
import math
import urllib
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import matplotlib.pyplot as plt
import numpy
import pygame
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import json
import webbrowser

scope = "user-modify-playback-state"


# username = 'Your user name'
clientID = 'ae89b1fc601b47138392ffda25c14219'
clientSecret = 'd9c7c51e504f4f4296ccbb73e5b90d69'
redirect_uri = 'http://google.com/callback/'

oauth_object = spotipy.SpotifyOAuth(clientID, clientSecret, redirect_uri) 
token_dict = oauth_object.get_access_token() 
token = token_dict['access_token'] 
# spotifyObject = spotipy.Spotify(auth=token) 
sp = spotipy.Spotify(auth=token, auth_manager=SpotifyOAuth(scope=scope))
# user_name = spotifyObject.current_user() 

# To print the response in readable format. 
# print(json.dumps(user_name, sort_keys=True, indent=4)) 

while True: 
	# print("Welcome to the project, " + user_name['display_name']) 
	print("0 - Exit the console") 
	print("1 - Search for a Song") 
	user_input = int(input("Enter Your Choice: ")) 
	if user_input == 1: 
		search_song = input("Enter the song name: ") 
		results = sp.search(search_song, 1, 0, "track") 
		songs_dict = results['tracks'] 
		song_items = songs_dict['items'] 
		song = song_items[0]['uri']
		print(song)
		# webbrowser.open(song)
		# link = sp.search(inp, limit=1)['tracks']['items'][0]['external_urls']['spotify']
		# print(sp.audio_features(link)[0]['tempo'])
		# print(sp.audio_features(link)[0]['duration_ms'] / 1000)
		# sp.start_playback()
		sp.start_playback(context_uri=song)
		print('Song has opened in your browser.') 
	elif user_input == 0: 
		print("Good Bye, Have a great day!") 
		break
	else: 
		print("Please enter valid user-input.") 



# inp = input('Enter a song title: ')




