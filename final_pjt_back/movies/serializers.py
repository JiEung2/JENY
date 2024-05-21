from rest_framework import serializers
from .models import Movie, Comment, Genre, Thrown_Movie
from django.conf import settings
from django.contrib.auth import get_user_model

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('movie', 'created_at', 'user',)

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class ThrownMovieSerializer(serializers.ModelSerializer):
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = ['id', 'username']

    movie = MovieSerializer()
    from_user = UserSerializer()
    to_user = UserSerializer()

    class Meta:
        model = Thrown_Movie
        fields = ['movie', 'from_user', 'to_user', 'created_at']