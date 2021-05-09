import model 
from hand-detector import HandDetector

def main():

    total_predictions = 0
    correct_predictions = 0

    h = HandDetector()
    try :
        while(True):
            h.calibrateBackground()
            print("Calibration Done")
            user_input = raw_input("Please enter command: ")
            if(user_input == "go" or user_input == "back" or user_input == "left" or user_input == "right"):
                img_hand = h.detectHand()
                model.add(img_hand,user_input)
                model.train()
            else:
                img_hand = h.detectHand()
                prediction = model.predict(img_hand)
                total_predictions += 1
                print("Prediction: " + prediction)
                user_input = raw_input("Valid? ")
                if(user_input == "y"):
                    model.enforce(img_hand,prediction)
                    model.train()
                    correct_predictions += 1

    except KeyboardInterrupt:
        print("Total Predictions: " + str(total_predictions))
        print("Error Rate: " + str(1 - (float(correct_predictions)/total_predictions)))
        h.closeCamera()
        print("exit")