# -*- coding:utf-8 -*-
from django.db import models
import markdown
from mdeditor.fields import MDTextField
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension

app_name = 'comment'


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, verbose_name=u'博客')
    parent_id = models.IntegerField(blank=True, default=0, verbose_name=u'父级评论id')
    reply_id = models.IntegerField(blank=True, default=0, verbose_name=u'回复id')

    content = MDTextField(verbose_name=u'评论内容')
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

    to_mail = models.EmailField(null=True, verbose_name=u'目标用户邮箱')
    to_nick = models.CharField(max_length=20, null=True, verbose_name=u'目标用户名')

    browser = models.CharField(max_length=100, null=True, verbose_name=u'浏览器')
    client = models.CharField(max_length=100, null=True, verbose_name=u'客户端')
    avatar = models.URLField(null=True, verbose_name=u'头像')

    is_show = models.BooleanField(default=True, verbose_name=u'是否显示评论')

    def __str__(self):
        return str(self.post_id)

    class Meta:
        ordering = ['post_id', 'add_time']
        verbose_name = u'评论内容'
        verbose_name_plural = u'评论内容'

    def get_markdown_content(self):
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ])
        return {
            'body': md.convert(self.content),
            'toc': md.toc,
        }
