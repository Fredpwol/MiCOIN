from utility.hash_util import hash_block, hash_string_256
from wallet import Wallet

class Verification():
    @staticmethod
    def valid_proof(transactions,last_hash,proof):
        '''
        This checks if The hash of the proof of work data meets a certain criteria if so
        return True
        '''
        trial = (str([tx.toordered_dict() for tx in transactions]) + str(last_hash) + str(proof)).encode()
        hashedtrail = hash_string_256(trial)
        return hashedtrail[0:2] == '00'

    @staticmethod
    def verify_transaction(transaction, get_balance, check_balance=True):
        '''
        This is will check if the sender has enough balance left to send to the reciepient
        '''
        if check_balance:
            sender_balance = get_balance(transaction.sender)
            return sender_balance >= transaction.amount and Wallet.verify_signature(transaction)
        else:
            return Wallet.verify_signature(transaction)

    @classmethod
    def verify_chain(cls, blockchain):
        '''Checks if the chain is Valid or not in a block chain and stop it from corrupting the 
        Entire system....'''
        for (index,block) in enumerate(blockchain):
            if index == 0:
                continue
            elif block.previous_hash != hash_block(blockchain[index-1]):
                return  False
            # checks if the hash of The  block fullfils The condition given else return false
            if not cls.valid_proof(block.transaction [:-1],block.previous_hash,block.proof):
                print('Invalid Block!!!')
                return False
        return True

    @classmethod
    def verify_openTransaction(cls,open_tx,get_balance):
        return [cls.verify_transaction(tx, get_balance, False) for tx in open_tx]
