from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def flux_view(request):
    return HttpResponse('<h1>This is the flux view.</h1>')