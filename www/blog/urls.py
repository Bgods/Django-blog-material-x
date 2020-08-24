# -*- coding: utf-8 -*-

from django.urls import path
from . import views as BlogViews

app_name = 'blog'

urlpatterns = [
    path('', BlogViews.Index().index, name='Index'),
    path('archives/', BlogViews.Archives, name='Archives'),
    path('tutorial/', BlogViews.Tutorial, name='Tutorial'),
    path('about/', BlogViews.About, name='About'),
    path('project/', BlogViews.Project, name='Project'),


    path('tags/<tag>/', BlogViews.Index().tags, name='tags'),
    path('post/<int:pk>/', BlogViews.Detail, name='post'),
    path('content.json/',BlogViews.search, name='search'),




]
