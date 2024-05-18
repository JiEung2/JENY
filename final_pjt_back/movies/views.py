from django.shortcuts import render
import requests
from django.conf import settings

# Create your views here.
def getMovieData(request):

  url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"

  headers = {
      "accept": "application/json",
      "Authorization": f"Bearer {settings.TMDB_TOKEN}"
  }

  response = requests.get(url, headers=headers)
  print(response.text)

  return render(request)