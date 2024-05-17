from django.db import models
from django.conf import settings
from accounts.models import User 

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    release_data = models.DateField()
    poster_path = models.TextField()
    vote_average = models.FloatField()
    adult = models.BooleanField()
    runtime = models.IntegerField()

class Thrown_Movie(models.Model):
    to_user_id = models.ManyToManyField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    from_user_id = models.ManyToManyField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="movie_comment")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Genre(models.Model):
    id = models.IntegerField()
    name = models.CharField(max_length=100)

