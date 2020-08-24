# _*_ coding:utf-8 _*_

from django.shortcuts import render, get_object_or_404
from blog.models import Post, Tag
from comment.models import Comment
from comment.forms import CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.db.models.aggregates import Count
import json
from django.http import HttpResponse
from www.views import page_not_found


# 获取某篇文章的评论回复内容
def comment_reply_content(post_id):
    # 评论
    comments = Comment.objects.filter(is_show=True, post_id=post_id, comment_type='comment').order_by('pk')
    comments_dict = {'comments': {}, 'count': 0}
    for comment in comments:
        comments_dict['comments'][comment.id] = {
            'comment': {
                'id': comment.pk,
                'post_id': comment.post_id,
                'add_time': comment.add_time,
                'content': comment.content,
                'parent_id': comment.parent_id,
                'reply_id': comment.reply_id,
                'nick': comment.nick,
                'browser': comment.browser,
                'client': comment.client,
                'avatar': comment.avatar,
            },
            'reply': [],
        }
    # 回复
    replys = Comment.objects.filter(is_show=True, post_id=post_id, comment_type='reply').order_by('pk')
    for reply in replys:
        if reply.parent_id in comments_dict['comments'].keys():
            comments_dict['comments'][reply.parent_id]['reply'].append({
                'id': reply.pk,
                'post_id': reply.post_id,
                'add_time': reply.add_time,
                'content': reply.content,
                'parent_id': reply.parent_id,
                'reply_id': reply.reply_id,
                'nick': reply.nick,
                'to_nick': reply.to_nick,
                'browser': reply.browser,
                'client': reply.client,
                'avatar': reply.avatar,
            })
    comments_dict['count'] = len(replys) + len(comments)
    return comments_dict


# 博客文章列表页面
class Index(object):
    def __init__(self):
        # 定义 per_page 的值，每个页面的文章数
        self.per_page = 10

    def index(self, request):
        # 博客首页：获取Post表中所有文章列表
        post_list = Post.objects.filter(is_show=True, post_type='post')
        page = request.GET.get('page')
        return self.get_data(post_list=post_list, page=page, request=request)

    def tags(self, request, tag):
        # 标签：按照标签(tag)查询Post表中的文章列表
        post_list = Post.objects.filter(tags__name=tag, is_show=True, post_type='post')
        page = request.GET.get('page')
        return self.get_data(post_list=post_list, page=page, request=request)

    def get_data(self,post_list, page, request):
        post_list = self.Pagination(post_list=post_list, page=page)
        post_type = 'post'
        return render(request, 'blog/index.html', context={'post_list': post_list, 'post_type': post_type})

    # 高级分页扩展函数
    def Pagination(self, post_list, page):
        # 使用 Paginator 函数将post_list以每页per_page篇文章进行分页
        paginator = Paginator(post_list, self.per_page)
        try:
            post_list = paginator.page(page)
        except PageNotAnInteger:
            post_list = paginator.page(1)
        except EmptyPage:
            post_list = paginator.page(paginator.num_pages)
        return post_list


# 博客详情页
def Detail(request, pk):
    post = get_object_or_404(Post, pk=pk, is_show=True, post_type='post')
    post.increase_views()  # 调用 increase_views 方法，统计访问量
    comments_dict = comment_reply_content(post_id=pk)  # 评论回复
    comment_form = CommentForm()  # 引入评论表单
    context = {
        'post': post,
        'comments_dict': comments_dict,
        'comment_form': comment_form,
    }
    return render(request, 'blog/detail.html', context=context)


# 教程
def Tutorial(request):
    # 获取教程类型博文列表
    post_list = Post.objects.filter(is_show=True, post_type='post', tutorial__name__isnull=False).order_by('created_time')

    # 创建一个 dict, 以教程名称为关键字保存
    post_dict = {}
    for post in post_list:
        if post.tutorial not in post_dict.keys():
            post_dict[post.tutorial] = []
        post_dict[post.tutorial].append(post)
    return render(request, 'blog/tutorials.html', context={'post_dict': post_dict})


# 归档页面
def Archives(request):
    years = Post.objects.filter(is_show=True,post_type='post').dates('created_time', 'year', order='DESC')
    post_list = Post.objects.filter(is_show=True,post_type='post').order_by('-created_time')
    return render(request, 'blog/archives.html', context={'years': years, 'post_list':post_list})


# 关于页面
def About(request):
    post = Post.objects.filter(is_show=True, post_type='about').first()
    if post:
        post.increase_views()  # 调用 increase_views 方法，统计访问量
        comments_dict = comment_reply_content(post_id=post.id)  # 评论回复
        comment_form = CommentForm()  # 引入评论表单
        context = {
            'post': post,
            'comments_dict': comments_dict,
            'comment_form': comment_form,
        }
        return render(request, 'blog/about.html', context=context)
    else:
        return page_not_found(request)


# 我的项目
def Project(request):
    post = Post.objects.filter(is_show=True, post_type='project').first()
    if post:
        post.increase_views()  # 调用 increase_views 方法，统计访问量
        comments_dict = comment_reply_content(post_id=post.id)  # 评论回复
        comment_form = CommentForm()  # 引入评论表单
        context = {
            'post': post,
            'comments_dict': comments_dict,
            'comment_form': comment_form,
        }
        return render(request, 'blog/project.html', context=context)
    else:
        return page_not_found(request)


# 搜索请求
def search(request):
    # 搜索内容
    if request.method == 'GET':
        q = request.GET.get('q')
        post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q), is_show=True, post_type='post')

        data = {'posts': []}
        for post in post_list:
            data['posts'].append({
                "title": post.title,
                "permalink": post.get_absolute_url(),
                "text": post.body
            },)
        return HttpResponse(json.dumps(data,ensure_ascii=False), content_type="application/json,charset=utf-8")
    else:
        pass
