from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
from flux import models
from authentication import models as auth_models
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone
from itertools import chain
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.
class HomePage(LoginRequiredMixin, View):
    template_name = 'flux/home.html'

    def get(self, request):
        users_followed = auth_models.User.objects.filter(followed_by__user=request.user)
        tickets = models.Ticket.objects.filter(
            Q(author__in=users_followed) | Q(author=request.user)
        )
        reviews = models.Review.objects.filter(ticket__in=tickets)
        reviewed_ticket_ids = set(reviews.values_list('ticket_id', flat=True))
        tickets_and_reviews = sorted(
            chain(tickets, reviews),
            key=lambda instance: instance.date_created if isinstance(instance, models.Ticket) else instance.time_created,
            reverse=True
        )

        paginator = Paginator(tickets_and_reviews, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'tickets_and_reviews': page_obj,
            'reviewed_ticket_ids': reviewed_ticket_ids,
        }

        return render(request, self.template_name, context=context)
    
class PostsPage(LoginRequiredMixin, View):
    template_name = 'flux/posts.html'

    def get(self, request):
        tickets = models.Ticket.objects.filter(author=request.user)
        reviews = models.Review.objects.filter(user=request.user)
        tickets_and_reviews = sorted(
            chain(tickets, reviews),
            key=lambda instance: instance.date_created if isinstance(instance, models.Ticket) else instance.time_created,
            reverse=True
        )
        paginator = Paginator(tickets_and_reviews, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, context={'tickets_and_reviews': page_obj})
    
class SubscriptionsPage(LoginRequiredMixin, View):
    template_name = 'flux/subscriptions.html'
    form_class = forms.FollowUsersForm

    def get(self, request):
        form = self.form_class()
        users_followed = auth_models.User.objects.filter(followed_by__user=request.user)
        users_following = auth_models.User.objects.filter(follows__user_followed=request.user)

        context = {
            'form': form,
            'users_followed': users_followed,
            'users_following': users_following,
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request):
        form = self.form_class(request.POST)
        users_followed = auth_models.User.objects.filter(followed_by__user=request.user)
        users_following = auth_models.User.objects.filter(follows__user_followed=request.user)

        context = {
            'form': form,
            'users_followed': users_followed,
            'users_following': users_following,
        }
        if form.is_valid():
            if form.cleaned_data['user_to_follow'] == request.user.username:
                form.add_error('user_to_follow', "Vous ne pouvez pas vous suivre vous-même.")
                return render(request, self.template_name, context=context)
            user_to_follow = auth_models.User.objects.filter(username=form.cleaned_data['user_to_follow']).first()
            if not user_to_follow:
                form.add_error('user_to_follow', "Cet utilisateur n'existe pas.")
                return render(request, self.template_name, context=context)
            if models.UserFollows.objects.filter(user=request.user, user_followed=user_to_follow).exists():
                form.add_error('user_to_follow', "Vous suivez déjà cet utilisateur.")
                return render(request, self.template_name, context=context)
            models.UserFollows.objects.create(user=request.user, user_followed=user_to_follow)
            return redirect('flux:subscriptions')
        return render(request, self.template_name, context=context)
    
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
            return redirect('flux:posts')
        return render(request, self.template_name, context={'form': form})
    
class EditTicketPage(LoginRequiredMixin, View):
    template_name = 'flux/edit_ticket.html'
    edit_form_class = forms.TicketForm

    def get(self, request, ticket_id):
        ticket = get_object_or_404(models.Ticket, id=ticket_id)
        if ticket.author != request.user:
            return redirect(settings.LOGIN_REDIRECT_URL)
        edit_form = self.edit_form_class(instance=ticket)
        context = {
            'edit_form': edit_form,
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request, ticket_id):
        ticket = get_object_or_404(models.Ticket, id=ticket_id)
        if ticket.author != request.user:
            return redirect(settings.LOGIN_REDIRECT_URL)
        edit_form = self.edit_form_class(request.POST, request.FILES, instance=ticket)
        if edit_form.is_valid():
            edit_form.save(commit=False)
            ticket.date_edited = timezone.now()
            edit_form.save()
            return redirect('flux:posts')
        context = {
            'edit_form': edit_form,
        }
        return render(request, self.template_name, context=context)
    
