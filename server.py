import socket
import json
from chain import *
from datetime import datetime
from pending import *

HOST = "10.0.1.1"
PORT = 12345
password = '09cc3fc8ac3cb63aebf89b85a45488ba9a681b822778941e12ec4b963b453e33'

class Message:
    def __init__(self,):
        self.data = ""
        self.signature = ""

def server(pending_transactions):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        id = 0
        s.bind((HOST, PORT))
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

                #IF THE SIGNATURE IS RIGHT THE MESSAGE IS PUT IN THE 
                #PENDING TRANSACTIONS AND THE SERVER SENDS THE PENDING TRANSACTION ID (>=0)
                #IF NOT, IT SENDS -1
                if signature == message.signature:
                    message.data = 'Client ' + addr[0] + ' - ' + message.data

                    transaction = PendingTransaction(message, datetime.now(), id)
                    id += 1
                    
                    pending_transactions.append(transaction)
                    conn.sendall(str(transaction.id).encode())
                else:
                    print('>>> INVALID TRANSACTION')
                    conn.sendall("-1".encode())

                    