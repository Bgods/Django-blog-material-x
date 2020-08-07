# -*- coding: utf-8 -*-

from comment.models import Comment
from django.shortcuts import redirect
from django.views import View
from django.core.mail import EmailMultiAlternatives
import re
from www.settings import EMAIL_RECEIVE_LIST, EMAIL_HOST_USER


class CommentView(View):
    #  处理POST请求
    def post(self, request, post_id):
        comment = Comment()  # 实例化类
        comment.post_id = post_id
        comment.parent_id = request.POST['parent_id']
        comment.reply_id = request.POST['reply_id']
        comment.nick = request.POST['nick']
        comment.mail = request.POST['mail']
        comment.content = request.POST['content']

        ua = parse_user_agent(request.META.get('HTTP_USER_AGENT', ''))  # 解析HTTP_USER_AGENT
        comment.browser = ua['browser']
        comment.client = ua['client']

        # 处理回复评论
        if request.POST['reply_id'] != '0':
            comment.comment_type = 'reply'
            reply_comment = Comment.objects.filter(id=request.POST['reply_id']).first()
            if reply_comment:
                comment.to_nick = reply_comment.nick
                comment.to_mail = reply_comment.mail

                # 如果是回复评论，则发送邮件通知相关评论人
                recipient_list = EMAIL_RECEIVE_LIST + [reply_comment.mail]
            else:
                recipient_list = None
        else:
            # 如果是新的评论内容，则只需要发送通知博客作者
            recipient_list = EMAIL_RECEIVE_LIST

        comment.save()  # 保存评论数据到数据库

        redirect_url = request.POST['redirect_url'] + '#comment-{0}'.format(comment.id)
        if recipient_list:  # 发送邮件
            try:
                send_email(url=redirect_url, recipient_list=recipient_list, post_id=post_id)
            except BaseException as e:
                print('发送邮件错误: {}'.format(e))
        return redirect(redirect_url)  # 重定向到指定页面

    def get(self, request):
        pass


def send_email(url, recipient_list, post_id):
    """
    发送邮件
    :param url: 评论内容链接
    :param recipient_list: 邮件接收人
    :return: None
    """
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


# 解析User-Agent
def parse_user_agent(user_agent):
    browser = re.findall(r'([a-z]+/[0-9\.]+)[a-z ]*Safari/[0-9\.]+$', user_agent, re.I)
    if browser:
        browser = browser[0]

    else:
        browser = 'Unknown Browser'

    client = re.findall(r'^[a-z]+/\d*.?\d* \((.*?)\)', user_agent, re.I)
    if client:
        client = client[0]
    else:
        client = 'Unknown Client'

    return {
        'browser': browser,
        'client': client
    }


