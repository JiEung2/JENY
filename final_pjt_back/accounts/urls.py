from django.urls import path
from . import views

urlpatterns = [
    path('my_profile/', views.my_profile),
    path('update_profile/', views.update_profile),
]