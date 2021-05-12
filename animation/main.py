
import os
import sys, pygame
import time

EAR_ANIMATION = ["dog_images/dog_normal.png","dog_images/dog_ear_up_1.png", "dog_images/dog_ear_up_2.png","dog_images/dog_ear_up_3.png","dog_images/dog_ear_up_4.png","dog_images/dog_ear_up_5.png","dog_images/dog_ear_up_6.png"]   
EYE_ANIMATION = ["dog_images/dog_normal.png","dog_images/dog_look_1.png","dog_images/dog_look_2.png"]

pygame.init()
size = width, height = 320, 240

background = (97,220,248)
screen = pygame.display.set_mode(size)
  
dog = pygame.image.load("dog_images/dog_normal.png")
dogrect = dog.get_rect()
screen.fill(background)
screen.blit(dog, dogrect)
pygame.display.flip()

for frame in EAR_ANIMATION:
        dog = pygame.image.load(frame)
        dogrect = dog.get_rect()
        screen.fill(background)
        screen.blit(dog, dogrect)
        pygame.display.flip()
        time.sleep(0.08)
flag = True

while(True):

    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            flag = False
            sys.exit()

    # speech_fifo = open('speechToAnimation.fifo', 'r')
    # audio_cmd = speech_fifo.readline()[:-1]
    audio_cmd = input("Please Enter User Input: ")
    # Bring down the ear
    for frame in EAR_ANIMATION[::-1]:
            dog = pygame.image.load(frame)
            dogrect = dog.get_rect()
            screen.fill(background)
            screen.blit(dog, dogrect)
            pygame.display.flip()
            time.sleep(0.08)
    
    
    if(audio_cmd == "LEFT"):
        dog = pygame.image.load("dog_images/dog_left.png")
    elif(audio_cmd == "RIGHT"):
        dog = pygame.image.load("dog_images/dog_right.png")
    elif(audio_cmd == "LOOK"):
        for frame in EYE_ANIMATION:
            dog = pygame.image.load(frame)
            dogrect = dog.get_rect()
            screen.fill(background)
            screen.blit(dog, dogrect)
            pygame.display.flip()
            time.sleep(0.08)
    else:
        dog = pygame.image.load("dog_images/dog_normal.png")
    dogrect = dog.get_rect()
    screen.fill(background)
    screen.blit(dog, dogrect)
    pygame.display.flip()

    # Wait for motion to finish    
    motor_cmd = input("Please Enter User Input: ")
    
    if(audio_cmd == "LOOK"):
        for frame in EYE_ANIMATION[::-1]:
            dog = pygame.image.load(frame)
            dogrect = dog.get_rect()
            screen.fill(background)
            screen.blit(dog, dogrect)
            pygame.display.flip()
            time.sleep(0.08)
        
    for frame in EAR_ANIMATION:
        dog = pygame.image.load(frame)
        dogrect = dog.get_rect()
        screen.fill(background)
        screen.blit(dog, dogrect)
        pygame.display.flip()
        time.sleep(0.08)



    



# while 1:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT: sys.exit()

#     screen.fill((169,117,43))
#     pygame.draw.ellipse(screen, (255,255,255), pygame.Rect(90,60,60,120))
#     pygame.draw.ellipse(screen, (255,255,255), pygame.Rect(190,60,60,120))
#     pygame.draw.ellipse(screen, (0,0,0), pygame.Rect(100,100,40,50))
#     pygame.draw.ellipse(screen, (0,0,0), pygame.Rect(210,100,40,50))
#     pygame.draw.circle(screen, (255,255,255), (134,120), 5)
#     pygame.draw.circle(screen, (255,255,255), (244,120), 5)
#     pygame.display.flip()


# dog = pygame.image.load("dog.png")
# dogrect = dog.get_rect()
# dogrect.move(160,120)

# while 1:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT: sys.exit()

#     screen.fill((169,117,43))
#     screen.blit(dog, dogrect)
#     pygame.display.flip()
