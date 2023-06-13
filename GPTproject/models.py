from django.db import models
from django.contrib.auth.models import User

class Registration(models.Model):
    username = models.CharField(default="",max_length=100)
    email = models.EmailField(default="")
    password = models.CharField(default="",max_length=100)

    def __str__(self):
        return self.username


class MovieRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    rating = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} rated {self.title} {self.rating}/10"