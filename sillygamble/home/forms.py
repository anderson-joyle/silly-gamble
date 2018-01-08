from django import forms

class WalletNumberForm(forms.Form):
    wallet_number = forms.CharField(label='Wallet number', max_length=255)