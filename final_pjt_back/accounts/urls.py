from django.urls import path
from . import views

urlpatterns = [
    path('my_profile/', views.my_profile),
    path('user_profile/<int:user_id>/', views.user_profile),
    path('update_profile/', views.update_profile),
    path('follow/<int:user_id>/', views.follow),
    path('is_followed/<int:user_id>/', views.is_followed),
    path('get_followings/', views.get_followings),
]