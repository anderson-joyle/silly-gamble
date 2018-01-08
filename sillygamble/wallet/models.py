import uuid
from django.db import models

def uuid_str():
    return str(uuid.uuid4()).replace('-','')

# Create your models here.
class Common(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Wallet(Common):
    wallet_id = models.CharField(primary_key=True, max_length=100, blank=False)
    label = models.CharField(max_length=20, blank=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{0} ({1}...)'.format(self.label, self.wallet_id[:6])

class Transaction(Common):
    transaction_id = models.CharField(primary_key=True, max_length=100, blank=False)
    amount_out = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    amount = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    fee = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    from_wallet = models.CharField(max_length=100, blank=False)
    to_wallet = models.ForeignKey('wallet.Wallet', on_delete=models.DO_NOTHING)
    spent = models.BooleanField(default=False)

    def __str__(self):
        return '{0}...'.format(self.transaction_id[:20])

# class Deposit(Common):
#     deposit_id = models.CharField(primary_key=True, max_length=100, default=uuid_str)
#     from_wallet = models.CharField(max_length=100, blank=False)
#     to_wallet = models.ForeignKey('wallet.Wallet', on_delete=models.DO_NOTHING)
#     bitcoin_amount = models.DecimalField(max_digits=10, decimal_places=5, default=0)
#     spent = models.BooleanField(default=False)

    # def __str__(self):
    #     return '%s' % (self.deposit_id)