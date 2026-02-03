from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def flux_view(request):
    return render(request, 'flux/flux-home.html')