from django.urls import path
from flux import views

app_name = 'flux'

urlpatterns = [
    path('home/', views.HomePage.as_view(), name='home'),
    path('posts/', views.PostsPage.as_view(), name='posts'),
    path('subscriptions/', views.SubscriptionsPage.as_view(), name='subscriptions'),
    path('create-ticket/', views.CreateTicketPage.as_view(), name='create_ticket'),
    path('edit-ticket/<int:ticket_id>/', views.EditTicketPage.as_view(), name='edit_ticket'),
    path('create-review/', views.CreateReviewPage.as_view(), name='create_review'),
    path('create-review/<int:ticket_id>/', views.CreateReviewForTicketPage.as_view(), name='create_review_for_ticket'),
    path('unsubscribe/<int:user_followed_id>/', views.SubscriptionDeleteView.as_view(), name='unsubscribe'),
    path('delete-ticket/<int:ticket_id>/', views.TicketDeleteView.as_view(), name='delete_ticket'),
    path('delete-review/<int:review_id>/', views.ReviewDeleteView.as_view(), name='delete_review'),
    path('edit-review/<int:review_id>/', views.EditReviewPage.as_view(), name='edit_review'),
]