import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import cv2
import random
import time
import librosa
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import pygame


pygame.init()
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
y, sr = librosa.load('Zedd - Clarity (feat. Foxes).wav')
my_sound = pygame.mixer.Sound('Zedd - Clarity (feat. Foxes).wav')
tempo, beatframes = librosa.beat.beat_track(y=y, sr=sr)
print('Estimated tempo: {:.2f} beats per minute'.format(tempo))
print(tempo)
my_sound.set_volume(.2)
length = 271
# Library Constants
VisionRunningMode = mp.tasks.vision.RunningMode
DrawingUtil = mp.solutions.drawing_utils

class Gesture:
    def __init__(self, screen_width=1200, screen_height=700):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = 600
        self.y  = 150
        self.list_of_gestures = ["Closed_Fist", "Open_Palm", "Pointing_Up", "Thumb_Down", "Thumb_Up", "Victory", "ILoveYou"]
        self.current_gesture = None
    
    
    def update_gesture(self):
        self.current_gesture = self.list_of_gestures[random.randint(0,6)]

    def gesture_rn(self):
        return self.current_gesture

    def clear_gesture(self):
        self.current_gesture = None

    def draw(self, image):
        cv2.putText(image, self.current_gesture, (self.x, self.y), 1,  
                   5, (0,0,255), 3, cv2.LINE_AA) 

    def remove(self, image):
        cv2.putText(image, None, (self.x, self.y), 1,  
                   1, (0,0,255), 1, cv2.LINE_AA) 



      
class Game:
    def __init__(self):
        # Load game elements
        self.gesture = Gesture()
        self.accuracy = 100
        self.level = 0
        self.score = 0
        self.held_gesture = None
        # self.tempo = tempo


        # Create the hand detector
        base_options = python.BaseOptions(model_asset_path='data/gesture_recognizer.task')
        options = vision.GestureRecognizerOptions(base_options=base_options)
        self.detector = vision.GestureRecognizer.create_from_options(options)
        

        # TODO: Load video
        self.video = cv2.VideoCapture(0)


    
    def draw_gestures(self, image):
        results = self.detector.recognize(image)
        # Get a list of the landmarks
        if results.gestures:
            self.held_gesture = results.gestures[0][0]

    def display_score(self, image):
        cv2.putText(image, str(self.score), (25, 25), 1,  
                   2, (0,0,255), 3, cv2.LINE_AA) 
        
    
    def check_gesture(self, gesture):
        if self.held_gesture and self.held_gesture.category_name == gesture:
            return True
          

    
    def run(self):
        """
        Main game loop. Runs until the 
        user presses "q".
        """    
        # TODO: Modify loop condition
        if self.level == 0:
            starting_time = time.time()
            my_sound.play()
            while self.video.isOpened():
                spawn_time = time.time()
                # Get the current frame
                frame = self.video.read()[1]

                # Convert it to an RGB image
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = cv2.flip(image, 1)

                to_detect = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
                self.display_score(image)
                
                # cv2.putText(image, str(self.score), (50,50), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,color=GREEN,thickness=2)
                self.draw_gestures(to_detect)
                if (spawn_time >= (length / tempo)):
                    self.gesture.draw(image)
                if(self.check_gesture(self.gesture.gesture_rn())):
                    self.gesture.clear_gesture()
                    self.score += 100
                elif (time.time() - starting_time >= 1):
                    self.gesture.update_gesture()
                    starting_time = time.time()

                # Change the color of the frame bacqk
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                cv2.imshow('Gesture Tracking', image)

                # Break the loop if the user presses 'q'
                if (cv2.waitKey(50) & 0xFF == ord('q') or (time.time() - starting_time >= 273)):
                    break
            self.video.release()
            cv2.destroyAllWindows()
            print(self.score)


if __name__ == "__main__":        
    g = Game()
    g.run()