class TicketDeleteView(LoginRequiredMixin, View):

    def post(self, request, ticket_id):
        ticket = get_object_or_404(models.Ticket, id=ticket_id)
        if ticket.author != request.user:
            return redirect(settings.LOGIN_REDIRECT_URL)
        ticket.delete()
        return redirect('flux:posts')
    
class SubscriptionDeleteView(LoginRequiredMixin, View):

    def post(self, request, user_followed_id):
        user_followed = get_object_or_404(auth_models.User, id=user_followed_id)
        subscription = get_object_or_404(models.UserFollows, user=request.user, user_followed=user_followed)
        subscription.delete()
        return redirect('flux:subscriptions')
    
class CreateReviewPage(LoginRequiredMixin, View):
    template_name = 'flux/create_review.html'
    review_form_class = forms.ReviewForm
    ticket_form_class = forms.TicketForm

    def get(self, request):
        review_form = self.review_form_class()
        ticket_form = self.ticket_form_class()
        context = {
            'review_form': review_form,
            'ticket_form': ticket_form,
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request):
        review_form = self.review_form_class(request.POST)
        ticket_form = self.ticket_form_class(request.POST, request.FILES)
        if review_form.is_valid() and ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.author = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect(settings.LOGIN_REDIRECT_URL)
        context = {
            'review_form': review_form,
            'ticket_form': ticket_form,
        }
        return render(request, self.template_name, context=context)
    
class CreateReviewForTicketPage(LoginRequiredMixin, View):
    template_name = 'flux/create_review_for_ticket.html'
    review_form_class = forms.ReviewForm

    def get(self, request, ticket_id):
        ticket = get_object_or_404(models.Ticket, id=ticket_id)
        if models.Review.objects.filter(ticket=ticket).exists():
            return redirect(settings.LOGIN_REDIRECT_URL)
        review_form = self.review_form_class()
        context = {
            'form': review_form,
            'ticket': ticket,
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request, ticket_id):
        ticket = get_object_or_404(models.Ticket, id=ticket_id)
        if models.Review.objects.filter(ticket=ticket).exists():
            return redirect(settings.LOGIN_REDIRECT_URL)
        review_form = self.review_form_class(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect(settings.LOGIN_REDIRECT_URL)
        context = {
            'form': review_form,
            'ticket': ticket,
        }
        return render(request, self.template_name, context=context)
    
class ReviewDeleteView(LoginRequiredMixin, View):

    def post(self, request, review_id):
        review = get_object_or_404(models.Review, id=review_id)
        review.delete()
        return redirect(settings.LOGIN_REDIRECT_URL)
    
class EditReviewPage(LoginRequiredMixin, View):
    template_name = 'flux/edit_review.html'
    edit_form_class = forms.ReviewForm

    def get(self, request, review_id):
        review = get_object_or_404(models.Review, id=review_id)
        ticket = get_object_or_404(models.Ticket, id=review.ticket_id)
        edit_form = self.edit_form_class(instance=review)
        context = {
            'edit_form': edit_form,
            'ticket': ticket,
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request, review_id):
        review = get_object_or_404(models.Review, id=review_id)
        ticket = get_object_or_404(models.Ticket, id=review.ticket_id)
        edit_form = self.edit_form_class(request.POST, instance=review)
        if edit_form.is_valid():
            edit_form.save(commit=False)
            review.time_edited = timezone.now()
            edit_form.save()
            return redirect(settings.LOGIN_REDIRECT_URL)
            
        context = {
            'edit_form': edit_form,
            'ticket': ticket,
        }
        return render(request, self.template_name, context=context)