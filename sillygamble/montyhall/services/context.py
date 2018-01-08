from . import crypto

def create(request):
    current_game = request.session.get('game')

    if current_game['stage'] == 2:
        context = {
            'game_data_id': request.session.get('game_data_id'),
            'cards': current_game['cards'],
            'wallet_number': request.session.get('wallet_number'),
            'checksum': request.session.get('checksum'),
            'prize': current_game['prize'],
            'selected': current_game['selected'],
            'winner': current_game['winner'],
            'test_mode': current_game['test_mode'],
            'amount_out': request.session.get('amount_out'),
        }
    else:
        context = {
            'wallet_number': request.session.get('wallet_number'),
            'stage': current_game['stage'],
            'checksum': request.session.get('checksum'),
            'cards': current_game['cards'],
            'selected': current_game['selected'],
            'revealed': current_game['revealed'],
            'test_mode': current_game['test_mode'],
            'amount_out': request.session.get('amount_out'),
        }

    return context