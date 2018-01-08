import logging

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.core.exceptions import SuspiciousOperation

from .services import crypto, context, session, game
from .forms import SelectCardForm

logger = logging.getLogger(__name__)

def index(request):
    try:
        if request.method == 'GET':
            session.validate(request)
            session.create(request)
            return render(request, 'montyhall/index.html', context.create(request))
        else:
            raise SuspiciousOperation('POST operations ARE NOT allowed here.')
    except SuspiciousOperation as err:
        logger.error(err)
        return SuspiciousOperation(err)

def card(request, card_id):
    try:
        current_game = request.session.get('game')
        if current_game is None:
            request.session.flush()
            return redirect('/')

        if request.method == 'GET':
            request.session['game'] = game.progress(current_game, card_id)
            if request.session['game']['stage'] == 2:
                return render(request, 'montyhall/result.html', context.create(request))
            else:
                return render(request, 'montyhall/index.html', context.create(request))
        else:
            raise SuspiciousOperation('POST operations ARE NOT allowed here.')
    except ValueError as err:
        request.session.flush()
        return redirect('/')

def test(request):
    request.session['wallet_number'] = 'test_mode'
    return redirect('/montyhall/')

def data(request, game_data_id):
    if game_data_id == request.session['game_data_id'] and request.session['game']['stage'] == 2:
        response = HttpResponse(game.create_game_data(request.session['game']), content_type="application/txt")
        response['Content-Disposition'] = 'inline; filename=' + request.session['game']['id'] + '.txt'
        return response
    else:
        raise SuspiciousOperation('Illegal attempt to download game data file')

def reset(request):
    session.create(request)
    return redirect('/montyhall/')

def logout(request):
    request.session.flush()
    return redirect('/')