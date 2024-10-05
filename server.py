import socket
import json
from chain import *

HOST = "192.168.1.118"
PORT = 12345
password = '09cc3fc8ac3cb63aebf89b85a45488ba9a681b822778941e12ec4b963b453e33'

class Message:
    def __init__(self):
        self.data = ""
        self.signature = ""


def server(blockchain):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                print("Connected by", addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    print("Received", data)

                    message = Message()
                    message.data = json.loads(data.decode())['data']
                    message.signature = json.loads(data.decode())['signature']

                    signature = sha256((message.data + password).encode()).hexdigest()

                    if signature == message.signature:
                        blockchain.add_block(message.data)
                        conn.sendall(b'OK')
                    else:
                        print('>>> INVALID TRANSACTION')
                        conn.sendall(b'INVALID TRANSACTION')

                    