from django import forms
from flux.models import Ticket, Review


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']


class FollowUsersForm(forms.Form):
    user_to_follow = forms.CharField(label="Nom d'utilisateur", max_length=55)


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [(i, str(i)) for i in range(6)]
    rating = forms.ChoiceField(
        choices=RATING_CHOICES, widget=forms.RadioSelect, label="Note")

    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']
