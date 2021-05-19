""" 
ECE 5725 Spring 2021
Final Project

PiDog
Aryaa Pai (avp34) and Krithik Ranjan (kr397)

HandDetector class to handle CV for hand gesture detection. 
""" 
# Import global libraries
import cv2
import numpy as np
import time

""" 
HandDetector
Class to encapsulate the computer vision algorithms for hand 
gesture detection.

background: background image array
background_frames: No. of frames over which background averaged
image_frames: No. of frames over which each image averaged
counter: Counter to update and save new images 
weight: Weight for average
camera: OpenCV camera object
"""
class HandDetector:
    """ 
    Constructor
    """
    def __init__(self):
        self.background = None
        self.background_frames = 30
        self.image_frames = 10
        self.counter = 0
        self.weight = 0.5
        self.camera = cv2.VideoCapture(0)

    """ 
    getFrame()
    Function to get a frame from the camera
    """
    def getFrame(self):
        _, frame = self.camera.read()
        frame = cv2.flip(frame, 1)
        img_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        img_grey = cv2.GaussianBlur(img_grey, (7, 7), 0)
        return img_grey

    """ 
    backgroundAvg(img):
    Function to compute background by taking average of frames
    """
    def backgroundAvg(self,img):
        if self.background is None:
            self.background = img.copy().astype("float")
            return
        cv2.accumulateWeighted(img, self.background, self.weight)

    """ 
    segment(img, threshold)
    Function to draw contours around the hand image
    """
    def segment(self,img, threshold=25):
        img_diff = cv2.absdiff(self.background.astype("uint8"), img.astype("uint8"))
        img_thresh = cv2.threshold(img_diff, threshold, 255, cv2.THRESH_BINARY)[1]
        (_, contours, _) = cv2.findContours(img_thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) == 0:
            return
        else:
            img_segment = max(contours, key=cv2.contourArea)
            return (img_thresh, img_segment)

    """ 
    getHand(img, thresh, img_segment)
    Function to use the thresholded and segmented images to obtain the final 
    cropped image of the hand
    """
    def getHand(self,img_thresh, img_segment):
        # Obtain the convex hull around the segmented hand
        convex_hull = cv2.convexHull(img_segment)
        min_y = tuple(convex_hull[convex_hull[:, :, 1].argmin()][0])
        max_y = tuple(convex_hull[convex_hull[:, :, 1].argmax()][0])
        min_x   = tuple(convex_hull[convex_hull[:, :, 0].argmin()][0])
        max_x  = tuple(convex_hull[convex_hull[:, :, 0].argmax()][0])
        hand = img_thresh[min_y[1]:min_y[1]+max_x[0]-min_x[0], min_x[0]:max_x[0]]

        print("Image {} size: {}, {}".format(self.counter, len(img_thresh), len(img_thresh[0])))
        
        # Ensure that the hand detected correctly by comparing with minimum size
        if(len(hand) >= 50 and len(hand[0]) >= 50):
            print("Hand size: {}, {}".format(len(hand), len(hand[0])))
            # Resize the hand to standard image size
            hand = cv2.resize(hand,(128,128))
            cv2.imwrite("hand_images/gesture" + str(self.counter) + ".png", hand)
            np.save("hand_frames/gesturef" + str(self.counter),hand)
            self.counter += 1
            return hand
        else:
            return None

    """ 
    calibrateBackground()
    Function to calibrate background by averaging multiple_frames
    """
    def calibrateBackground(self): 
        # Read the first frame 
        self.background = self.getFrame().copy().astype("float")
        for i in range(self.background_frames):
            # Iterate to compute weighted average
            img = self.getFrame()
            cv2.accumulateWeighted(img, self.background, self.weight)

    """ 
    getImage()
    Function to get current image by averaging image_frames frames
    """
    def getImage(self):
        # Read first frame
        img_avg = self.getFrame().copy().astype("float")
        for i in range(self.image_frames):
            # Iterate to compute weighted average
            img = self.getFrame()
            cv2.accumulateWeighted(img, img_avg, self.weight)
        return img

    """ 
    detectHand()
    Main function (called externally) to take an image and obtain the hand
    gesture
    """ 
    def detectHand(self):
        # Get image from camera
        img_grey = self.getImage()
        hand_segment = self.segment(img_grey)

        # Try obtaining the hand gesture from image, timeout after 3s
        start_time = time.time()
        while (time.time() - start_time < 3):
            # Check if any hand detected, else retake image
            if (hand_segment is None):
                img_grey = self.getImage()
                hand_segment = self.segment(img_grey)
            else :
                # Obtain hand from thresholded and segmented image
                (thresholded, segmented) = hand_segment
                hand = self.getHand(thresholded, segmented)
                # Check if hand able to be cropped out, else retake image
                if (hand is None):
                    img_grey = self.getImage()
                    hand_segment = self.segment(img_grey)
                else :
                    return hand
        return None

    """ 
    closeCamera()
    Function to close camera feed once process finished
    """
    def closeCamera(self):
        self.camera.release()
        cv2.destroyAllWindows()

