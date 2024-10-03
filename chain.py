from hashlib import sha256
import json

class Block:
    def __init__(self, data, previous_hash):
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calc_hash()

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
        self.chain.append(Block(data, self.chain[-1].hash))
        self.last_block = self.chain[len(self.chain) - 1]

    def print_chain(self):
        print(json.dumps(self.chain, indent=4, default=lambda x: x.__dict__))

    def get_first_block_hash(self):
        return self.first_block.hash

    def get_last_block_hash(self):
        return self.last_block.hash
    
    def verify_integrity(self):
        for block in self.chain:
            if block.hash != block.calc_hash():
                return False
            if self.chain.index(block) == 0:
                continue
            if block.previous_hash != self.chain[self.chain.index(block) - 1].hash:
                return False
        return True
    
    def save_chain(self):
        print("Saving chain to file...")
        with open('./chain.json', "w") as file:
            file.write(json.dumps(self.chain, default=lambda x: x.__dict__))
        print("Done.")

    def load_chain(self):
        print("Loading chain from file...")
        with open('./chain.json', "r") as file:
            self.chain = json.load(file)
            self.chain = [Block(block['data'], block['previous_hash']) for block in self.chain]
            self.first_block = self.chain[0]
            self.last_block = self.chain[len(self.chain) - 1]
        print("Done.")