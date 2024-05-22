from django.urls import path
from . import views


urlpatterns = [
    path('<int:user_id>/', views.myPage, name='mypage'),
]