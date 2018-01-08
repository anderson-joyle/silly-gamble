from django.core.exceptions import SuspiciousOperation

from . import game, crypto

def create(request):
    request.session['game'] = game.create(request)
    request.session['game_data_id'] = crypto.salt()
    request.session['checksum'] = crypto.checksum(game.create_game_data(request.session['game']))

def validate(request):
    if not request.session.get('wallet_number'):
        raise SuspiciousOperation('Trying to access without wallet number')

    game.validate(request.session.get('game'))
    