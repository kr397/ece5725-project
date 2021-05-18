""" 
ECE 5725 Spring 2021
Final Project

PiDog
Aryaa Pai (avp34) and Krithik Ranjan (kr397)

Helper script for the Speech Recognition module to perform Ping
Continuously pings the user's IP address to see if they are home, 
ends if found.
""" 
from pythonping import ping

# Ping user's IP continuously
ping_response = ping('192.168.1.68')
flag = True
while (flag):
    for resp in ping_response:
        flag = resp.success
    ping_response = ping('192.168.1.68')

# Successful ping
print("User's home!")