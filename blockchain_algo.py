from flask import Flask, jsonify, request
import json
from time import time
from hashlib import sha256

class Blockchain:
    def __init__(self):
        # Initialize the blockchain with an empty chain, transactions, and a set of nodes
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash='1', proof=100)

    def new_block(self, proof, previous_hash=None):
        # Create a new block in the blockchain
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]) if self.chain else None,
        }

        # Reset the current list of transactions
        self.current_transactions = []

        # Add the new block to the chain
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        # Add a new transaction to the list of transactions
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        # Hash a block using SHA-256
        block_string = json.dumps(block, sort_keys=True).encode()
        return sha256(block_string).hexdigest()

    @property
    def last_block(self):
        # Get the last block in the chain
        return self.chain[-1]

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    # In a real-world scenario, you'd have a more complex PoW algorithm here
    proof = 1
    previous_hash = blockchain.hash(blockchain.last_block)
    block = blockchain.new_block(proof, previous_hash)

    # Respond with information about the mined block
    response = {
        'message': 'New Block Forged',
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    # Receive and add a new transaction to the block
    values = request.get_json()

    # Check that the required values are present in the POST data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Add the new transaction and respond with a confirmation message
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    # Return the full blockchain
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

if __name__ == '__main__':
    # Run the Flask application on host 0.0.0.0 and port 5000
    app.run(host='0.0.0.0', port=5000)
# This is a draft algorithm for the blockchain we are creating, for demonstration purpose. 
