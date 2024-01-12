from django.urls import path
from .views import PostView, Userview, UserBlockView



urlpatterns = [
    path('user/', Userview, name='user_url'),      # To create a User
    path('posts/', PostView.as_view(), name='post_urls'),
    path('posts/<int:pk>/', PostView.as_view(), name='post_urls'),
    path('block-user/', UserBlockView.as_view(), name='block_urls'),
]