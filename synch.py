import socket
import json
import time
from chain import Blockchain, Block  # Assuming these are the relevant classes

PORT_SYNCHRONIZE = 12347  # The port used by the network to synchronize the blockchain
HOSTS = ["10.0.1.1", "10.0.0.1", "10.0.0.2"]  # The IP addresses of the blockchain network

def server(blockchain, host):
    # CREATES A SOCKET TO SEND THE BLOCKCHAIN FOR THE SERVERS TO SYNCHRONIZE
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, PORT_SYNCHRONIZE))
        s.listen(len(HOSTS))
        while True:
            conn, addr = s.accept()
            with conn:                
                data = conn.recv(1024)
                if not data:
                    break

                if data.decode() == "sync":
                    # Serialize the blockchain
                    serialized_chain = json.dumps([block.__dict__ for block in blockchain.chain])
                    conn.sendall(serialized_chain.encode())
                else:
                    conn.sendall("error".encode())

def client(blockchain, pending_transactions):
    while True:
        time.sleep(15)
        #CREATE A SOCKET TO RECEIVE DATABASES AND SYNCHRONIZE
        blockchains = []

        for HOST in HOSTS:        
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT_SYNCHRONIZE))
                s.sendall("sync".encode())
                
                # Receive data in chunks and ensure complete JSON string
                data = b""
                while True:
                    chunk = s.recv(2048)
                    if not chunk:
                        break
                    data += chunk
                    try:
                        json_data = json.loads(data)
                        break
                    except json.JSONDecodeError:
                        continue
                
                # Deserialize the JSON data back into Block instances
                deserialized_chain = [Block(**block) for block in json_data]
                blockchains.append(deserialized_chain)

        #COMPARE THE BLOCKCHAINS AND CHOOSE THE LONGEST
        longest = blockchain.chain
        longest_size = len(blockchain.chain) + len(pending_transactions)

        for chain in blockchains:
            if len(chain) > longest_size:
                longest = chain
                longest_size = len(chain)

        #IF THE LONGEST IS NOT THE LOCAL BLOCKCHAIN, REPLACE IT
        if longest != blockchain.chain:
            blockchain.chain = longest
            print("Blockchain synchronized")
        else:
            print("Blockchain already was synchronized")