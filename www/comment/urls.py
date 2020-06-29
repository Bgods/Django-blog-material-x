# -*- coding: utf-8 -*-

from django.urls import path
from .views import CommentView


app_name = 'comment'


urlpatterns = [
    path('add/', CommentView.as_view(), name='add_comment'),
]
