from django.shortcuts import render
import requests
from django.conf import settings
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
          'runtime': movie.get('runtime', 0)  # runtime이 없을 경우 0으로 설정합니다.
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
