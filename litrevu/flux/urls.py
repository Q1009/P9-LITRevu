from django.urls import path
from flux import views

app_name = 'flux'

urlpatterns = [
    path('home/', views.HomePage.as_view(), name='home'),
    path('posts/', views.PostsPage.as_view(), name='posts'),
    path('subscriptions/', views.SubscriptionsPage.as_view(), name='subscriptions'),
    path('create-ticket/', views.CreateTicketPage.as_view(), name='create_ticket'),
    path('edit-ticket/<int:ticket_id>/', views.EditTicketPage.as_view(), name='edit_ticket'),
]