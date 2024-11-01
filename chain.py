from hashlib import *
import json
import time

class Block:
    def __init__(self, data, previous_hash):
        self.data = data
        self.previous_hash = previous_hash

    def calc_hash(self):
        return sha256(self.data.encode()).hexdigest()
    
class Blockchain:

    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        self.chain.append(Block("Genesis Block", "0"))
        self.last_block = self.first_block = self.chain[0]

    def add_block(self, data):
        self.chain.append(Block(data, self.chain[-1].calc_hash()))
        self.last_block = self.chain[len(self.chain) - 1]
        self.save_chain()

    def print_chain(self):
        print(json.dumps(self.chain, indent=4, default=lambda x: x.__dict__))
    
    def verify_integrity(self):
        for block in self.chain:
            if self.chain.index(block) == 0:
                continue
            if block.previous_hash != self.chain[self.chain.index(block) - 1].calc_hash():
                return False
        return True
    
    def save_chain(self):
        with open('./chain.json', "w") as file:
            file.write(json.dumps(self.chain, default=lambda x: x.__dict__))

    def load_chain(self):
        print("Loading chain from file...")
        with open('./chain.json', "r") as file:
            self.chain = json.load(file)
            self.chain = [Block(block['data'], block['previous_hash']) for block in self.chain]
            self.first_block = self.chain[0]
            self.last_block = self.chain[len(self.chain) - 1]
        print("Done.")

def maintenance(blockchain):
    try:
        startup(blockchain)

        while (True):
            if blockchain.verify_integrity():
                blockchain.save_chain()
            else:
                print("ALERT: Blockchain was compromised")
                print("Do you want to restore it from the last save? (y/n)")
                choice = input("> ")

                if choice.upper() == "Y":
                    blockchain.load_chain()
                    blockchain.print_chain()
                else:
                    print("Do you want to create a new blockchain? (y/n)")
                    choice = input("> ")

                    if choice.upper() == "Y":
                        blockchain = Blockchain()
                        blockchain.save_chain()
                    else:
                        print("Exiting...")
                        exit(0)

            time.sleep(1)

    except KeyboardInterrupt:
            print("\n\n\nExiting...")
            if (blockchain.verify_integrity()):
                blockchain.save_chain()

def startup(blockchain):
    while (True):
        print("Do you want to create a new blockchain or load an existing one? (new/load)")
        choice = input("> ")
        if choice.upper() == "NEW":
            blockchain.save_chain()
            break
        elif choice.upper() == "LOAD":
            blockchain.load_chain()
            blockchain.print_chain()
            break
