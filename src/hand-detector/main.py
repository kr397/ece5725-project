import time
import sys 
import subprocess

import model as md
from hand_detector import HandDetector

def main():

    commands = {
        "GO" : (True, ["GO"]),
        "BACK" : (True, ["BACK"]),
        "LEFT" : (True, ["LEFT"]),
        "RIGHT" : (True, ["RIGHT"])
    }

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
            
            # Basic audio command found
            if(audio_cmd in commands):
                is_basic , motions = commands[audio_cmd]

                if(is_basic):
                    # Detect hand, add it to the model and train it
                    img_hand = detector.detectHand()
                    if(not img_hand is None):
                        model.add(img_hand,audio_cmd)
                        model.train()

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
                        print("No prediction")
                        prev_look = False
                        # # Send command to indicate hand not found
                        # subprocess.check_output('echo "NONE" > ../handToMotion.fifo', shell=True)
                        # subprocess.check_output('echo "NONE" >> ../handToMotion.log', shell=True)
                        # Wait for ack from motion
                        # motion_fifo = open('../motionToHand.fifo', 'r')
                        # motion_cmd = motion_fifo.readline()[:-1]
                else:
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
            
            else:
                print("Looking")
                # Loop for more gestures 
                flag = True
                motions = []
                while(flag):
                    # Indicate to animation that hand being detected 
                    subprocess.check_output('echo "CHANGE" > ../handToAnimation.fifo', shell=True)
                    subprocess.check_output('echo "CHANGE" >> ../handToAnimation.log', shell=True)
                    time.sleep(0.5)
                    img_hand = detector.detectHand()
                    if(img_hand is None):
                        flag = False 
                        break
                    prediction = model.predict(img_hand)
                    if(not prediction == ""):
                        print("Prediction added: " + str(prediction))
                        motions.append(prediction)
                        # Break if 5 gestures detected
                        if (len(motions) >= 5):
                            print("Max limit")
                            break
                    else:
                        print("No Prediction")
                        break
                    time.sleep(0.5)
                    print("Change Gesture")
                    # Indicate to animation that hand not being detected 
                    subprocess.check_output('echo "CHANGE" > ../handToAnimation.fifo', shell=True)
                    subprocess.check_output('echo "CHANGE" >> ../handToAnimation.log', shell=True)

                    time.sleep(2)
                # Indicate to animation that looking for gestures over
                subprocess.check_output('echo "DONE" > ../handToAnimation.fifo', shell=True)       
                subprocess.check_output('echo "DONE" >> ../handToAnimation.log', shell=True)          
                
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
                    # Send dummy command to motion
                    # subprocess.check_output('echo "NONE" > ../handToMotion.fifo', shell=True)
                    # subprocess.check_output('echo "NONE" > ../handToMotion.log', shell=True)
                    # # Wait for acknowledgement from motion
                    # motion_fifo = open('../motionToHand.fifo', 'r')
                    # motion_cmd = motion_fifo.readline()[:-1]
                    
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
