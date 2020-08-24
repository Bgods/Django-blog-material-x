# -*- coding:utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models import Q


# Create your models here.
class Tag(models.Model):
    # 文章标签,继承 model.Model
    name = models.CharField(max_length=100, unique=True, verbose_name=u'标签')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'标签'
        verbose_name_plural = u'标签'


class Tutorial(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=u'教程')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'教程'
        verbose_name_plural = u'教程'


# 普通博文
class Post(models.Model):
    # 文章类型
    post_type = models.CharField(
        max_length=20,
        choices=(('post', u'博客文章'), ('about', u'关于本站'), ('project', u'我的项目')),
        default='post',
        verbose_name=u'类型'
    )

    title = models.CharField(max_length=100, verbose_name=u'标题')
    body = RichTextUploadingField(verbose_name=u'正文')
    created_time = models.DateTimeField(verbose_name=u'创建时间')
    modified_time = models.DateTimeField(auto_now=True, verbose_name=u'更新时间')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name=u'标签')  # 文章标签：一篇文章可以有多个标签，一对多关系，可为空
    tutorial = models.ForeignKey('Tutorial', null=True, blank=True, on_delete=models.SET_NULL, verbose_name=u'教程')  # 文章教程: 允许为空
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=u'作者')   # 文章作者：一篇文章只有一个作者，与文章一对一关系
    views = models.PositiveIntegerField(default=0, verbose_name=u'访问量')  # 文章访问量
    is_top = models.BooleanField(default=False, verbose_name=u'顶置文章')  # 文章是否顶置，默认不顶置
    is_show = models.BooleanField(default=True, verbose_name=u'发布状态')    # 文章发布状态，默认是创建成功就发布

    def get_next_field_by_created_time(self):  # 获取下一页
        post = Post.objects.filter(~Q(pk=self.pk), is_show=True, post_type='post', created_time__gte=self.created_time).order_by('created_time').first()
        return post

    def get_previous_field_by_created_time(self):
        post = Post.objects.filter(~Q(pk=self.pk), is_show=True, post_type='post', created_time__lte=self.created_time).order_by('-created_time').first()
        return post

    def __str__(self):
        return self.title

    # 自定义 get_absolute_url 方法
    def get_absolute_url(self):
        return reverse('blog:post', kwargs={'pk': self.pk})

    # 自定义 increase_views 方法：用于统计访问量
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    class Meta:
        # 获取 Post 列表时，按照顶置文章、创建时间排序
        ordering = ['-is_top', '-created_time']
        verbose_name = u'博客文章'
        verbose_name_plural = u'博客文章'

# 友情链接
class Links(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'站点名称')
    url = models.URLField(max_length=225, verbose_name=u'站点链接')
    is_show = models.BooleanField(default=True, verbose_name=u'是否展示')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'友情链接'
        verbose_name_plural = u'友情链接'


# 广告链接
class Advertising(models.Model):
    ad_name = models.CharField(max_length=100, verbose_name=u'广告名称')
    ad_url = models.URLField(max_length=225, verbose_name=u'广告链接')
    img_url = models.ImageField(upload_to='ad/', verbose_name='广告图片')
    is_show = models.BooleanField(default=True, verbose_name=u'是否推广')

    def __str__(self):
        return self.ad_name

    class Meta:
        verbose_name = u'广告链接'
        verbose_name_plural = u'广告链接'


# 侧边栏 - 音乐插件配置
class SidebarMusic(models.Model):
    server = models.CharField(
        max_length=20,
        choices=(('netease', u'网易云音乐'), ('tencent', u'QQ音乐'), ('xiami', u'虾米'), ('kugou', u'酷狗')),
        unique=True,
        default='netease',
        verbose_name=u'平台'
    )
    mode = models.CharField(
        max_length=20,
        choices=(('random', u'随机'), ('single', u'单曲'), ('circulation', u'列表循环'), ('order', u'列表')),
        default='random',
        verbose_name=u'播放模式'
    )
    type = models.CharField(
        max_length=20,
        choices=(('song', u'单曲'), ('album', u'专辑'), ('playlist', u'歌单'), ('search', u'搜索')),
        default='playlist',
        verbose_name=u'类型'
    )
    # 播放歌单id，获取方法自行百度。比如我的id就是链接后面的id，https://music.163.com/#/playlist?id=2700450552
    play_id = models.BigIntegerField(verbose_name=u'播放歌单id')
    home_url = models.URLField(null=True, blank=True, max_length=225, verbose_name=u'音乐主页')
    autoplay = models.BooleanField(default=True, verbose_name=u'自动播放')
    enable = models.BooleanField(default=True, verbose_name=u'启用插件')

    def __str__(self):
        return self.server

    class Meta:
        verbose_name = u'侧边栏音乐配置'
        verbose_name_plural = u'侧边栏音乐配置'


# 站点设置
class SiteSettings(models.Model):
    name = models.CharField(
        max_length=20,
        choices=(
            ('sitename', u'站点名称'),
            ('sitetitle', u'站点标题'),
            ('email', u'我的邮箱'),
            ('weibo', u'微博主页'),
            ('music', u'我的音乐主页'),
            ('twitter', u'Twitter'),
            ('github', u'GitHub'),
            ('beian', u'备案号'),
            ('baidu_tj', u'百度统计代码'),
        ),
        unique=True,
        verbose_name=u'名称'
    )
    value = models.TextField(verbose_name=u'值')
    is_show = models.BooleanField(default=True, verbose_name=u'是否展示')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']
        verbose_name = u'站点设置'
        verbose_name_plural = u'站点设置'
