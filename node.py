from flask import Flask, jsonify
from flask_cors import CORS
from wallet import Wallet
from blockchain import Blockchain

app = Flask(__name__)
wallet = Wallet()
CORS(app)
blockchain = Blockchain(wallet.public_key)


@app.route("/")
def index():
    return "Hello World!"

@app.route("/chain")
def get_blockchain():
    chain = blockchain.serialize_chain()
    return jsonify(chain)

if __name__ == "__main__":
    app.run(debug=True)