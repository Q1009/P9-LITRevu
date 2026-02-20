from django.urls import path
from flux import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'flux'

urlpatterns = [
    path('home/', views.HomePage.as_view(), name='home'),
    path('posts/', views.PostsPage.as_view(), name='posts'),
    path('subscriptions/', views.SubscriptionsPage.as_view(), name='subscriptions'),
    path('create-ticket/', views.CreateTicketPage.as_view(), name='create_ticket'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)