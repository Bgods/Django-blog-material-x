# -*- coding: utf-8 -*-

from blog.models import Tag, Links, Advertising, SidebarMusic
from django import template
from django.db.models.aggregates import Count
from blog.models import SiteSettings
register = template.Library()


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


# 侧边栏音乐配置
@register.simple_tag
def get_music():
    return SidebarMusic.objects.filter(enable=True).first()


# 站点配置
@register.simple_tag
def get_site_configs():
    """
    :return: dict
    """
    Settings = SiteSettings.objects.filter(is_show=True)
    return {s.name: s.value for s in Settings}
