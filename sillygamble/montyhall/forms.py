from django import forms

class SelectCardForm(forms.Form):
    card_id = forms.CharField(label='Card id', max_length=255)