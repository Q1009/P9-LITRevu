from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
from flux import models
from django.conf import settings

# Create your views here.
class HomePage(LoginRequiredMixin, View):
    template_name = 'flux/home.html'

    def get(self, request):
        tickets = models.Ticket.objects.all()
        return render(request, self.template_name, context={'tickets': tickets})
    
class PostsPage(LoginRequiredMixin, View):
    template_name = 'flux/posts.html'

    def get(self, request):
        return render(request, self.template_name)
    
class SubscriptionsPage(LoginRequiredMixin, View):
    template_name = 'flux/subscriptions.html'

    def get(self, request):
        return render(request, self.template_name)
    
class CreateTicketPage(LoginRequiredMixin, View):
    template_name = 'flux/create_ticket.html'

    def get(self, request):
        form = forms.TicketForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.author = request.user
            ticket.save()
            return redirect(settings.LOGIN_REDIRECT_URL)
        return render(request, self.template_name, context={'form': form})