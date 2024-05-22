from rest_framework import serializers
from django.conf import settings
from django.contrib.auth import get_user_model 

class UserSerializer(serializers.ModelSerializer):
    followings_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'followings_count', 'followers_count', 'introduce', 'mbti', 'image']

    def get_followings_count(self, obj):
        return obj.followings.count()

    def get_followers_count(self, obj):
        return obj.followers.count()
    
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['introduce', 'mbti', 'image']