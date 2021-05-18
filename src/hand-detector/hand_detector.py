import cv2
import numpy as np
import time

class HandDetector:
    # Constructor
    def __init__(self):
        self.background = None
        self.background_frames = 30
        self.image_frames = 10
        self.calibrate = True
        self.counter = 0
        self.weight = 0.5
        self.camera = cv2.VideoCapture(0)

    # Function to get a frame from the camera
    def getFrame(self):
        _, frame = self.camera.read()
        frame = cv2.flip(frame, 1)
        img_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        img_grey = cv2.GaussianBlur(img_grey, (7, 7), 0)
        return img_grey

    # Function to compute background by taking average of frames
    def backgroundAvg(self,img):
        if self.background is None:
            self.background = img.copy().astype("float")
            return
        cv2.accumulateWeighted(img, self.background, self.weight)

    def segment(self,img, threshold=25):
        img_diff = cv2.absdiff(self.background.astype("uint8"), img.astype("uint8"))
        img_thresh = cv2.threshold(img_diff, threshold, 255, cv2.THRESH_BINARY)[1]
        (_, contours, _) = cv2.findContours(img_thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) == 0:
            return
        else:
            img_segment = max(contours, key=cv2.contourArea)
            return (img_thresh, img_segment)

    def getHand(self,img_thresh, img_segment):
        convex_hull = cv2.convexHull(img_segment)
        min_y = tuple(convex_hull[convex_hull[:, :, 1].argmin()][0])
        max_y = tuple(convex_hull[convex_hull[:, :, 1].argmax()][0])
        min_x   = tuple(convex_hull[convex_hull[:, :, 0].argmin()][0])
        max_x  = tuple(convex_hull[convex_hull[:, :, 0].argmax()][0])
        hand = img_thresh[min_y[1]:min_y[1]+max_x[0]-min_x[0], min_x[0]:max_x[0]]

        print("Image {} size: {}, {}".format(self.counter, len(img_thresh), len(img_thresh[0])))
        
        if(len(hand) >= 50 and len(hand[0]) >= 50):
            print("Hand size: {}, {}".format(len(hand), len(hand[0])))
            
            hand = cv2.resize(hand,(128,128))
            cv2.imwrite("hand_images/gesture" + str(self.counter) + ".png", hand)
            np.save("hand_frames/gesturef" + str(self.counter),hand)
            self.counter += 1
            return hand
        else:
            return None

    # Function to calibrate background by reading background_frames frames
    def calibrateBackground(self): 
        # Read the first frame 
        self.background = self.getFrame().copy().astype("float")
        for i in range(self.background_frames):
            # Iterate to compute weighted average
            img = self.getFrame()
            cv2.accumulateWeighted(img, self.background, self.weight)

    # Function to get current image by averaging image_frames frames
    def getImage(self):
        # Read first frame
        img_avg = self.getFrame().copy().astype("float")
        for i in range(self.image_frames):
            # Iterate to compute weighted average
            img = self.getFrame()
            cv2.accumulateWeighted(img, img_avg, self.weight)
        return img

    def detectHand(self):
        img_grey = self.getImage()
        hand_segment = self.segment(img_grey)

        start_time = time.time()
        while (time.time() - start_time < 3):
            # Check if any hand detected, else retake frame
            if (hand_segment is None):
                img_grey = self.getImage()
                hand_segment = self.segment(img_grey)
            else :
                (thresholded, segmented) = hand_segment
                hand = self.getHand(thresholded, segmented)
                # Check if hand able to be cropped out, else retake frame
                if (hand is None):
                    img_grey = self.getImage()
                    hand_segment = self.segment(img_grey)
                else :
                    return hand
        return None

    def closeCamera(self):
        self.camera.release()
        cv2.destroyAllWindows()

# h = HandDetector()
# h.calibrateBackground()
# for i in range(0,10):
#    print("fsas")
#    time.sleep(3)
#    h.detectHand()
#    time.sleep(2)
# h.closeCamera()
