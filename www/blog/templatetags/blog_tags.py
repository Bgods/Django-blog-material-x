# -*- coding: utf-8 -*-

from blog.models import Post, Tag, Links, Advertising
from django import template
from django.db.models.aggregates import Count
from www.settings import SITE_CONFIGS

register = template.Library()

# 获取最新5个评论
@register.simple_tag
def get_recent_comments(num=5):
    comments = Comment.objects.filter(is_show=True).order_by('-created_time')[:num]
    return comments


# 获取最新5篇文章
@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.filter(is_show=True).order_by('-created_time')[:num]

# 获取文章归档
@register.simple_tag
def get_archives():
    return Post.objects.filter(is_show=True).dates('created_time', 'month', order='DESC')


@register.simple_tag
def get_tags():
    # 使用 Count 方法统计文章数，并保存到 num_posts 属性中
    tags_style = [
        "font-size:19px;color:#777",
        "font-size:14px;color:#999",
        "font-size:16.5px;color:#888",
        "font-size:24px;color:#555",
        "font-size:21.5px;color:#666"
    ]
    tags = Tag.objects.filter(post__is_show=True).annotate(num_posts=Count('post')).filter(num_posts__gt=0).order_by('-num_posts')[:20]
    return {'tags_style':tags_style, 'tags':tags}


# 获取友情链接
@register.simple_tag
def get_links():
    return Links.objects.filter(is_show=True)


# 获取广告链接
@register.simple_tag
def get_advertising():
    return Advertising.objects.filter(is_show=True)


# 站点配置
@register.simple_tag
def get_site_configs():
    return SITE_CONFIGS
