import os
import sys, pygame
import time
import subprocess

EAR_ANIMATION = ["dog_images/dog_normal.png","dog_images/dog_ear_up_1.png", "dog_images/dog_ear_up_2.png","dog_images/dog_ear_up_3.png","dog_images/dog_ear_up_4.png","dog_images/dog_ear_up_5.png","dog_images/dog_ear_up_6.png"]   
EYE_ANIMATION = ["dog_images/dog_normal.png","dog_images/dog_look_1.png","dog_images/dog_look_2.png"]

# Set up the environment variables
os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb0')

# Displays the image on the PiTFT screen
def display(img):
    global screen
    dog = pygame.image.load(img)
    dogrect = dog.get_rect()
    screen.fill(background)
    screen.blit(dog, dogrect)
    pygame.display.flip()

# Initialize PyGame
pygame.init()
pygame.mouse.set_visible(False)
size = width, height = 320, 240
background = (97,220,248)
screen = pygame.display.set_mode(size)

# Displaying Initial Frame
display("dog_images/dog_normal.png")


flag = True
while(flag):

    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            flag = False
            sys.exit()

    # Read audio command
    speech_fifo = open('../speechToAnimation.fifo', 'r')
    audio_cmd = speech_fifo.readline()[:-1]
    #audio_cmd = input("Please Enter User Input: ")

    # Case: started recording audio
    if(audio_cmd == "1"):
        # Ear Up
        print("Ear up")
        for frame in EAR_ANIMATION:
            display(frame)
            time.sleep(0.05)
        continue

    # Case: finished recording audio
    elif(audio_cmd == "2"):
        # Ear Down
        print("Ear down")
        for frame in EAR_ANIMATION[::-1]:
                display(frame)
                time.sleep(0.05)
        continue

    # Case: left audio command
    elif(audio_cmd == "LEFT"):
        print("Look left")
        display("dog_images/dog_right.png")
        

    # Case: right audio command
    elif(audio_cmd == "RIGHT"):
        print("Look right")
        display("dog_images/dog_left.png")

    # Case: look audio command
    elif(audio_cmd == "LOOK"):
        # Widen Eyes
        print("Widen eyes")
        for frame in EYE_ANIMATION:
            display(frame)
            time.sleep(0.08)

    # Case: unrecognized audio command
    elif(audio_cmd == "NEW"):
        look = True
        while(True):
            speech_fifo = open('../handToAnimation.fifo', 'r')
            hand_cmd = speech_fifo.readline()[:-1]
            if(hand_cmd == "CHANGE"):
                if(look):
                    display("dog_images/dog_look_2.png")
                else:
                    display("dog_images/dog_normal.png")
                look = not look
            else:
                break

        display("dog_images/dog_normal.png")

    # Case: quit audio command
    elif (audio_cmd == "QUIT"):
        flag = False
        continue

    # Case: renforcement
    elif (audio_cmd == "GOOD"):
        continue

    # Case: other recognized audio commands
    else:
        display("dog_images/dog_normal.png")

    # Bark 
    subprocess.call("aplay audio/dog_bark.wav", shell=True)

    # Wait for motion to finish   
    speech_fifo = open('../speechToAnimation.fifo', 'r')
    speech_cmd = speech_fifo.readline()[:-1] 
    
    #motor_cmd = input("Please Enter User Input: ")
    
    # Animation for look
    if(audio_cmd == "LOOK"):
        # Unwiden Eyes
        print("Unwiden eyes")
        for frame in EYE_ANIMATION[::-1]:
            display(frame)
            time.sleep(0.08)

    # Normal Face after Motion has been completed
    display("dog_images/dog_normal.png")
    

