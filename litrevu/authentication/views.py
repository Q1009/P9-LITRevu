from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.conf import settings
from . import forms

class LoginPage(View):

    form_class = forms.LoginForm
    template_name = 'authentication/login.html'

    def get(self, request):
        form = self.form_class()
        message = "Veuillez vous connecter pour accéder à votre flux."
        return render(request, self.template_name, context={'form': form, 'message': message})

    def post(self, request):
        form = self.form_class(request.POST)
        message = "Veuillez vous connecter pour accéder à votre flux."
        if form.is_valid():
            # Authentication logic
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                message = "Nom d'utilisateur ou mot de passe incorrect."
        return render(request, self.template_name, context={'form': form, 'message': message})
    
class LogoutPage(View):

    def get(self, request):
        logout(request)
        return redirect(settings.LOGIN_URL)
    
class SignupPage(View):
    
    form_class = forms.SignupForm
    template_name = 'authentication/signup.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        return render(request, self.template_name, context={'form': form})