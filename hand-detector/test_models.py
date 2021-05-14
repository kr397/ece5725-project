import time 

import model as md
from hand_detector import HandDetector

COMMANDS = ["GO", "BACK", "LEFT", "RIGHT"]

def main():

    total_predictions = 0
    correct_predictions = 0

    detector = HandDetector()
    
    # Get current directory
    filename = raw_input("Enter dataset file: ")
    if filename is '':
        model = md.Model()
    else:
        model = md.Model(filename = filename)
    
    time.sleep(1)
    print("Starting Calibration")
    detector.calibrateBackground()
    print("Calibration Done")
    
    try :
        while(True):
            print("Starting Calibration")
            time.sleep(2)
            #detector.calibrateBackground()
            print("Calibration Done")
            user_input = raw_input("Please enter command: ").upper()
            if (user_input in COMMANDS):
                img_hand = detector.detectHand()
                if(not img_hand is None):
                    model.add(img_hand,user_input)
                    print (user_input)
                    model.train()
            elif (user_input == "LOOK"):
                img_hand = detector.detectHand()
                prediction = model.predict(img_hand)
                if(not prediction == ""):
                    total_predictions += 1
                    print("Prediction: " + str(prediction))
                    user_input = raw_input("Valid? ")
                    if(user_input == "y"):
                        model.enforce(img_hand,prediction)
                        model.train()
                        correct_predictions += 1
                else:
                    print("No Prediction")
            else :
                while(True):
                    img_hand = detector.detectHand()
                    if(img_hand is None):
                        break
                    prediction = model.predict(img_hand)
                    if(not prediction == ""):
                        print("Prediction added: " + str(prediction))
                    else:
                        print("No Prediction")
                        break
                    print("Change Gesture")
                    time.sleep(1)
                
    except KeyboardInterrupt:
        print("Total Predictions: " + str(total_predictions))
        print("Error Rate: " + str(1 - (float(correct_predictions)/total_predictions)))
        model.save('test_dataset.dat')
        print("Model saved")
        detector.closeCamera()
        print("exit")

main()
