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


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
y, sr = librosa.load('Zedd - Clarity (feat. Foxes).wav')
tempo, beatframes = librosa.beat.beat_track(y=y, sr=sr)
print('Estimated tempo: {:.2f} beats per minute'.format(tempo))
print(tempo)
# beat_times = librosa.frames_to_time(beatframes, sr=sr)
# print(beat_times)



