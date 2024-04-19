import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import cv2
import random
import time
import librosa
import math
import urllib


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Library Constants
# BaseOptions = mp.tasks.BaseOptions
# HandLandmarker = mp.tasks.vision.HandLandmarker
# HandLandmarkPoints = mp.solutions.hands.HandLandmark
# HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
# VisionRunningMode = mp.tasks.vision.RunningMode
# DrawingUtil = mp.solutions.drawing_utils



# IMAGE_FILENAMES = ['thumbs_down.jpg', 'victory.jpg', 'thumbs_up.jpg', 'pointing_up.jpg']

# for name in IMAGE_FILENAMES:
#   url = f'https://storage.googleapis.com/mediapipe-tasks/gesture_recognizer/{name}'
#   urllib.request.urlretrieve(url, name)

# DESIRED_HEIGHT = 480
# DESIRED_WIDTH = 480

# def resize_and_show(image):
#   h, w = image.shape[:2]
#   if h < w:
#     img = cv2.resize(image, (DESIRED_WIDTH, math.floor(h/(w/DESIRED_WIDTH))))
#   else:
#     img = cv2.resize(image, (math.floor(w/(h/DESIRED_HEIGHT)), DESIRED_HEIGHT))
#   cv2.imshow(img)


# # Preview the images.
# images = {name: cv2.imread(name) for name in IMAGE_FILENAMES}
# for name, image in images.items():
#   print(name)
#   resize_and_show(image)

# STEP 2: Create an GestureRecognizer object.


# Library Constants
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkPoints = mp.solutions.hands.HandLandmark
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode
DrawingUtil = mp.solutions.drawing_utils

      
class Game:
    def __init__(self):
        # Load game elements
        self.level = 0
        self.score = 0
        self.count = 0
        self.die = 15

        # Create the hand detector
        base_options = mp.tasks.BaseOptions(model_asset_path='data/gesture_recognizer.task')
        options = mp.tasks.vision.GestureRecognizerOptions(base_options=base_options)
        self.detector = mp.tasks.vision.GestureRecognizer.create_from_options(options)
        

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
        if results:
            top_gesture = results.gestures[0][0]
            print(top_gesture.category_name)
        
    

    
    def check_enemy_intercept(self, finger_x, finger_y, enemy, image):
        """
        Determines if the finger position overlaps with the 
        enemy's position. Respawns and draws the enemy and 
        increases the score accordingly.
        Args:
            finger_x (float): x-coordinates of index finger
            finger_y (float): y-coordinates of index finger
            image (_type_): The image to draw on
        """
        if (enemy.x <= finger_x + 10 and finger_x - 10 <= enemy.x) and (enemy.y <= finger_y + 10 and finger_y - 10 <= enemy.y):
            if self.level != 2:
                self.score += 1   
                if self.level == 1:
                    self.enemies.pop()
                    self.count -= 1
                if self.level == 0:
                    enemy.respawn()
            else:
                return True
            

    def check_enemy_kill(self, image, detection_result):
        """
        Draws a green circle on the index finger 
        and calls a method to check if we've intercepted
        with the enemy
        Args:
            image (Image): The image to draw on
            detection_result (HandLandmarkerResult): HandLandmarker detection results
        """
        # Get image details
        imageHeight, imageWidth = image.shape[:2]
        # Get a list of the landmarks
        hand_landmarks_list = detection_result.hand_landmarks
        
        # Loop through the detected hands to visualize.
        for idx in range(len(hand_landmarks_list)):
            hand_landmarks = hand_landmarks_list[idx]
            finger = hand_landmarks[HandLandmarkPoints.INDEX_FINGER_TIP.value]
            thumb = hand_landmarks[HandLandmarkPoints.THUMB_TIP.value]
            pixelCoordinates = DrawingUtil._normalized_to_pixel_coordinates(finger.x, finger.y, imageWidth,  imageHeight)
            thumbCoordinates = DrawingUtil._normalized_to_pixel_coordinates(thumb.x, thumb.y, imageWidth,  imageHeight)
            if pixelCoordinates and self.level == 0:
                cv2.circle(image, (pixelCoordinates[0], pixelCoordinates[1]), 25, GREEN, 5)
                cv2.circle(image, (thumbCoordinates[0], thumbCoordinates[1]), 25, RED, 5)
                self.check_enemy_intercept(pixelCoordinates[0], pixelCoordinates[1], self.green_enemy, image)
                self.check_enemy_intercept(thumbCoordinates[0], thumbCoordinates[1], self.red_enemy, image)
            if pixelCoordinates and self.level == 1:
                cv2.circle(image, (pixelCoordinates[0], pixelCoordinates[1]), 25, GREEN, 5)
                for enemy in self.enemies:
                    self.check_enemy_intercept(pixelCoordinates[0], pixelCoordinates[1], enemy, image)
            if pixelCoordinates and thumbCoordinates and self.level == 2:
                cv2.circle(image, (pixelCoordinates[0], pixelCoordinates[1]), 25, GREEN, 5)
                cv2.circle(image, (thumbCoordinates[0], thumbCoordinates[1]), 25, RED, 5)
                if (self.check_enemy_intercept(pixelCoordinates[0], pixelCoordinates[1], self.green_enemy, image)) and (self.check_enemy_intercept(thumbCoordinates[0], thumbCoordinates[1], self.red_enemy, image)):
                    self.green_enemy.respawn()
                    self.red_enemy.respawn()
                    self.score +=1






    
    def run(self):
        """
        Main game loop. Runs until the 
        user presses "q".
        """    
        # TODO: Modify loop condition
        if self.level == 0:
            while self.video.isOpened():
                starting_time = time.time()
                # Get the current frame
                frame = self.video.read()[1]

                # Convert it to an RGB image
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = cv2.flip(image, 1)

                # Convert the image to a readable format and find the hands
                to_detect = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
                results = self.detector.detect(to_detect)

                cv2.putText(image, str(self.score), (50,50), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,color=GREEN,thickness=2)


                # Change the color of the frame back
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                cv2.imshow('Gesture Tracking', image)

                # Break the loop if the user presses 'q'
                if (cv2.waitKey(50) & 0xFF == ord('q')) or self.score == 10:
                    print(time.time() - starting_time)
                    break
            self.video.release()
            cv2.destroyAllWindows()


if __name__ == "__main__":        
    g = Game()
    g.run()