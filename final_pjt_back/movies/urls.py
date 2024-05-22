from django.urls import path
from . import views

app_name='movies'
urlpatterns = [
  path('getMovies/', views.getMovieData),
  path('getGenres/', views.getGenreData),
  path('getNowPlayingMovies/', views.getNowPlayingMovieData),
  path('movies/popular/', views.popular, name='popular'),
  path('movies/late_release/', views.late_release, name='late_release'),
  path('movies/getMovieDetail/<int:movie_id>/', views.getMovieDetail),
  path('movies/getMovieGenres/<int:movie_id>/', views.getMovieGenres),
  path('movies/getUserId/', views.getUserId),
  path('movies/<str:movie_name>/', views.search_movie, name='search_movie'),
  path('movies/<int:movie_id>/', views.comment_list),
  # path('genres/<int:genre_id>/', views.search_genre),
  path('movies/<int:movie_id>/comments/', views.comment_list),
  path('movies/<int:movie_id>/comments/<int:comment_id>/', views.comment_detail),
  # path('movies/<int:movie_id>/<int:comment_id>/', views.comment_detail),
  path('movies/<int:movie_id>/comments/create/', views.comment_create),
  path('movies/<int:movie_id>/review/wordcloud/', views.rewiew_wordcloud),
]