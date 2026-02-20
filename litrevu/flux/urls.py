from django.urls import path
from flux import views

app_name = 'flux'

urlpatterns = [
    path('home/', views.HomePage.as_view(), name='home'),
    path('posts/', views.PostsPage.as_view(), name='posts'),
    path('subscriptions/', views.SubscriptionsPage.as_view(), name='subscriptions'),
]