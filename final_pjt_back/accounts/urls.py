from django.urls import path
from . import views

urlpatterns = [
    path('<int:user_id>/', views.myPage, name='mypage'),
    path('my_profile/', views.my_profile),
    path('update_profile/', views.update_profile),
]