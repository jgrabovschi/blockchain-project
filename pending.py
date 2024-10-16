from datetime import datetime
import time
import socket

class PendingTransaction:
    def __init__(self, message, timestamp, id):
        self.message = message
        self.timestamp = timestamp
        self.id = id
        self.accepted = 'Not Yet'

HOST = '10.0.1.1'
PORT_ACCEPT = 12346 
TTL = 5 #IN MINUTES

def verify_pending(pending_transactions, blockchain):
    # This function will be responsible for verifying the pending transactions
    while(True):
        print(pending_transactions)
        for pending in pending_transactions:
            now = datetime.now()
            difference = now - pending.timestamp

            if difference.seconds / 60 < TTL and pending.accepted == 'Not Yet':
                continue

            if pending.accepted == 'Yes':
                blockchain.add_block(pending.message.data)
                print('[PENDING_VERIFIED] block added')

            pending_transactions.remove(pending)

        time.sleep(5)

def accept_pending(pending_transactions):        
    # This function will be responsible for managing the pending transactions.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT_ACCEPT))
        s.listen(len(pending_transactions))
        while (True):
            conn, addr = s.accept()
            with conn:
                print('[PENDING] Connected by', addr)
                data = conn.recv(1024)
                if not data:
                    break            
                
                id = int(data.decode())
                
                if id != -1:
                    for pending in pending_transactions:
                        if pending.id == id:
                            index = pending_transactions.index(pending)
                            pending_transactions[index].accepted = 'Yes'
                            break
                    print('[PENDING] Transaction ' + data.decode() + ' accepted')
                else:
                    for pending in pending_transactions:
                        if pending.id == id:
                            index = pending_transactions.index(pending)
                            pending_transactions[index].accepted = 'No'
                            break
                    print('[PENDING] Transaction ' + data.decode() + ' rejected')
                
            