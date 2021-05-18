from pythonping import ping
import subprocess

ping_response = ping('192.168.1.68')
flag = True
while (flag):
    for resp in ping_response:
        flag = resp.success
    ping_response = ping('192.168.1.68')

print("User's home!")
# subprocess.check_output('echo "YAY" > pingToSpeech.fifo', shell=True)
