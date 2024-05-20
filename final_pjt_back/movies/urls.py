from django.urls import path
from . import views

urlpatterns = [
  path('getMovies/', views.getMovieData),
  path('getNowPlayingMovies/', views.getNowPlayingMovieData),
  path('getGenres/', views.getGenreData),
  path('movies/popular/', views.popular, name='popular'),
  path('movies/late_release/', views.late_release, name='late_release'),
  path('movies/<int:movie_id>/', views.comment_list),
  path('movies/<int:movie_id>/<int:comment_id>/', views.comment_detail),
  path('movies/<int:movie_id>/comments/create/', views.comment_create)
]