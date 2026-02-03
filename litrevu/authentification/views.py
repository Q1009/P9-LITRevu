from django.shortcuts import render
from django.http import HttpResponse
from authentification.models import User
from authentification.forms import UserForm
from django.shortcuts import redirect

# Create your views here.
def login_view(request):
    users = User.objects.all()

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            email = user_form.cleaned_data['email']
            password = user_form.cleaned_data['password']
            # Here you would typically authenticate the user
            # For simplicity, we just print the credentials
            for user in users:
                if user.email == email and user.password == password:
                    print(f"Email: {email}, Password: {password}")
                    return redirect('flux')  # Redirect to flux view after login
                else:
                    print("Invalid credentials")
    else:
        user_form = UserForm()

    return render(request, 'authentification/login.html', {'users': users, 'user_form': user_form})

def subscribe_view(request):
    return render(request, 'authentification/subscribe.html')

def about_view(request):
    return HttpResponse('<h1>This is the about view.</h1> <p>Welcome to the LITRevu application!</p>')
