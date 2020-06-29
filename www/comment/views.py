# -*- coding: utf-8 -*-

from comment.models import Comment
from django.shortcuts import redirect
from django.views import View
from django.core.mail import EmailMultiAlternatives
import re
import os
import random
from www.settings import HTTP_HOST, EMAIL_HOST_USER


class CommentView(View):
    #  处理POST请求
    def post(self, request):
        comment = Comment()  # 实例化类
        comment.post_id = request.POST['post_id']
        comment.parent_id = request.POST['parent_id']
        comment.reply_id = request.POST['reply_id']
        comment.nick = request.POST['nick']
        comment.mail = request.POST['mail']
        comment.content = request.POST['content']
        ua = request.META.get('HTTP_USER_AGENT', '')
        print(ua)

        # 从请求头中匹配客户端及浏览器
        browser = re.findall(r'([a-z]+/[0-9\.]+)[a-z ]*Safari/[0-9\.]+$', ua, re.I)
        if browser:
            comment.browser = browser[0]
        else:
            comment.browser = 'Unknown Browser'

        client = re.findall(r'Mozilla/5.0 \((.*?)\)', ua, re.I)
        if client:
            comment.client = client[0]
        else:
            comment.client = 'Unknown Client'

        redirect_url = HTTP_HOST + request.POST['redirect_url']

        # 处理回复评论
        if request.POST['reply_id'] != '0':
            comment.comment_type = 'reply'
            reply_comment = Comment.objects.filter(id=request.POST['reply_id']).first()
            if reply_comment:
                comment.to_nick = reply_comment.nick
                comment.to_mail = reply_comment.mail
                # 如果是回复评论，则发送邮件通知相关评论人
                send_email(url=redirect_url, recipient_list=[reply_comment.mail])
        else:
            # 如果是新的评论内容，则发送通知博客作者
            send_email(url=redirect_url, recipient_list=[EMAIL_HOST_USER])

        comment.avatar = get_avatar(request.POST['mail'])
        comment.save()  # 保存评论数据到数据库
        return redirect(request.POST['redirect_url'])  # 重定向到指定页面

    def get(self, request):
        pass


# 获取评论用户头像
def get_avatar(mail):
    try:
        # 1、判断该用户头像是否存在
        comment = Comment.objects.filter(mail=mail).first()
        if comment:
            if comment.avatar:
                return comment.avatar

        # 2、如果是新用户，则随机分配一个头像
        path = r'static/images/comment_avatar'  # 头像保存在项目下的静态文件static路径中
        comment_avatar_list = os.listdir(path=path)
        if comment_avatar_list:
            comment_avatar = random.choice(comment_avatar_list)  # 随机取一个头像分配给评论用户
            return '/{0}/{1}'.format(path, comment_avatar)
        else:
            return ''
    except:
        return ''


# 发送邮件
def send_email(url, recipient_list):

    subject = '来自博客的留言'   # 邮件主题
    html_content = '<p>你好，你在博客中的留言有了新的回复内容! <a href="{0}" target="_blank">点击查看</a></p>'.format(url)  # 邮件正文
    msg = EmailMultiAlternatives(
        subject=subject,
        body=html_content,
        from_email=EMAIL_HOST_USER,
        to=recipient_list
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send()  # 发送
