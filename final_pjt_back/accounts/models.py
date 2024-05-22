from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from movies.models import Movie

class User(AbstractUser):
    followings = models.ManyToManyField(settings.AUTH_USER_MODEL, symmetrical=False, related_name="followers")
    recent_watched_movie = models.ManyToManyField(Movie, related_name="watched_users")
    like_movies = models.ManyToManyField(Movie, related_name="like_users")
    recommendation_movie = models.ManyToManyField(Movie, related_name="recommended_users")
    introduce = models.TextField(blank=True, null=True)
    mbti = models.CharField(max_length=4, blank=True, null=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    updated_at = models.DateTimeField(null=True)
    see = models.BooleanField(default=True)