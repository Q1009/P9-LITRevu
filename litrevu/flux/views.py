from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class HomePage(LoginRequiredMixin, View):
    template_name = 'flux/home.html'

    def get(self, request):
        return render(request, self.template_name)
    
class PostsPage(LoginRequiredMixin, View):
    template_name = 'flux/posts.html'

    def get(self, request):
        return render(request, self.template_name)
    
class SubscriptionsPage(LoginRequiredMixin, View):
    template_name = 'flux/subscriptions.html'

    def get(self, request):
        return render(request, self.template_name)