import time
import sys 
import subprocess

from knn import knn
from hand_detector import HandDetector

COMMANDS = ["GO", "BACK", "LEFT", "RIGHT"]

def main():
    detector = HandDetector()

    filename = str(sys.argv[0])
    if filename is None:
        model = knn.KNN()
    else:
        model = knn.KNN(data_file = filename)

    try :
        print("Starting Calibration")
        detector.calibrateBackground()
        print("Calibration Done")

        prev_img_hand = None
        prev_prediction = None

        running = True
        while running:
            speech_fifo = open('../speechToHand.fifo', 'r')
            audio_cmd = speech_fifo.readline()[:-1]
            print("Command: " + str(cmd))
            
            # Audio command for training 
            if(audio_cmd in COMMANDS):
                # Detect hand, add it to the model and train it
                img_hand = detector.detectHand()
                model.add(img_hand,audio_cmd)
                model.train()
                # Send command to perform motion 
                subprocess.check_output('echo ' + audio_cmd.upper() + ' > ../handToMotion.fifo', shell=True)
                # Wait until motion is completed
                motion_fifo = open('../motionToHand.fifo', 'r')
                motion_cmd = motion_fifo.readline()[:-1]
                # Calibrate background once motion complete
                detector.calibrateBackground()
                print("Calibration Done")
            # Reinforcement for previous detection
            elif (audio_cmd == "GOOD" and prev_img_hand is not None):
                print("Reinforcement received")
                model.enforce(prev_img_hand,prev_prediction)
                model.train()
            # Command to recognize gesture and follow
            elif (audio_cmd == "HEY"):
                # Detect hand and predict command
                img_hand = detector.detectHand()
                prediction = model.predict(img_hand)
                print("Prediction: " + str(prediction))
                # Send command to perform motion 
                subprocess.check_output('echo ' + audio_cmd.upper() + ' > ../handToMotion.fifo', shell=True)
                # Wait until motion is completed
                motion_fifo = open('../motionToHand.fifo', 'r')
                motion_cmd = motion_fifo.readline()[:-1]
                # Calibrate background once motion complete
                detector.calibrateBackground()
                print("Calibration Done")
                # Save images for reinforcement
                prev_img_hand = img_hand
                prev_prediction = prediction 
            # Quit the program   
            elif (audio_cmd == "QUIT") :
                running = False
                # Send quit command to motion
                subprocess.check_output('echo ' + audio_cmd.upper() + ' > ../handToMotion.fifo', shell=True)
                # Save model
                model.save('knn_dataset.dat')
                print("Model saved")
                break
                
    except KeyboardInterrupt:
        pass
    detector.closeCamera()
    print("Exit")

main()
