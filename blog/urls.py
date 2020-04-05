# -*- coding: utf-8 -*-

from django.urls import path
from blog import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('articalList', views.getArticalList),
    path('articalDetail', views.articalDetail),
    path('tagSearch', views.getTagSearch),
    path('getSearch', views.getSearch),
    path('list-<int:lid>.html', views.list, name='list'),
    path('show-<int:aid>.html', views.show, name='show'),
    path('tag/<str:tname>', views.tags, name='tags'),
    path('s/', views.search, name='search'),
]