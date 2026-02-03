from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def subscriptions_view(request):
    return render(request, 'subscriptions/subs-home.html')