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
import pygame


pygame.init()
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
y, sr = librosa.load('Zedd - Clarity (feat. Foxes).wav')
my_sound = pygame.mixer.Sound('Zedd - Clarity (feat. Foxes).wav')
tempo, beatframes = librosa.beat.beat_track(y=y, sr=sr)
# print('Estimated tempo: {:.2f} beats per minute'.format(tempo))
# print(tempo)


# Library Constants
VisionRunningMode = mp.tasks.vision.RunningMode
DrawingUtil = mp.solutions.drawing_utils

      
class Game:
    def __init__(self):
        # Load game elements
        self.accuracy = 100
        self.level = 0
        self.tempo = tempo


        # Create the hand detector
        base_options = python.BaseOptions(model_asset_path='data/gesture_recognizer.task')
        options = vision.GestureRecognizerOptions(base_options=base_options)
        self.detector = vision.GestureRecognizer.create_from_options(options)
        

        # TODO: Load video
        self.video = cv2.VideoCapture(0)

    
    def draw_landmarks_on_hand(self, image):
        """
        Draws all the landmarks on the hand
        Args:
            image (Image): Image to draw on
            detection_result (HandLandmarkerResult): HandLandmarker detection results
        """
        results = self.detector.recognize(image)
        # Get a list of the landmarks
        if results.gestures:
            top_gesture = results.gestures[0][0]
            print(top_gesture.category_name)
        
    


            

#     # def check_enemy_kill(self, image, detection_result):
#     #     """
#     #     Draws a green circle on the index finger 
#     #     and calls a method to check if we've intercepted
#     #     with the enemy
#     #     Args:
#     #         image (Image): The image to draw on
#     #         detection_result (HandLandmarkerResult): HandLandmarker detection results
#     #     """
#     #     # Get image details
#     #     imageHeight, imageWidth = image.shape[:2]
#     #     # Get a list of the landmarks
#     #     hand_landmarks_list = detection_result.hand_landmarks
        
#     #     # Loop through the detected hands to visualize.
#     #     for idx in range(len(hand_landmarks_list)):
#     #         hand_landmarks = hand_landmarks_list[idx]
#     #         finger = hand_landmarks[HandLandmarkPoints.INDEX_FINGER_TIP.value]
#     #         thumb = hand_landmarks[HandLandmarkPoints.THUMB_TIP.value]
#     #         pixelCoordinates = DrawingUtil._normalized_to_pixel_coordinates(finger.x, finger.y, imageWidth,  imageHeight)
#     #         thumbCoordinates = DrawingUtil._normalized_to_pixel_coordinates(thumb.x, thumb.y, imageWidth,  imageHeight)
#     #         if pixelCoordinates and self.level == 0:
#     #             cv2.circle(image, (pixelCoordinates[0], pixelCoordinates[1]), 25, GREEN, 5)
#     #             cv2.circle(image, (thumbCoordinates[0], thumbCoordinates[1]), 25, RED, 5)
#     #             self.check_enemy_intercept(pixelCoordinates[0], pixelCoordinates[1], self.green_enemy, image)
#     #             self.check_enemy_intercept(thumbCoordinates[0], thumbCoordinates[1], self.red_enemy, image)
#     #         if pixelCoordinates and self.level == 1:
#     #             cv2.circle(image, (pixelCoordinates[0], pixelCoordinates[1]), 25, GREEN, 5)
#     #             for enemy in self.enemies:
#     #                 self.check_enemy_intercept(pixelCoordinates[0], pixelCoordinates[1], enemy, image)
#     #         if pixelCoordinates and thumbCoordinates and self.level == 2:
#     #             cv2.circle(image, (pixelCoordinates[0], pixelCoordinates[1]), 25, GREEN, 5)
#     #             cv2.circle(image, (thumbCoordinates[0], thumbCoordinates[1]), 25, RED, 5)
#     #             if (self.check_enemy_intercept(pixelCoordinates[0], pixelCoordinates[1], self.green_enemy, image)) and (self.check_enemy_intercept(thumbCoordinates[0], thumbCoordinates[1], self.red_enemy, image)):
#     #                 self.green_enemy.respawn()
#     #                 self.red_enemy.respawn()
#     #                 self.score +=1

    
    def run(self):
        """
        Main game loop. Runs until the 
        user presses "q".
        """    
        # TODO: Modify loop condition
        if self.level == 0:
            my_sound.play()
            while self.video.isOpened():
                starting_time = time.time()
                # Get the current frame
                frame = self.video.read()[1]

                # Convert it to an RGB image
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = cv2.flip(image, 1)

                to_detect = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
                


                # cv2.putText(image, str(self.score), (50,50), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,color=GREEN,thickness=2)
                self.draw_landmarks_on_hand(to_detect)


                # Change the color of the frame back
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                cv2.imshow('Gesture Tracking', image)

                # Break the loop if the user presses 'q'
                if (cv2.waitKey(50) & 0xFF == ord('q')):
                    print(time.time() - starting_time)
                    break
            self.video.release()
            cv2.destroyAllWindows()


if __name__ == "__main__":        
    g = Game()
    g.run()