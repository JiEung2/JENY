from django.urls import path
from . import views

urlpatterns = [
  path('getMovies/', views.getMovieData),
  path('getNowPlayingMovies/', views.getNowPlayingMovieData),
  path('getGenres/', views.getGenreData),
  path('movies/popular/', views.popular, name='popular'),
  path('movies/late_release/', views.late_release, name='late_release'),
]