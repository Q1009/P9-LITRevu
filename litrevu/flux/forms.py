from django import forms
from flux.models import Ticket, Review
from django.contrib.auth import get_user_model

class TicketForm(forms.ModelForm):
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput(), initial=True)
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']

class DeleteTicketForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput(), initial=True)

class FollowUsersForm(forms.Form):
    user_to_follow = forms.CharField(label="Nom d'utilisateur", max_length=55)

class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [(i, str(i)) for i in range(6)]
    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect, label="Note")
    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']