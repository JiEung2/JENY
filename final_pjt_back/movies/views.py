import requests
from collections import Counter
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from django.conf import settings
from django.utils import timezone
from krwordrank.word import summarize_with_keywords
from django.contrib.auth import get_user_model
from .serializers import MovieSerializer, CommentSerializer, GenreSerializer, ThrownMovieSerializer
from .models import Movie, Genre, Comment, Thrown_Movie
from django.shortcuts import get_object_or_404
from accounts.serializers import UserSerializer

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

# 인기 영화 조회
@api_view(['GET'])
def popular(request): 
    popular_movies = Movie.objects.order_by('-popularity')[:15]
    serializer = MovieSerializer(popular_movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# 초반 인기 영화 선택
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def popular_many(request):  
    user = request.user
    if user.see or (user.updated_at and (timezone.now() - user.updated_at).total_seconds() < 60):
        if user.is_selected:
            return Response(status=status.HTTP_200_OK)

        user.see = True
        user.save()
        popular_movies = Movie.objects.order_by('-popularity')[:100]
        serializer = MovieSerializer(popular_movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_200_OK)


# 더이상 보지 않음
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def no_see(request):
    user = request.user
    user.see = False
    user.updated_at = timezone.now()
    user.save()
    return Response(status=status.HTTP_200_OK)

# 최근 개봉한 영화 조회
@api_view(['GET'])
def late_release(request): 
    today = timezone.now().date()
    late_movies = Movie.objects.filter(release_data__lte=today).exclude(overview="").order_by('-release_data')[:10]
    serializer = MovieSerializer(late_movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# 영화 디테일 가져오기
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMovieDetail(request, movie_id):  
    movie = Movie.objects.filter(id=movie_id)
    serializer = MovieSerializer(movie, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# 영화 제목으로 영화 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_movie(request, movie_name): 
    find_movies = Movie.objects.filter(title__icontains=movie_name)
    serializer = MovieSerializer(find_movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# movie 좋아요
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def likes_movie(request, movie_id): 
    movie = Movie.objects.get(id = movie_id)
    user = request.user
    print(user)
    if user.like_movies.filter(id=movie.id).exists():
        user.like_movies.remove(movie)
        liked = False
    else:
        user.like_movies.add(movie)
        liked = True
    return Response({'liked': liked}, status=status.HTTP_200_OK)

# 여러 movie 좋아요
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_movies(request):
    user = request.user
    movie_ids = request.data.get('movies', [])
    for movie_id in movie_ids:
        movie = get_object_or_404(Movie, id=movie_id)
        user.like_movies.add(movie)
    user.is_selected = True
    user.save()
    return Response(status=status.HTTP_200_OK)

# 좋아요 누른 영화 반환
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def liked_movies(request, username):
    User = get_user_model()
    user = User.objects.get(username=username)
    movies = user.like_movies.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# 둘 다 좋아하는 영화 반환
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_both_like(request, username):
    User = get_user_model()
    user = User.objects.get(username=username)
    my_movies = set(request.user.like_movies.values_list('id', flat=True))
    user_movies = set(user.like_movies.values_list('id', flat=True))
    common_likes = my_movies.intersection(user_movies)
    movies = Movie.objects.filter(id__in=common_likes)
    serializer = MovieSerializer(movies, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

# 해당 movie_id의 모든 댓글 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def comment_list(request, movie_id): 
    if request.method == 'GET': 
        comments = Comment.objects.filter(movie_id=movie_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

# 해당 movie_id에 댓글 작성
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_create(request, movie_id): 
    if request.method == 'POST': 
        movie = Movie.objects.get(pk=movie_id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(movie=movie, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

# 단일 댓글 조회, 삭제, 수정
@api_view(['GET', 'DELETE', 'PUT']) 
@permission_classes([IsAuthenticated])
def comment_detail(request, movie_id, comment_id): 
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
    
# 영화의 장르 반환
@api_view(['GET'])
def getMovieGenres(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    serializer = MovieSerializer(movie)

    genre_ids = serializer.data["genre"]
    genre_names = Genre.objects.filter(id__in=genre_ids).values_list('name', flat=True)

    return Response(genre_names)

# 나의 아이디 반환
@api_view(['GET'])
def getUserId(request):
    user_id = request.user.id
    return Response(user_id)

# 영화 던지기
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def throw_movie(request, movie_id, username):
    from_user = request.user
    User = get_user_model()
    to_user = User.objects.get(username=username)
    if from_user != to_user:
        movie = Movie.objects.get(id=movie_id)
        Thrown_Movie.objects.create(
            to_user=to_user,
            from_user=from_user,
            movie=movie,
        )

        return Response({"message": "Movie throw successfully"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"message": "You can't throw yourself"}, status=status.HTTP_400_BAD_REQUEST)

# 받은 영화 반환
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def thrown_movies(request):
    user = request.user
    thrown_movie = Thrown_Movie.objects.filter(to_user=user, is_read=False).first()

    if thrown_movie:
        thrown_movie.is_read = True
        thrown_movie.save()
        serializer = ThrownMovieSerializer(thrown_movie)
        return Response(serializer.data)
    else:
        return Response({"detail": "받은 영화가 없습니다."}, status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_catched_movies(request):
    user = request.user
    thrown_movies = Thrown_Movie.objects.filter(to_user=user)
    serializer = ThrownMovieSerializer(thrown_movies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_sent_movies(request):
    user = request.user
    movies = Thrown_Movie.objects.filter(from_user=user)
    serializer = ThrownMovieSerializer(movies, many=True)
    # print(serializer.data)
    return Response(serializer.data)

# 장르를 좋아하고 있는지 반환
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_liked_genres(request, user_id):
    User = get_user_model()
    user = User.objects.get(id=user_id)
    movies = user.like_movies.all()
    genres_list = []

    for movie in movies:
        for genre in movie.genre.all():  # Assuming movie.genres is a ManyToMany field
            genres_list.append(genre.name)

    genre_count = Counter(genres_list)
    most_common_genres = genre_count.most_common()

    data = []
    for genre, count in most_common_genres:
        data.append([genre, count])
    return Response(data)

# 영화를 좋아하고 있는지 반환
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_is_liked(request, movie_id):
    try:
        movie = Movie.objects.get(id=movie_id)
    except Movie.DoesNotExist:
        return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)

    user = request.user
    is_liked = user.like_movies.filter(id=movie.id).exists()

    context = {
        'is_liked': is_liked
    }
    return Response(context, status=status.HTTP_200_OK)

# id로 유저 반환
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserName(request, user_id):
    try:
        User = get_user_model()
        user = User.objects.get(id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


# 추천 알고리즘
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommendation(request):
    user = request.user
    movies = user.like_movies.all()
    genres_list = []

    # Count genres from liked movies
    for movie in movies:
        for genre in movie.genre.all():
            genres_list.append(genre.name)

    genre_count = Counter(genres_list)
    most_common_genres = genre_count.most_common()

    recommended_movies = []
    recommended_movie_ids = set()

    # Fetch movies based on genre frequency and popularity
    for genre, count in most_common_genres:
        if len(recommended_movies) >= 10:
            break
        genre_movies = Movie.objects.filter(genre__name=genre).exclude(id__in=movies.values_list('id', flat=True)).order_by('-popularity')
        
        if genre == most_common_genres[0][0]:
            genre_movies = genre_movies[:5]
        elif genre == most_common_genres[1][0]:
            genre_movies = genre_movies[:3]
        elif genre == most_common_genres[2][0]:
            genre_movies = genre_movies[:2]

    for movie in genre_movies:
        if len(recommended_movies) < 10 and movie.id not in recommended_movie_ids:
            recommended_movies.append(movie)
            recommended_movie_ids.add(movie.id)
        else:
            break

    # If we don't have enough recommendations, fill the rest with popular movies
    if len(recommended_movies) < 10:
        needed = 10 - len(recommended_movies)
        popular_movies = Movie.objects.exclude(id__in=recommended_movie_ids).order_by('-popularity')[:needed]
        for movie in popular_movies:
            if movie.id not in recommended_movie_ids:
                recommended_movies.append(movie)
                recommended_movie_ids.add(movie.id)

    # Serialize the recommended movies
    serializer = MovieSerializer(recommended_movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def rewiew_wordcloud(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    reviews = movie.movie_comment.all()
    
    texts = []
    for review in reviews:
        texts.append(review.content)
    
    stopwords = {
        "정말", "너무", "좀", "기대했던", "특히", "정말로", "매우", "아주", "너무", "많이", 
        "다시", "더", "더러", "이", "있", "하", "것", "들", "그", "되", "수", "보", "않", "없", "나", "사람", "주", "아니", "등", 
        "같", "우리", "때", "년", "가", "한", "지", "대하", "오", "말", "일", "그렇", "위하", "때문", "그것", "두", "말하", "알", 
        "그러나", "받", "못하", "그런", "또", "문제", "사회", "많", "그리고", "좋", "크", "따르", "중", "나오", "가지", "씨", "시간", 
        "만들", "지금", "생각하", "그러", "속", "하나", "집", "살", "모르", "적", "월", "데", "자신", "안", "어떤", "내", "내", 
        "경우", "명", "생각", "시작", "우리", "다시", "이런", "그녀", "이러", "앞", "보이", "번", "나", "다른", "어떻", "전", "말", 
        "로", "이렇", "약", "분", "영화", "하게", "있어요.", "되는", "콩과",
    }
    keywords = summarize_with_keywords(texts, min_count=2, max_length=10, 
        beta=0.85, max_iter=10, stopwords=stopwords, verbose=True)
    wordlist = []

    for key, val in keywords.items():
        temp = [key, int(val*100)]
        wordlist.append(temp)

    return Response(wordlist)