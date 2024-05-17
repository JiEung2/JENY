from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from movies.models import Movie

# Create your models here.
class User(AbstractUser):
    followings = models.ManyToManyField(settings.AUTH_USER_MODEL, symmetrical=False, related_name="followers")
    recent_watched_movie = models.ManyToManyField(Movie, related_name="watched_user")
    like_movies = models.ManyToManyField(Movie, related_name="like_users")
    