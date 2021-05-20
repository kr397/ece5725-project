# PiDog
## ECE 5725 Spring 2021 Final Project
### Aryaa Pai **avp34** | Krithik Ranjan **kr397**

PiDog is an intelligent robot dog that can follow voice commands, be trained to recognize hand gestures, and also be taught new voice commands. Please refer to the project website (here: ) for detailed description of the features and implementation of the project. This system has been built on a Raspberry Pi 4B 2GB running the Raspberry Pi OS kernel `5.10.11-v71+`. This document describes the software setup of the Raspberry Pi and steps to run the complete system. 
### Setup
1. The first set of installations is for the Speech Recognition module.
``` 
> sudo apt-get install libasound-dev
> sudo apt-get install portaudio19-dev
> sudo apt-get install python3-pyaudio
> sudo apt-get install flac
> sudo pip3 install SpeechRecognition
```
2. For the Hand Detector module, we have the following set up.
```
> sudo apt-get install python-opencv
> sudo apt-get install python-scipy
> sudo apt-get install ipython
> pip install scikit-learn
> sudo raspi-config
```
In the menu, configure the Raspberry Pi to interface with the camera in 5. Interfacing options --> P1 Camera --> Select Yes to enable camera interface --> Reboot.

3. The animation module uses the `PyGame` library.
```
> pip install pygame
```
4. And the wake-up feature uses ping through `PythonPing`
```
> sudo pip3 install pythonping
```
5. Finally, the Rasbperry Pi needs to interface with the PiTFT. This was done using instructions from the Lab 1 Handout. The Adafruit website features instructions for PiTFT installation for any verson of the Pi.  

### Usage
In order to run the complete system, the `main.sh` script can be run directly which sequentially executes processes for all the modules. 
```
> ./main.sh &
```
This command can also be included in the `./bashrc` to run automatically every time the Raspberry Pi is boot up. 

For detailed output and feedback, the different modules can be executed separately in different terminal sessions. 
```
Terminal 1: > cd animation && sudo python main.py  
Terminal 2: > cd hand-detector && python main.py
Terminal 3: > cd motion && python3 main.py
Terminal 4: > cd speech-recognition && python3 main.py
```
