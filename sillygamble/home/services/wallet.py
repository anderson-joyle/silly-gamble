import requests

from django.core.exceptions import ObjectDoesNotExist, PermissionDenied

from requests.exceptions import HTTPError, Timeout

from wallet.models import Wallet, Transaction

class TransactionDetails(object):
    def __init__(self, wallet_number):
        self._wallet_number = wallet_number
        self.amount_out = 0.0
        self.transaction_id = ''

        self._fetch()

    def _fetch(self):
        try:
            transaction = Transaction.objects.get(from_wallet=self._wallet_number, spent=False, amount__gt=0)
            self.transaction_id = transaction.transaction_id
            self.amount_out = transaction.amount_out
        except ObjectDoesNotExist as err:
            raise PermissionDenied('No valid deposit has been identified for this wallet address.')

    def get_transaction_id(self):
        return self.transaction_id

    def get_amount_out(self):
        return self.amount_out

    def get_amount_out_str(self):
        return str(self.amount_out)

class WalletNumberValidator(object):
    TIMEOUT = 3000
    def __init__(self, wallet_number):
        self._wallet_number = wallet_number

    def validate(self):
        ret = True
        try:
            url = 'https://blockexplorer.com/api/addr-validate/{0}'.format(self._wallet_number)

            response = requests.get(url=url)
            response.raise_for_status()

            if response.text == 'false':
                ret = False
        except (HTTPError, Timeout) as err:
            pass
        finally:
            return ret

class CurrentWallet(object):
    def __init__(self):
        pass

    def get_current_wallet(self):
        wallet = Wallet.objects.filter(active=True).latest('created_at')
        return wallet.wallet_id