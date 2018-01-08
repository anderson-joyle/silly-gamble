import random
import requests
import os

from requests.exceptions import HTTPError

from montyhall.models import Game, GameCard
from wallet.models import Transaction

from . import crypto

def create(request):
    cards = [crypto.salt(), crypto.salt(), crypto.salt(), crypto.salt()]

    test_mode = False
    transaction_id = ''
    if request.session.get('wallet_number') == 'test_mode':
        test_mode = True
    else:
        transaction = Transaction.objects.get(transaction_id=request.session.get('transaction_id'))
        transaction_id = transaction.transaction_id

    suffled_cards = list(cards)
    random.shuffle(suffled_cards)

    game = {
        'id': crypto.salt(),
        'stage': 0,
        'cards': cards,
        'prize': random.choice(cards),
        'selected': '',
        'revealed': '',
        'winner': False,
        'test_mode': test_mode,
        'transaction_id':transaction_id,
        'game_data_salt': crypto.salt()
    }

    game_record = Game()
    game_record.game_id = game['id']
    game_record.wallet_number = request.session.get('wallet_number')
    # game_record.transaction_id = transaction
    game_record.test = test_mode
    game_record.save()

    for card in cards:
        game_card_record = GameCard()
        game_card_record.game = game_record
        game_card_record.card_id = card

        if card == game['prize']:
            game_card_record.prize = True

        game_card_record.save()

    return game

def validate(game):
    # Has game? Validate!
    if game:
        if game['stage'] == 0:
            """
            Game has begun. No selected cards.
            """
            if game['selected']:
                raise ValueError('Stage 0 has selected card already, which is not normal.')
        elif game['stage'] == 1:
            """
            User has selected a card. Should contain one selected card.
            Plus. this selected card must match with any card in the list.
            """
            if not game['selected']:
                raise ValueError('Stage 1 has no selected card, which is not normal.')

            if not game['selected'] in game['cards']:
                raise ValueError('Selected card does not exists in card list.')
        elif game['stage'] == 2:
            """
            User has selected a card. Should contain one selected card.
            Plus. this selected card must match with any card in the list.
            """
            pass
        else:
            raise ValueError('Stange {0} is not expected.'.format(game['stage']))

def progress(current_game, card_id):
    if current_game['stage'] == 0:
        current_game = select_card(current_game, card_id)
        current_game = reveal_card(current_game)
        current_game = _step_stage_forward(current_game)
        validate(current_game)
        # return render(request, 'montyhall_index.html', context.create(request))
    elif current_game['stage'] == 1:
        current_game = select_card(current_game, card_id)

        # Set selected card record
        game_record = Game.objects.get(game_id=current_game['id'])

        game_card_record = GameCard.objects.get(card_id=card_id)
        game_card_record.selected = True

        if card_id == current_game['prize']:
            current_game['winner'] = True

            game_record.winner = True
            game_record.save()

            game_card_record.prize = True

        current_game = _step_stage_forward(current_game)
        game_record.finished = True

        game_record.save()
        game_card_record.save()

        if not current_game['test_mode']:
            transaction = Transaction.objects.get(transaction_id=current_game['transaction_id'])
            transaction.spent = True
            transaction.save()
    else:
        raise ValueError('Stange {0} is not expected.'.format(current_game['stage']))

    return current_game

def create_game_data(game):
    if game['test_mode']:
        data = """Game id: {0}
        Prize card: {1}
        Cards set: {2}
        Salt: {3}""".format(game['id'], game['prize'], game['cards'], game['game_data_salt'])
    else:
        data = """Game id: {0}
        transaction id: {1}
        Prize card: {2}
        Cards set: {3}
        Salt: {4}""".format(game['id'], game['transaction_id'], game['prize'], game['cards'], game['game_data_salt'])
    return data

def select_card(game, card_id):
    game['selected'] = card_id

    return game

def reveal_card(game):

    suffled_cards = list(game['cards'])
    random.shuffle(suffled_cards)

    while True:
        card = random.choice(suffled_cards)
        if card != game['selected'] and card != game['prize']:
            game['revealed'] = card
            break

    game_card_record = GameCard.objects.get(card_id=card)
    game_card_record.revealed = True
    game_card_record.save()

    return game

def _step_stage_forward(game):
    game['stage'] += 1
    return game

def create_looser_deck():
    return ''

def create_winner_deck():
    return ''