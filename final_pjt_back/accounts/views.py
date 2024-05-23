from django.shortcuts import render
from .serializers import UserSerializer, UserUpdateSerializer, FollowingsSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.shortcuts import get_object_or_404


# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_profile(request):
    print(request.user)
    user = request.user
    serializers = UserSerializer(user)
    return Response(serializers.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, id=user_id)
    serializers = UserSerializer(user)
    return Response(serializers.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    mbti = request.data.get('mbti', '')

    if len(mbti) != 4:
        return Response({'message': 'MBTI는 4자리여야 합니다.'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = UserUpdateSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow(request, user_id):
    User = get_user_model()
    person = get_object_or_404(User, id=user_id)
    if person != request.user:
        if person.followers.filter(id=request.user.id).exists():
            person.followers.remove(request.user)
            is_follow = False
        else:
            person.followers.add(request.user)
            is_follow = True
    return Response({'is_follow': is_follow}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def is_followed(request, user_id):
    user = request.user
    is_followed = user.followings.filter(id=user_id).exists()
    return Response({'is_followed': is_followed}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_followings(request):
    user = request.user

    followings = user.followings.annotate(
        throw_count=Count('sent_movies')
    ).order_by('-throw_count')[:10]

    serializer = FollowingsSerializer(followings, many=True)
    
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_user(request, username):
    User = get_user_model()
    user = get_object_or_404(User, username=username)
    serialzer = UserSerializer(user)
    return Response(serialzer.data)