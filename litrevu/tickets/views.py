from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def tickets_view(request):
    return HttpResponse('<h1>This is the tickets view.</h1>')