from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
from flux import models
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone

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
    
class EditTicketPage(LoginRequiredMixin, View):
    template_name = 'flux/edit_ticket.html'
    edit_form_class = forms.TicketForm
    delete_form_class = forms.DeleteTicketForm

    def get(self, request, ticket_id):
        ticket = get_object_or_404(models.Ticket, id=ticket_id)
        if ticket.author != request.user:
            return redirect(settings.LOGIN_REDIRECT_URL)
        edit_form = self.edit_form_class(instance=ticket)
        delete_form = self.delete_form_class()
        context = {
            'edit_form': edit_form,
            'delete_form': delete_form,
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request, ticket_id):
        ticket = get_object_or_404(models.Ticket, id=ticket_id)
        edit_form = self.edit_form_class(instance=ticket)
        delete_form = self.delete_form_class()
        if ticket.author != request.user:
            return redirect(settings.LOGIN_REDIRECT_URL)
        if 'edit_ticket' in request.POST:
            edit_form = self.edit_form_class(request.POST, request.FILES, instance=ticket)
            if edit_form.is_valid():
                edit_form.save(commit=False)
                ticket.date_edited = timezone.now()
                edit_form.save()
                return redirect(settings.LOGIN_REDIRECT_URL)
        if 'delete_ticket' in request.POST:
            delete_form = self.delete_form_class(request.POST)
            if delete_form.is_valid():
                ticket.delete()
                return redirect(settings.LOGIN_REDIRECT_URL)
        context = {
            'edit_form': edit_form,
            'delete_form': delete_form,
        }
        return render(request, self.template_name, context=context)