import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render
from django.conf import settings
from django.utils import timezone
from .serializers import MovieSerializer, CommentSerializer, GenreSerializer
from .models import Movie
from .models import Genre
from .models import Comment

# Create your views here.
def getMovieData(request):

  for i in range(1, 501):
    url = f"https://api.themoviedb.org/3/movie/popular?language=ko&page={i}"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {settings.TMDB_TOKEN}"
    }

    response = requests.get(url, headers=headers)
    movies_data = response.json() 

    for movie in movies_data['results']:
      if movie['release_date'] == "":
        continue
      if not movie['poster_path']:
        continue
      movie_obj, created = Movie.objects.get_or_create(
        id=movie['id'],
        defaults={
          'title': movie['title'],
          'overview': movie['overview'],
          'release_data': movie['release_date'],
          'poster_path': movie['poster_path'],
          'vote_average': movie['vote_average'],
          'popularity': movie['popularity'],
          'adult': movie['adult'],
          'runtime': movie.get('runtime', 0)
        }
      )
        
      if created:
        print(f'Created movie: {movie["title"]}')
      else:
        print(f'Movie already exists: {movie["title"]}')

      for genre_id in movie['genre_ids']:
        try:
          genre_obj = Genre.objects.get(id=genre_id)
          movie_obj.genre.add(genre_obj)
        except Genre.DoesNotExist:
          print(f'Genre with id {genre_id} does not exist.')
                
      print(i)
  return render(request, 'getData.html')

def getNowPlayingMovieData(request):

  for i in range(1, 501):
    url = f"https://api.themoviedb.org/3/movie/now_playing?language=ko&page={i}"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {settings.TMDB_TOKEN}"
    }

    response = requests.get(url, headers=headers)
    movies_data = response.json() 

    for movie in movies_data['results']:
      if movie['release_date'] == "":
        continue
      if not movie['poster_path']:
        continue
      movie_obj, created = Movie.objects.get_or_create(
        id=movie['id'],
        defaults={
          'title': movie['title'],
          'overview': movie['overview'],
          'release_data': movie['release_date'],
          'poster_path': movie['poster_path'],
          'vote_average': movie['vote_average'],
          'popularity': movie['popularity'],
          'adult': movie['adult'],
          'runtime': movie.get('runtime', 0)
        }
      )
        
      if created:
        print(f'Created movie: {movie["title"]}')
      else:
        print(f'Movie already exists: {movie["title"]}')

      for genre_id in movie['genre_ids']:
        try:
          genre_obj = Genre.objects.get(id=genre_id)
          movie_obj.genre.add(genre_obj)
        except Genre.DoesNotExist:
          print(f'Genre with id {genre_id} does not exist.')
                
      print(i)
  return render(request, 'getData.html')

def getGenreData(request):
    url = "https://api.themoviedb.org/3/genre/movie/list?language=en"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {settings.TMDB_TOKEN}"
    }

    response = requests.get(url, headers=headers)
    genres_data = response.json()
    
    for genre in genres_data['genres']:
        Genre.objects.get_or_create(
            id=genre['id'],
            defaults={'name': genre['name']}
        )

    return render(request, 'getData.html')

@api_view(['GET'])
def popular(request): # 인기 영화 조회
  popular_movies = Movie.objects.order_by('-popularity')[:10]
  serializer = MovieSerializer(popular_movies, many=True)
  return Response(serializer.data)

@api_view(['GET'])
def late_release(request): # 최근 개봉한 영화 조회
  today = timezone.now().date()
  late_movies = Movie.objects.filter(release_data__lte=today).exclude(overview="").order_by('-release_data')[:10]
  serializer = MovieSerializer(late_movies, many=True)
  return Response(serializer.data)

@api_view(['GET'])
def search_movie(request, movie_name): # 영화 제목으로 영화 조회
  find_movies = Movie.objects.filter(title__icontains=movie_name)
  serializer = MovieSerializer(find_movies, many=True)
  return Response(serializer.data)

@api_view(['GET'])
def search_genre(request, genre_id):
  genre = Genre.objects.get(id = genre_id)
  serializer = GenreSerializer(genre)
  return Response(serializer.data)

@api_view(['GET'])
def comment_list(request, movie_id): # 해당 movie_id의 모든 댓글 조회
  if request.method == 'GET': 
    comments = Comment.objects.filter(movie_id=movie_id)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)
  
@api_view(['POST'])
def comment_create(request, movie_id): # 해당 movie_id에 댓글 작성
  if request.method == 'POST': 
    movie = Movie.objects.get(pk=movie_id)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save(movie=movie, user=request.user)
      return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'DELETE', 'PUT']) 
def comment_detail(request, movie_id, comment_id,): # 단일 댓글 조회, 삭제, 수정
  comment = Comment.objects.get(pk=comment_id)
  if request.method == 'GET':
    serializer = CommentSerializer(comment)
    return Response(serializer.data)
  
  elif request.method == 'DELETE':
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
  
  elif request.method == 'PUT':
    serializer = CommentSerializer(comment, data=request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
      return Response(serializer.data)