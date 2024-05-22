from django.urls import path
from . import views

app_name='movies'
urlpatterns = [
  path('getMovies/', views.getMovieData),
  path('getGenres/', views.getGenreData),
  path('getNowPlayingMovies/', views.getNowPlayingMovieData),
  path('movies/popular/', views.popular, name='popular'),
  path('movies/popular_many/', views.popular_many, name='popular_many'),
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
  path('movies/<int:movie_id>/likes/', views.likes_movie, name='likes'),
  path('movies/both_like/<str:username>/', views.search_both_like, name='search_both_like'),
  path('throw/<int:movie_id>/<str:username>/', views.throw_movie, name='throw_movie'),
  path('thrown_movies/', views.thrown_movies, name='thrown_movies'),
  path('get_catched_movies/', views.get_catched_movies, name="catched_movies"),
  path('get_liked_movies/<str:username>/', views.liked_movies, name='my_like_movies'),
  path('get_sent_movies/', views.get_sent_movies, name="sent_movies"),
  path('get_liked_genres/', views.get_liked_genres, name="liked_genres"),
  path('movies/<int:movie_id>/get_is_liked/', views.get_is_liked, name="get_is_liked"),
]