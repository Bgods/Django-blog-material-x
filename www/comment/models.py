# -*- coding:utf-8 -*-
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from blog.models import Post
import os
import random

app_name = 'comment'


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, blank=True, null=True, verbose_name=u'文章')
    parent_id = models.IntegerField(blank=True, default=0, verbose_name=u'父级评论id')
    reply_id = models.IntegerField(blank=True, default=0, verbose_name=u'回复id')

    content = RichTextUploadingField(verbose_name=u'评论内容', config_name='comment')
    comment_type = models.CharField(
        max_length=10,
        choices=(('comment', u'评论'),
                 ('reply', u'回复'),
                 ),
        default='comment',
        verbose_name=u'评论类型',
    )
    add_time = models.DateTimeField(blank=True, auto_now_add=True, verbose_name=u'评论时间')

    mail = models.EmailField(verbose_name=u'评论用户邮箱')
    nick = models.CharField(max_length=20, verbose_name=u'评论用户名')

    to_mail = models.EmailField(null=True, blank=True, verbose_name=u'目标用户邮箱')
    to_nick = models.CharField(max_length=20, null=True, blank=True, verbose_name=u'目标用户名')
    browser = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'浏览器')
    client = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'客户端')
    avatar = models.CharField(max_length=200, null=True, blank=True, verbose_name=u'头像')

    is_show = models.BooleanField(default=True, verbose_name=u'是否显示评论')

    def __str__(self):
        return str(self.post_id)

    class Meta:
        ordering = ['post_id', 'add_time']
        verbose_name = u'评论内容'
        verbose_name_plural = u'评论内容'

    def save(self, *args, **kwargs):
        self.avatar = get_avatar(self.mail)  # 获取头像
        super().save(*args, **kwargs)


# 获取评论用户头像
def get_avatar(mail):
    def get_avatar_files(file_path):  # 获取路径中的头像文件名
        if os.path.exists(file_path):
            files_list = []
            for root, dirs, files in os.walk(file_path):
                for file in files:
                    # 筛选图片类型
                    file_type = os.path.splitext(file)[1]
                    if file_type.lower() in ['.png', '.jpg', '.jpeg']:
                        files_list.append(file)
            return files_list
        else:
            return []

    try:
        # 1、判断该用户头像是否存在
        comment = Comment.objects.filter(mail=mail).first()
        if comment:
            if comment.avatar:
                return comment.avatar

        # 2、如果是新用户，则随机分配一个头像
        path = r'static/comment_avatar'  # 静态文件static路径
        comment_avatar_list = get_avatar_files(file_path=path)

        if not comment_avatar_list:  # 如果路径中匹配不到，则从app的静态文件路径查找
            comment_avatar_list = get_avatar_files(file_path='comment/' + path)

        if comment_avatar_list:
            comment_avatar = random.choice(comment_avatar_list)  # 随机取一个头像分配给评论用户
            return '/{0}/{1}'.format(path, comment_avatar)

        return ''
    except BaseException as e:
        print(e)
        return ''
