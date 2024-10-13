import socket
import json
from chain import *

PORT_SYNCHRONIZE = 12347  # The port used by the network to synchronize the blockchain
IP_ADDRESS = "10.0.1.1"
HOSTS = ["10.0.1.1"]  # The IP addresses of the blockchain network


def server(blockchain):
    #ALSO CREATES A SOCKET TO SEND THE BLOCKCHAIN FOR THE SERVERS TO SYNCHRONIZE
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((IP_ADDRESS, PORT_SYNCHRONIZE))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                print("[SERVER-SYNC] Connected by", addr)
                
                data = conn.recv(1024)
                if not data:
                    break
                print("[SERVER-SYNC] Received", data)

                if data.decode() == "sync":
                    conn.sendall(json.dumps(blockchain.chain, default=lambda x: x.__dict__).encode())
                else:
                    conn.sendall("error".encode())

def client(blockchain):
    while True:
        #CREATE A SOCKET TO RECEIVE DATABASES AND SYNCHRONIZE
        blockchains = []

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            for HOST in HOSTS:
                s.connect((HOST, PORT_SYNCHRONIZE))
                s.sendall("sync".encode())
                data = s.recv(1024)
                print("[CLIENT-SYNC] Received", data.decode())
                blockchains.append(json.loads(data.decode()))

        #COMPARE THE BLOCKCHAINS AND CHOOSE THE LONGEST
        longest = blockchain.chain
        for chain in blockchains:
            if len(chain) > len(longest):
                longest = chain

        #IF THE LONGEST IS NOT THE LOCAL BLOCKCHAIN, REPLACE IT
        if longest != blockchain.chain:
            blockchain.chain = longest
            blockchain.first_block = longest[0]
            blockchain.last_block = longest[len(longest) - 1]
            print("Blockchain synchronized")
        else:
            print("Blockchain already synchronized")
        
        time.sleep(5)

    
