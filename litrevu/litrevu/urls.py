"""
URL configuration for litrevu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from authentification import views as auth_views
from flux import views as flux_views
from subscriptions import views as subs_views
from posts import views as posts_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.login_view, name='login'),
    path('subscribe/', auth_views.subscribe_view, name='subscribe'),
    path('about/', auth_views.about_view, name='about'),
    path('flux/', flux_views.flux_view, name='flux'),
    path('subscriptions/', subs_views.subscriptions_view, name='subscriptions'),
    path('posts/', posts_views.posts_view, name='posts'),
]
