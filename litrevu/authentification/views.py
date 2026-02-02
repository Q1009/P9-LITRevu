from django.shortcuts import render
from django.http import HttpResponse
from authentification.models import User

# Create your views here.
def login_view(request):
    users = User.objects.all()
    return render(request, 'authentification/login.html', {'users': users})

def subscribe_view(request):
    return render(request, 'authentification/subscribe.html')

def about_view(request):
    return HttpResponse('<h1>This is the about view.</h1> <p>Welcome to the LITRevu application!</p>')
