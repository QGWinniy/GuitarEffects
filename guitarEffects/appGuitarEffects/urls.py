from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('songs/<int:song_id>/', views.song_detail, name='song_detail'),
    path('group/<int:group_id>/', views.group_detail, name='group_detail'),
    path('search/', views.search_results),
]