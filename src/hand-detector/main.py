import time
import sys 
import subprocess

import model as md
from hand_detector import HandDetector

COMMANDS = ["GO", "BACK", "LEFT", "RIGHT"]

def main():
    detector = HandDetector()

    if len(sys.argv) == 1:
        model = md.Model()
    else:
        filename = str(sys.argv[1])
        model = md.Model(filename = filename)

    try :
        print("Starting Calibration")
        detector.calibrateBackground()
        print("Calibration Done")

        prev_img_hand = None
        prev_prediction = None
        prev_look = False

        running = True
        while running:
            speech_fifo = open('../speechToHand.fifo', 'r')
            audio_cmd = speech_fifo.readline()[:-1]
            print("Command: " + str(audio_cmd))
            
            # Audio command for training 
            if(audio_cmd in COMMANDS):
                # Detect hand, add it to the model and train it
                img_hand = detector.detectHand()
                if(not img_hand is None):
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
            elif (audio_cmd == "GOOD" and prev_img_hand is not None and prev_look):
                print("Reinforcement received")
                model.enforce(prev_img_hand,prev_prediction)
                model.train()
                prev_look = False
            # Command to recognize gesture and follow
            elif (audio_cmd == "LOOK"):
                # Detect hand and predict command
                img_hand = detector.detectHand()
                if(not img_hand is None):
                    prediction = model.predict(img_hand)
                    if(not prediction == ""):
                        print("Prediction: " + str(prediction))
                        # Send command to perform motion 
                        subprocess.check_output('echo ' + prediction[0].upper() + ' > ../handToMotion.fifo', shell=True)
                        # Wait until motion is completed
                        motion_fifo = open('../motionToHand.fifo', 'r')
                        motion_cmd = motion_fifo.readline()[:-1]
                        # Calibrate background once motion complete
                        detector.calibrateBackground()
                        print("Calibration Done")
                        # Save images for reinforcement
                        prev_img_hand = img_hand
                        prev_prediction = prediction 
                        prev_look = True
                    else:
                        print("Hand Not Found")
                        # Send command to indicate hand not found
                        subprocess.check_output('echo "NONE" > ../handToMotion.fifo', shell=True)
                        # Wait for ack from motion
                        motion_fifo = open('../motionToHand.fifo', 'r')
                        motion_cmd = motion_fifo.readline()[:-1]
                        continue
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
