from Crypto.PublicKey import RSA
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