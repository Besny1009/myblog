# -*- coding: utf-8 -*-

from django.urls import path
from blog import views

app_name = 'blog'
urlpatterns = [
    path('', views.index),
    path('articalList', views.getArticalList),
    path('articalDetail', views.articalDetail),
    path('tagSearch', views.getTagSearch),
    path('getSearch', views.getSearch),
]