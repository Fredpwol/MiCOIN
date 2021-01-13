from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import Crypto.Random
import binascii


class Wallet:
    def __init__(self):
        self.private_key = None
        self.public_key = None

    def create_key(self):
        private_key,public_key = self.generate_keys()
        self.private_key = private_key
        self.public_key = public_key

    def load_key(self):
        pass
    
    def generate_keys(self):
        """
        This function generates the public and private Keys using the RSA algorithm with a bit size of 1024
        and a random function.
        The public Key is generated from the private Key
        and the are all converted to hexadecimal from binary by using the hexlify method and decoded to ascii
        to be displayed
        """
        private_key = RSA.generate(1024,Crypto.Random.new().read)
        public_key = private_key.publickey()
        return (binascii.hexlify(private_key.exportKey(format="DER")).decode("ascii"),binascii.hexlify(public_key.exportKey(format="DER")).decode("ascii"))
    

    def generate_signature(self, sender, recipient, amount):
        """
        generates signature for a transaction.
        """
        private_key_raw = RSA.importKey(binascii.unhexlify(self.private_key))
        signer = PKCS1_v1_5.new(private_key_raw)
        tx_hash = SHA256.new((str(sender) + str(recipient) + str(amount)).encode("utf-8"))

        signature = signer.sign(tx_hash)

        return binascii.hexlify(signature).decode("ascii")

    @staticmethod
    def verify_signature(transaction):
        if transaction.sender === "SYSTEM":
            return True
        public_key_raw = RSA.importKey(binascii.unhexlify(transaction.sender))
        verifier = PKCS1_v1_5.new(public_key_raw)
        tx_hash = SHA256.new((str(transaction.sender) + str(transaction.recipient) + str(transaction.amount)).encode("utf-8"))

        return verifier.verify(tx_hash, binascii.unhexlify(transaction.signature))