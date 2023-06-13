from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import hello_world, login_view, RegistrationView, chat_view, rate_movies_view, user_ratings
from django.urls import include


urlpatterns = [
    path('hello-world/', hello_world, name='hello_world'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('chat-with-gpt/', chat_view, name='chat_view'),
    path('rate-movies/', rate_movies_view, name='rate_movies_view'),
    path('user-ratings/', user_ratings, name = 'user_ratings')
]
