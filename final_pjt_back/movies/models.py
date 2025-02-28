from django.db import models
from django.conf import settings

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=100)

class Movie(models.Model):
    genre = models.ManyToManyField(Genre)
    title = models.CharField(max_length=100)
    overview = models.TextField()
    release_data = models.DateField()
    poster_path = models.TextField()
    vote_average = models.FloatField()
    popularity = models.FloatField()
    adult = models.BooleanField()
    runtime = models.IntegerField()

class Thrown_Movie(models.Model):
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="received_movies", on_delete=models.CASCADE)
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="sent_movies", on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

class Comment(models.Model):
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="movie_comment")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)