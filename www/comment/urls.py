# -*- coding: utf-8 -*-

from django.urls import path
from .views import CommentView


app_name = 'comment'

urlpatterns = [
    # 发表评论
    path('post-comment/<int:post_id>/', CommentView.as_view(), name='post_comment'),
]