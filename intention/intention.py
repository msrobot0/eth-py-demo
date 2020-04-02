import time, json, sys
from web3 import Web3, HTTPProvider
from web3.auto.infura import w3

class Intention:
    def __init__(self, contract_address,  wallet_address, wallet_private_key,provider_url):
        try:
            self.contract_address     = contract_address
            self.wallet_private_key   = wallet_private_key
            self.wallet_address       = wallet_address
            self.w3 = Web3(HTTPProvider(provider_url))
            self.contract = self.w3.eth.contract(address = contract_address, abi = json.loads(contract_abi.abi))
        except Exception:
            print("Error %s" %  sys.exc_info()[0])

    def echo_intention(self,intention):
        return intention

    def send_ether_to_contract(amount_in_ether):
        amount_in_wei = self.w3.toWei(amount_in_ether,'ether');
        nonce = self.w3.eth.getTransactionCount(self.wallet_address)
        txn_dict = {
                'to': self.contract_address,
                'value': amount_in_wei,
                'gas': 2000000,
                'gasPrice': self.w3.toWei('40', 'gwei'),
                'nonce': nonce,
                'chainId': 3
        }

        signed_txn = self.w3.eth.account.signTransaction(txn_dict, self.wallet_private_key)

        txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        txn_receipt = None
        count = 0
        #make async
        while txn_receipt is None and (count < 30):
            txn_receipt = w3.eth.getTransactionReceipt(txn_hash)
            print(txn_receipt)
            time.sleep(10)


        if txn_receipt is None:
            return {'status': 'failed', 'error': 'timeout'}

        return {'status': 'added', 'txn_receipt': txn_receipt}

    def check_whether_address_is_approved(address):
        return self.contract.functions.isApproved(address).call()

    def make_an_intention(intention):
        nonce = self.w3.eth.getTransactionCount(self.wallet_address)
        txn_dict = self.contract.functions.make_intention(intention).buildTransaction({
            'chainId': 3,
            'gas': 140000,
            'gasPrice': w3.toWei('40', 'gwei'),
            'nonce': nonce,
        })

        signed_txn = self.w3.eth.account.signTransaction(txn_dict, private_key=self.wallet_private_key)

        result = self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)

        tx_receipt = self.w3.eth.getTransactionReceipt(result)

        count = 0
        #make async
        while tx_receipt is None and (count < 30):
            time.sleep(10)
            tx_receipt = self.w3.eth.getTransactionReceipt(result)
            print(tx_receipt)


        if tx_receipt is None:
            return {'status': 'failed', 'error': 'timeout'}

        processed_receipt = self.contract.events.CreateIntention().processReceipt(tx_receipt)

        print(processed_receipt)

        output = "Address {} broadcasted the opinion: {}"\
            .format(processed_receipt[0].args._soapboxer, processed_receipt[0].args._opinion)
        print(output)

        return {'status': 'added', 'processed_receipt': processed_receipt}
