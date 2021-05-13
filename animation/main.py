import os
import sys, pygame
import time
import subprocess

EAR_ANIMATION = ["dog_images/dog_normal.png","dog_images/dog_ear_up_1.png", "dog_images/dog_ear_up_2.png","dog_images/dog_ear_up_3.png","dog_images/dog_ear_up_4.png","dog_images/dog_ear_up_5.png","dog_images/dog_ear_up_6.png"]   
EYE_ANIMATION = ["dog_images/dog_normal.png","dog_images/dog_look_1.png","dog_images/dog_look_2.png"]

# Set up the environment variables
os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb0')

# Initialize PyGame
pygame.init()
pygame.mouse.set_visible(False)
size = width, height = 320, 240
background = (97,220,248)
screen = pygame.display.set_mode(size)

# Displaying Initial Frame
dog = pygame.image.load("dog_images/dog_normal.png")
dogrect = dog.get_rect()
screen.fill(background)
screen.blit(dog, dogrect)
pygame.display.flip()


flag = True
while(flag):

    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            flag = False
            sys.exit()

    speech_fifo = open('../speechToAnimation.fifo', 'r')
    audio_cmd = speech_fifo.readline()[:-1]
    #audio_cmd = input("Please Enter User Input: ")

    if(audio_cmd == "1"):
        # Ear Up
        print("Ear up")
        for frame in EAR_ANIMATION:
            dog = pygame.image.load(frame)
            dogrect = dog.get_rect()
            screen.fill(background)
            screen.blit(dog, dogrect)
            pygame.display.flip()
            time.sleep(0.05)
        continue

    elif(audio_cmd == "2"):
        # Ear Down
        print("Ear down")
        for frame in EAR_ANIMATION[::-1]:
                dog = pygame.image.load(frame)
                dogrect = dog.get_rect()
                screen.fill(background)
                screen.blit(dog, dogrect)
                pygame.display.flip()
                time.sleep(0.05)
        continue

    elif(audio_cmd == "LEFT"):
        print("Look left")
        dog = pygame.image.load("dog_images/dog_right.png")

    elif(audio_cmd == "RIGHT"):
        print("Look right")
        dog = pygame.image.load("dog_images/dog_left.png")

    elif(audio_cmd == "LOOK"):
        # Widen Eyes
        print("Widen eyes")
        for frame in EYE_ANIMATION:
            dog = pygame.image.load(frame)
            dogrect = dog.get_rect()
            screen.fill(background)
            screen.blit(dog, dogrect)
            pygame.display.flip()
            time.sleep(0.08)
    elif (audio_cmd == "QUIT"):
        flag = False
        continue
    elif (audio_cmd == "GOOD"):
        continue
    else:
        dog = pygame.image.load("dog_images/dog_normal.png")

    # Display Motion Frame
    dogrect = dog.get_rect()
    screen.fill(background)
    screen.blit(dog, dogrect)
    pygame.display.flip()

    # Bark 
    subprocess.check_output("aplay audio/dog_bark.wav", shell=True)

    # Wait For Motion To Finish   
    motor_fifo = open('../motionToAnimation.fifo', 'r')
    motor_cmd = motor_fifo.readline()[:-1] 
    #motor_cmd = input("Please Enter User Input: ")
    
    if(audio_cmd == "LOOK"):
        # Unwiden Eyes
        print("Unwiden eyes")
        for frame in EYE_ANIMATION[::-1]:
            dog = pygame.image.load(frame)
            dogrect = dog.get_rect()
            screen.fill(background)
            screen.blit(dog, dogrect)
            pygame.display.flip()
            time.sleep(0.08)

    # Normal Face after Motion has been completed
    dog = pygame.image.load("dog_images/dog_normal.png")
    dogrect = dog.get_rect()
    screen.fill(background)
    screen.blit(dog, dogrect)
    pygame.display.flip()
    

