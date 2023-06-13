from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from .forms import RegistrationForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import openai
from .models import MovieRating
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


# Create your views here.
def hello_world(request):
    return render(request, 'hello_world.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # authenticate user
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # log user in and redirect
                login(request, user)
                return redirect('hello_world')
            
            form.add_error(None, "Invalid username or password")
    else:
        form = AuthenticationForm()
        
    context = {'form': form}
    return render(request, 'login.html', context)

class RegistrationView(FormView):
    template_name = 'register.html'
    form_class = RegistrationForm
    success_url = '/login/'

    def form_valid(self, form):
        # Get cleaned form data
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        
        # If any cleaned data is missing, return an error 
        if not username or not email or not password:
            form.add_error(None, "Missing required form data")
            return super().form_invalid(form)
        
        # Create and save user object to database
        try:
            user = User.objects.create(username=username, email=email)
        except IntegrityError:
            # If username already exists, display error message
            form.add_error('username', "Username already exists. Please choose a different username.")
            return super().form_invalid(form)
            
        user.set_password(password)
        user.save()
        return super().form_valid(form)


############Chat GPT View################
@csrf_exempt
def chat_view(request):
    if request.method == 'POST':
        prompt = "i have watched and rated these movies as follows:"
        ratings = MovieRating.objects.filter(user=request.user)
        for rating in ratings:
            prompt = prompt+ f"- {rating.title}: {rating.rating}/10"

        prompt = prompt + request.POST.get('prompt')
        # You need to replace 'your-openai-api-key' with your actual OpenAI API key
        openai.api_key = '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'
        response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ]
        )
        return JsonResponse({'response': response['choices'][0]['message']['content']})
    else:
        return render(request, 'chat.html')

##Movie Listings and Ratings
@login_required
@csrf_exempt
def rate_movies_view(request):
    url = "https://api.themoviedb.org/3/movie/top_rated"
    params = {"api_key": "6ac0507d9d45e4dc150f01782356bd60"}
    numbers = list(range(1, 11))
    response = requests.get(url, params=params)
    data = response.json()
    # retrieve movie list from API response
    movie_list = data["results"]
    titles = []

    for movie in movie_list:
        title = movie["title"]
        titles.append(title)

    if request.method == 'POST':
        ratings = dict(request.POST.items())  # Convert to dict so we can modify
        ratings.pop('csrfmiddlewaretoken', None)  # Remove CSRF token
        for title, rating in ratings.items():
            movie_rating = MovieRating(user=request.user, title=title, rating=rating)
            movie_rating.save()
        return JsonResponse({'message': 'Ratings received'})
    else:
        return render(request, 'rate_movies.html', {'movies': titles, 'numbers': numbers})

##Users movie ratings list
def user_ratings(request):
    user_ratings = MovieRating.objects.filter(user=request.user)
    rating_list = [(rating.title, rating.rating) for rating in user_ratings]
    context = {"rating_list": rating_list}
    return render(request, "user_ratings.html", context)