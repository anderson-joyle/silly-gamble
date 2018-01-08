from django.db import models

# Create your models here.
class Common(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Game(Common):
    game_id = models.CharField(primary_key=True, max_length=100, blank=False)
    wallet_number = models.CharField(max_length=100, blank=False)
    bitcoin_amount = models.DecimalField(max_digits=10, decimal_places=5, default=0)
    # deposit_id = models.ForeignKey('wallet.Deposit', on_delete=models.DO_NOTHING)
    finished = models.BooleanField(default=False)
    winner = models.BooleanField(default=False)
    test = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % (self.game_id)

class GameCard(Common):
    card_id = models.CharField(primary_key=True, max_length=100, blank=False)
    game = models.ForeignKey('montyhall.Game', on_delete=models.DO_NOTHING)
    selected = models.BooleanField(default=False)
    prize = models.BooleanField(default=False)
    reveal = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % (self.card_id)