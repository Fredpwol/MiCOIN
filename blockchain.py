from functools import reduce
import hashlib
import json
import pickle


from utility.verification import Verification
from utility.hash_util import hash_block
from block import Block
from transactions import Transaction
from wallet import Wallet

GENESIS_BLOCK = Block(0, '', [],None, 0)
MINING_REWARD = 10  # this ia The reward amount given to miners
class Blockchain():
    def __init__(self,user):
        # blockchain initialization with the GENESIS BLOCK as it start point
        self.__chain = [GENESIS_BLOCK] 
        # The oustanding transaction contains all the transaction ready to be placed in a block
        self.__outstanding_transaction = []
        self.owner = user
        self.load_data()

    @property
    def blockchain(self):
        return self.__chain[:]

    @blockchain.setter
    def blockchain(self,val):
        self.__chain = val

    def get_otx(self):
        copy_otx = self.__outstanding_transaction[:]
        return copy_otx

    def get_last_blockchain_value(self):
        """returns the last previous value of the blockchain """
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]


    def load_data(self):
        """
        This loads The data stored in the Blockchain file and assign it to The blockchain and outstanding_transaction
        Variables. if The file is isn't found it Initializes The blockchain variable and assign the genesis block to
        it. 
        """
        try:
            with open('blockchain.txt', mode='r') as b:
                block_data = b.readlines()
                blockchain = json.loads(block_data[0][:-1])
                outstanding_transaction = json.loads(block_data[1])
                updated_blockchain = []
                for block in blockchain:
                    orderd_transactions = [Transaction(tx['sender'],tx['recipient'],tx['amount'], tx["signature"]) for tx in block['transaction']]
                    # The updated_block assigns The block saved in the blockchain file to the Block class and assigns instatiate it to update_block
                    update_block = Block(block['index'],block['previous_hash'],orderd_transactions,block['proof'],block['timestamp'])
                    updated_blockchain.append(update_block)  # appends the block object to the updated_blockchain list
                self.blockchain = updated_blockchain 
                updated_tx = []
                for tx in outstanding_transaction:
                    update_tx = Transaction(tx['sender'],tx['recipient'],tx['amount'],tx["signature"])
                    updated_tx.append(update_tx)
                self.__outstanding_transaction = updated_tx
        except (IOError,IndexError):
            pass          


    def add_data(self):
        """
        This stores The data in The blockchain and outstanding_transaction Variable into The blockchain file
        """
        try:
            with open('blockchain.txt', mode='w') as f:
                save_block = [block.__dict__ for block in [Block(blockes.index,blockes.previous_hash,[tx.__dict__ for tx in blockes.transaction],blockes.proof,blockes.timestamp) for blockes in self.__chain]]
                f.write(json.dumps(save_block))
                f.write('\n')
                save_tx = [tx.__dict__ for tx in self.get_otx()]
                f.write(json.dumps(save_tx))
        except IOError:
            print('Failed to Save!')


    def add_transaction(self, recipient , amount, signature, sender):
        """adds value to the blockchain
        Arguments:
            sender: This is the sender of the coin
            recipient: This is the reciever of the coin whom is sent to
            ammount: This is the ammount that is been sent;"""
        if self.owner == None:
            return False

        transaction_data = Transaction(sender,recipient,amount, signature)
        # Checks if the Sender has enough amount left to send if so The transaction is Valid  and added to the oustanding ...
        # .....transaction where it will be proccesed into the blockchain.
        if Verification.verify_transaction(transaction_data,self.get_balance):
            self.__outstanding_transaction.append(transaction_data)
            self.add_data() # adds the transaction to the blockchain file after every transaction
            return True
        return False


    def get_balance(self,participant):
        # Get the amount of coin sent to the reciepient if nothing is sent it returns Zero.
        # Checks for coin already processed in the blockchain.
        sent_coin = [[val.amount for val in block.transaction if val.sender == participant] for block in self.__chain]
        # check for yet to be processed coin in the blockchain to avoid double spending...........
        open_coin = [tx.amount for tx in self.__outstanding_transaction if tx.sender == participant]
        # appends all of Them into the sent coin variable
        sent_coin.append(open_coin)
        print(sent_coin)
        coin_sent = reduce(lambda tx_sum,tx_amt:tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0,sent_coin,0)
        # get the amount of coin recieved by the sender
        recieved_coin = [[val.amount for val in block.transaction if val.recipient == participant] for block in self.__chain]
        coin_recived = reduce(lambda tx_sum,tx_amt:tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0,recieved_coin,0)
        return  coin_recived - coin_sent # total amount left



    def proof_of_work(self):
        """
        This check if The validation of proof meet The condition not so change the proof 
        Until it meets the condition 
        """
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        while not Verification.valid_proof(self.get_otx(), last_hash, proof):
            proof += 1
        return proof




    def mine_block(self):
        """This is used to verify if the block is legit and ready to be placed in the blockchain"""
        # REWARD: This is a bonus given to the miner after a successful mine....
        if self.owner == None:
            return False
        proof = self.proof_of_work()
        reward = Transaction('SYSTEM',self.owner,MINING_REWARD, "")
        # COPIED_TRANSACTION: This copies the outstanding transaction in case of a situation the mining Fails
        # And it also copied the block to mined and append the mining reward to it to show its been mined
        copied_transaction = self.__outstanding_transaction[:]
        for i, tx in enumerate(copied_transaction):
            if not Wallet.verify_signature(tx):
                block.transaction.pop(i) #remove the block from the transaction don't know if should return coin back to sender? consider that later.
        copied_transaction.append(reward)
        last_block = self.__chain[-1]
        hashed_block = hash_block(last_block)
        print(hashed_block)
        block = Block(len(self.__chain),hashed_block,copied_transaction,proof)
        self.__chain.append(block)
        self.__outstanding_transaction = []
        self.add_data()
        return True
        
