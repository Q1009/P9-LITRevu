from django import forms
from flux.models import Ticket

class TicketForm(forms.ModelForm):
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput(), initial=True)
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']

class DeleteTicketForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput(), initial=True)