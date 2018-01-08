import requests

from requests.exceptions import HTTPError

# BlockExplorer
BLOCKEXPLORERAPI_URL = 'https://blockexplorer.com/api'
BLOCKEXPLORERAPI_ADDR_URL = BLOCKEXPLORERAPI_URL + '/addr/'
BLOCKEXPLORERAPI_TX_URL = BLOCKEXPLORERAPI_URL + '/tx/'
BLOCKEXPLORERAPI_MIN_CONFIRMATION = 6

# BlockCypher
BLOCKCYPHERAPI_URL = 'https://api.blockcypher.com/v1/btc/main'
BLOCKCYPHERAPI_ADDR_URL = BLOCKCYPHERAPI_URL + '/addrs/'
BLOCKCYPHERAPI_TX_URL = BLOCKCYPHERAPI_URL + '/txs/'

class BlockAPI(object):
    def __init__(self, wallet):
        self._wallet = wallet

    def _get_transactions_list(self):
        try:
            url = BLOCKEXPLORERAPI_ADDR_URL + self._wallet

            response = requests.get(url)
            response.raise_for_status()

            json_addr = response.json()

            return json_addr['transactions']
        except HTTPError as err:
            pass

    def get_confirmed_transactions(self):
        raise NotImplementedError("Function not implemented.")

class BlockExplorerAPI(BlockAPI):
    def get_confirmed_transactions(self):
        try:
            confirmed_tx_list = []
            transactions = self._get_transactions_list()
            for transaction in transactions:
                url = BLOCKEXPLORERAPI_TX_URL + transaction

                response = requests.get(url)
                response.raise_for_status()

                json_tx = response.json()

                if int(json_tx['confirmations']) >= BLOCKEXPLORERAPI_MIN_CONFIRMATION:
                    confirmed_tx = BitcoinConfirmedTransaction()
                    confirmed_tx.hash = json_tx['txid']
                    confirmed_tx.wallet = json_tx['vin'][0]['addr']
                    confirmed_tx.value = float(json_tx['vout'][1]['value'])
                    confirmed_tx.fee = float(json_tx['vout'][0]['value'])
                    confirmed_tx.valueOut = float(json_tx['valueOut'])
                    confirmed_tx_list.append(confirmed_tx)
            return confirmed_tx_list

        except HTTPError as err:
            pass

class BlockCypherAPI(BlockAPI):
    pass

class BitcoinConfirmedTransaction(object):
    def __init__(self):
        self.hash = ''
        self.wallet = ''
        self.value = 0
        self.valueOut = 0
        self.fee = 0