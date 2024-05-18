from django.urls import path
from . import views

urlpatterns = [
  path('getMovies/', views.getMovieData),
  path('getGenres/', views.getGenreData),
]