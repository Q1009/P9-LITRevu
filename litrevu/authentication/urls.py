from django.urls import path
from authentication import views

app_name = 'authentication'

urlpatterns = [
    path('', views.LoginPage.as_view(), name='login'),
    path('signup/', views.SignupPage.as_view(), name='signup'),
    path('logout', views.LogoutPage.as_view(), name='logout'),
]