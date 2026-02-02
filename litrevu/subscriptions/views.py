from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def subscriptions_view(request):
    return HttpResponse('<h1>This is the subscriptions view.</h1>')