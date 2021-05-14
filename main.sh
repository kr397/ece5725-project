#!/bin/bash
echo "Hi! This is PiDog"
cd animation && sudo python main.py > animation.log &
cd hand-detector && python main.py > hand-detection.log &
cd motion && python3 main.py > motion.log &
cd speech-recognition && python3 main.py > speech-recognition.log &



