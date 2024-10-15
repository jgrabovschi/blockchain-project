import socket
import json
from hashlib import sha256
import os
import server

# BLOCKCHAIN NETWORK
HOSTS = ["10.0.1.1", "10.0.0.1", "10.0.0.2"] 
PORT_MESSAGES = 12345  # The port used by the network to send messages
PORT_ACCEPT = 12346


# SMART CONTRACT
class Message:
	def __init__(self, data, signature):
		self.data = data
		self.signature = signature
		


def client():
    # GET DATA USAGE AND FORMAT IT		
    command_result = os.popen('df / -h | tail -1 | tr -s " "').read().split(' ')
    time = os.popen('date -R').read()
    data = time.replace('\n', '') + ' - Data Usage: ' + command_result[2] + ' out of ' + command_result[1] + ' on ' + command_result[0]
    print(data)

    accepts = 0
    ids = []

    # SEND DATA TO ALL NODES
    for HOST in HOSTS:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT_MESSAGES))

            signature = sha256((data + '09cc3fc8ac3cb63aebf89b85a45488ba9a681b822778941e12ec4b963b453e33').encode()).hexdigest()
            message = Message(data, signature)
            s.sendall(json.dumps(message.__dict__).encode())

            response = s.recv(1024)

            ids.append(json.loads(response.decode())['id'])

            accepts += json.loads(response.decode())['accepted']
            print

    accepted_percentage = (accepts / len(HOSTS)) * 100

    print('[CLIENT] Accepted by ' + str(accepts) + ' nodes (' + str(accepted_percentage) + '%)')

    # IF THE MAJORITY OF THE NODES ACCEPT THE MESSAGE, SEND THE ID THAT WILL BE USED TO ACCEPT THE TRANSACTION
    if accepted_percentage > 50:
        for HOST in HOSTS:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT_ACCEPT))
                s.sendall(str(ids[HOSTS.index(HOST)]).encode())
         
     


client()
