from django.shortcuts import render
from .serializers import UserSerializer, UserUpdateSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_profile(request):
    print(request.user)
    user = request.user
    serializers = UserSerializer(user)
    return Response(serializers.data)


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