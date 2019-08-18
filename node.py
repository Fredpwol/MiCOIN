
from blockchain import Blockchain
from utility.verification import Verification
from wallet import Wallet

class Node():
    def __init__(self):
        self.wallet = Wallet()
        self.chain = None
    

    def run_mode(self):
        waiting = True
        while waiting:
            print('Please enter an input ')
            print('1: Add new Transaction Value')
            print('2: Mine the block')
            print('3: Output the blockchain block')
            print('4: to verify transactions.')
            print('5: to create a wallet.')
            print('6: to load wallet.')
            print('quit: to litterally Quit ')
            user_choice = self.get_user_choice()
            if user_choice == '1':
                txt_out = self.get_transaction_input()
                reciever,coin = (txt_out)
                if self.chain.add_transaction(reciever,coin,self.wallet.public_key):
                    print('Transaction completed')
                else:
                    print('Transaction Failed!!')
                print(self.chain.get_otx())
            elif user_choice == '2':
                if not self.chain.mine_block():
                    print("Sorry you can't mine a block right now,Please create a wallet.")
            elif user_choice == '3':
                self.display_blockchains()
            elif user_choice == '4':
                if Verification.verify_openTransaction(self.chain.get_otx(),self.chain.get_balance):
                    print('All Transactions are valid...')
                else:
                    print('The Transactions are invalid')
            elif user_choice == '5':
                self.wallet.create_key()
                self.chain = Blockchain(self.wallet.public_key)
            elif user_choice == '6':
                pass
            elif user_choice == 'quit':
                break
            else:
                print('Enter a Valid choice!')
            if not Verification.verify_chain(self.chain.blockchain):
                self.display_blockchains()
                print('Invalid Blockchain')
                break
            print('Balance of {} is {:.6f}'.format(self.wallet.public_key,self.chain.get_balance(self.wallet.public_key)))
            

            #print('Transactions completed')

        else:
            print('Event finished')
            
        print('Done!')


    def display_blockchains(self):
        # This displays Elements in the blockchain
        count = 0

        for bl in self.chain.blockchain:
            print('block '+str(count))
            print(bl)
            count += 1
    

    def get_user_choice(self):
        user_input = input('Enter your choice: ')
        return user_input


    # gets inputs of the user to add to the blockchain
    def get_transaction_input(self):
        trans_recipient = input('Enter a recipient name: ')
        trans_amount = float(input('Enter valid transaction: '))
        return trans_recipient,trans_amount

        
if __name__ == "__main__":
    node = Node()
    node.run_mode()