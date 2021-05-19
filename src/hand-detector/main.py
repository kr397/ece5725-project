""" 
ECE 5725 Spring 2021
Final Project

PiDog
Aryaa Pai (avp34) and Krithik Ranjan (kr397)

Main script for the Hand Detector module.
Runs continuously to detect hand gestures from the camera feed
and characterizes them to commands.
""" 

# Import global libraries
import time
import sys 
import subprocess

# Import local modules
import model as md
from hand_detector import HandDetector

def main():
    # Set of commands that the module recognizes paired with actions
    # COMMAND : (Basic?, List of actions)
    # Dictionary updated as new commands added
    commands = {
        "GO" : (True, ["GO"]),
        "BACK" : (True, ["BACK"]),
        "LEFT" : (True, ["LEFT"]),
        "RIGHT" : (True, ["RIGHT"])
    }

    # Initialize the HandDetector object
    detector = HandDetector()

    # Check command line arguments to pre-load a dataset or create new
    if len(sys.argv) == 1:
        model = md.Model()
    else:
        filename = str(sys.argv[1])
        model = md.Model(filename = filename)

    try :
        # Calibrate with current background
        print("Starting Calibration")
        detector.calibrateBackground()
        print("Calibration Done")

        # Initialize status variables
        prev_img_hand = None
        prev_prediction = None
        prev_look = False

        running = True
        while running:
            # Wait for command from speech recognition module
            speech_fifo = open('../speechToHand.fifo', 'r')
            audio_cmd = speech_fifo.readline()[:-1]
            print("Command: " + str(audio_cmd))
            
            # Check if known audio command 
            if(audio_cmd in commands):
                is_basic , motions = commands[audio_cmd]

                if(is_basic):
                    # For basic command, detect hand, add it to the model and train it
                    img_hand = detector.detectHand()
                    if(not img_hand is None):
                        model.add(img_hand,audio_cmd)
                        model.train()

                # Perform the motion sequence associated with command
                for motion_cmd in motions:
                    # Send command to perform motion 
                    subprocess.check_output('echo ' + motion_cmd + ' > ../handToMotion.fifo', shell=True)
                    subprocess.check_output('echo ' + motion_cmd + ' >> ../handToMotion.log', shell=True)
                    # Wait until motion is completed
                    motion_fifo = open('../motionToHand.fifo', 'r')
                    motion_cmd = motion_fifo.readline()[:-1]

                # Calibrate background once motion complete
                detector.calibrateBackground()
                print("Calibration Done")

                # Send complete acknowledgement to speech-recognition
                subprocess.check_output('echo "DONE" > ../handToSpeech.fifo', shell=True)
                subprocess.check_output('echo "DONE" >> ../handToSpeech.log', shell=True)

                prev_look = False
            
            # Reinforcement for previous detection
            elif (audio_cmd == "GOOD" and prev_img_hand is not None and prev_look):
                print("Reinforcement received")
                model.enforce(prev_img_hand,prev_prediction)
                model.train()
                prev_look = False

                # Send complete acknowledgement to speech-recognition
                subprocess.check_output('echo "DONE" > ../handToSpeech.fifo', shell=True)
                subprocess.check_output('echo "DONE" >> ../handToSpeech.log', shell=True)

            # Command to recognize gesture and follow
            elif (audio_cmd == "LOOK"):
                # Detect hand and predict command
                img_hand = detector.detectHand()
                if(not img_hand is None):
                    # Predict the command for the hand detected
                    prediction = model.predict(img_hand)
                    if(not prediction == ""):
                        print("Prediction: " + str(prediction))
                        # Send command to perform motion 
                        subprocess.check_output('echo ' + prediction.upper() + ' > ../handToMotion.fifo', shell=True)
                        subprocess.check_output('echo ' + prediction.upper() + ' >> ../handToMotion.log', shell=True)
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
                        # No prediction 
                        print("No prediction")
                        prev_look = False
                else:
                    # No detection
                    print("Hand not found") 
                    prev_look = False
                # Send complete acknowledgement to speech-recognition
                subprocess.check_output('echo "DONE" > ../handToSpeech.fifo', shell=True)
                subprocess.check_output('echo "DONE" >> ../handToSpeech.log', shell=True)

            # Quit the program   
            elif (audio_cmd == "QUIT") :
                running = False
                # Send quit command to motion
                subprocess.check_output('echo ' + audio_cmd.upper() + ' > ../handToMotion.fifo', shell=True)
                subprocess.check_output('echo ' + audio_cmd.upper() + ' >> ../handToMotion.log', shell=True)
                # Send complete acknowledgement to speech-recognition
                subprocess.check_output('echo "DONE" > ../handToSpeech.fifo', shell=True)
                subprocess.check_output('echo "DONE" >> ../handToSpeech.log', shell=True)
            
            # New voice command detected
            else:
                print("Looking")
                # Loop for detecting sequence of gestures
                flag = True
                motions = []
                while(flag):
                    # Indicate to animation that hand being detected 
                    subprocess.check_output('echo "CHANGE" > ../handToAnimation.fifo', shell=True)
                    subprocess.check_output('echo "CHANGE" >> ../handToAnimation.log', shell=True)
                    # Wait to ensure that hand gesture changed
                    time.sleep(0.5)
                    # Detect gesture
                    img_hand = detector.detectHand()
                    if(img_hand is None):
                        # Stop if no hand found
                        flag = False 
                        break
                    # Predict the command for gesture detected and add
                    prediction = model.predict(img_hand)
                    if(not prediction == ""):
                        print("Prediction added: " + str(prediction))
                        motions.append(prediction)
                        # Break if 5 gestures detected
                        if (len(motions) >= 5):
                            print("Max limit")
                            break
                    else:
                        # No prediction 
                        print("No Prediction")
                        break
                    # Buffer before next gesture detected
                    time.sleep(0.5)
                    print("Change Gesture")
                    # Indicate to animation that hand not being detected 
                    subprocess.check_output('echo "CHANGE" > ../handToAnimation.fifo', shell=True)
                    subprocess.check_output('echo "CHANGE" >> ../handToAnimation.log', shell=True)
                    # Buffer time for change in hand gesture
                    time.sleep(2)
                # Indicate to animation that looking for gestures over
                subprocess.check_output('echo "DONE" > ../handToAnimation.fifo', shell=True)       
                subprocess.check_output('echo "DONE" >> ../handToAnimation.log', shell=True)          
                
                # Perform the detected motion sequence
                if(len(motions) > 0):
                    commands[audio_cmd] = (False,motions)
                    print("New command performed")
                    for motion_cmd in commands[audio_cmd][1]:
                        # Send command to perform motion 
                        subprocess.check_output('echo ' + motion_cmd + ' > ../handToMotion.fifo', shell=True)
                        subprocess.check_output('echo ' + motion_cmd + ' >> ../handToMotion.log', shell=True)
                        # Wait until motion is completed
                        motion_fifo = open('../motionToHand.fifo', 'r')
                        motion_cmd = motion_fifo.readline()[:-1]
                    # Calibrate background once motion complete
                    detector.calibrateBackground()
                    print("Calibration Done")

                    # Send acknowledgement to speech-recognition that new command has been added 
                    subprocess.check_output('echo ' + audio_cmd + ' > ../handToSpeech.fifo', shell=True)
                    subprocess.check_output('echo ' + audio_cmd + ' >> ../handToSpeech.log', shell=True)
                else:
                    # Nack to speech-recognition to not add new command
                    print("New command not mapped")
                    # Send nack to speech recognition                    
                    subprocess.check_output('echo "NONE" > ../handToSpeech.fifo', shell=True)
                    subprocess.check_output('echo "NONE" >> ../handToSpeech.log', shell=True)
                
                prev_look = False


    except KeyboardInterrupt:
        pass
    # Save model
    model.save('knn_dataset.dat')
    print("Model saved")
    detector.closeCamera()
    print("Exit")

main()
