import logging

from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.core.exceptions import PermissionDenied
from django.contrib import messages

from .forms import WalletNumberForm
from .services.wallet import TransactionDetails, WalletNumberValidator, CurrentWallet

logger = logging.getLogger(__name__)

def index(request):
    try:
        if request.method == 'POST':
            form = WalletNumberForm(request.POST)
            if form.is_valid():
                number = form.cleaned_data['wallet_number']

                validator = WalletNumberValidator(number)
                validator.validate()

                transactionDetails = TransactionDetails(number)

                request.session['wallet_number'] = number
                request.session['transaction_id'] = transactionDetails.get_transaction_id()
                request.session['amount_out'] = transactionDetails.get_amount_out_str()

                return redirect('/montyhall/')
            else:
                raise PermissionDenied('Invalid bitcoin wallet number.')
                # messages.add_message(request, messages.WARNING, )
                # return render(request, 'home_index.html', {})
                # # raise ValueError('Invalid bitcoin wallet number')

        else:
            return render(request, 'home/index.html', {})
    except ValueError as err:
        raise PermissionDenied(err)

def howto(request):
    current = CurrentWallet()
    context = {
        'wallet': current.get_current_wallet()
    }
    return render(request, 'home/howto.html', context)

def about(request):
    return render(request, 'home/about.html', {})

def games(request):
    return render(request, 'home/games.html', {})

def trust(request):
    return render(request, 'home/trust.html', {})

def responsable(request):
    return render(request, 'home/responsable.html', {})
