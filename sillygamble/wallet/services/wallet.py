import requests

from django.core.exceptions import ObjectDoesNotExist
from requests.exceptions import HTTPError, Timeout

from wallet.models import Transaction
from .blockapi import BlockExplorerAPI

# from .models import Wallet, Desposit

class WalletImportTransaction(object):
    def __init__(self, request, queryset):
        self._request = request
        self._queryset = queryset

    def validate(self):
        pass
        
    def run(self):
        for wallet in self._queryset:
            api = BlockExplorerAPI(wallet.wallet_id)
            for confirmed_transaction in api.get_confirmed_transactions():
                try:
                    transaction = Transaction.objects.get(transaction_id=confirmed_transaction.hash)
                except ObjectDoesNotExist as err:
                    transaction = Transaction()
                    transaction.transaction_id = confirmed_transaction.hash
                    transaction.from_wallet = confirmed_transaction.wallet
                    transaction.to_wallet = wallet
                    transaction.amount_out = confirmed_transaction.valueOut
                    transaction.amount = confirmed_transaction.value
                    transaction.fee = confirmed_transaction.fee
                    transaction.save()