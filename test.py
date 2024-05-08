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

scope = "user-library-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

print(sp.search('BEVERLY', limit=1))
# print(sp.audio_features('https://open.spotify.com/track/03hl08vyDaBCQxQr8X6HXg?si=b9867a04d8994add')[0]['tempo'])
# print(sp.audio_features('https://open.spotify.com/track/03hl08vyDaBCQxQr8X6HXg?si=b9867a04d8994add')[0]['duration_ms'] / 1000)



