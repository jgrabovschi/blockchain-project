import socket
import json
from chain import *
from datetime import datetime
from pending import *


PORT = 12345
password = '09cc3fc8ac3cb63aebf89b85a45488ba9a681b822778941e12ec4b963b453e33'

class Message:
    def __init__(self,):
        self.data = ""
        self.signature = ""

class Response:
    def __init__(self, id, accepted):
        self.id = id
        self.accepted = accepted

def server(pending_transactions, host):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        id = 0
        s.bind((host, PORT))
        s.listen(3)
        while True:
            conn, addr = s.accept()
            with conn:
                print("[SERVER] Connected by", addr)
                
                data = conn.recv(1024)
                if not data:
                    break
                print("[SERVER] Received", data)

                #CREATE A MESSAGE OBJECT FROM THE RECEIVED JSON
                message = Message()
                message.data = json.loads(data.decode())['data']
                message.signature = json.loads(data.decode())['signature']
                
                #VERIFY THE SIGNATURE
                signature = sha256((message.data + password).encode()).hexdigest()

                #THE MESSAGE IS PUT IN THE 
                #PENDING TRANSACTIONS AND THE SERVER SENDS THE PENDING TRANSACTION ID 
                #IF THE SIGNATURE IS CORRECT
                #IT SENDS A FLAG OF 1 (ACCEPTED)
                #IF NOT, IT SENDS 0 (REJECTED)
                message.data = 'Client ' + addr[0] + ' - ' + message.data

                transaction = PendingTransaction(message, datetime.now(), id)
                id += 1
                
                pending_transactions.append(transaction)

                if signature == message.signature:
                    response = Response(transaction.id, 1)
                else:
                    response = Response(transaction.id, 0)

                conn.sendall(json.dumps(response.__dict__).encode())

                