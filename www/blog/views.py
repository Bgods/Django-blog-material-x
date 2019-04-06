# _*_ coding:utf-8 _*_

from django.shortcuts import render, get_object_or_404
from django.views import View
from blog.models import Post,Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.db.models.aggregates import Count
import json,re
from django.http import HttpResponse
from www.views import page_not_found


# 博客文章列表页面
class Index():
    def __init__(self):
        # 定义 per_page 的值，每个页面的文章数
        self.per_page = 10

    def index(self,request):
        # 博客首页：获取Post表中所有文章列表
        post_list = Post.objects.filter(is_show=True, post_type='post')
        page = request.GET.get('page')
        return self.get_data(post_list=post_list,page=page,request=request)


    def category(self,request, category):
        # 分类：按照标签(category)查询Post表中的文章列表
        post_list = Post.objects.filter(category__name=category,is_show=True,post_type='post')
        page = request.GET.get('page')
        return self.get_data(post_list=post_list, page=page, request=request)

    def tags(self,request, tag):
        # 标签：按照标签(tag)查询Post表中的文章列表
        post_list = Post.objects.filter(tags__name=tag,is_show=True,post_type='post')
        page = request.GET.get('page')
        return self.get_data(post_list=post_list, page=page, request=request)


    def get_data(self,post_list,page,request):
        context = self.Pagination(post_list=post_list, page=page)
        return render(request, 'blog/index.html', context=context)

    # 高级分页扩展函数
    def Pagination(self, post_list, page):
        # 使用 Paginator 函数将post_list以每页per_page篇文章进行分页
        paginator = Paginator(post_list, self.per_page)
        try:
            post_list = paginator.page(page)

        except PageNotAnInteger:
            page = 1
            post_list = paginator.page(1)
        except EmptyPage:
            post_list = paginator.page(paginator.num_pages)

        # 定义left_pages、right_pages两个列表，分别储存当前页面的前后页数，比如：总共有7页，当前页面是3，则分别储存[1,2]、[4,5,6,7]
        left_pages = []
        right_pages = []
        for p in paginator.page_range:
            if int(p) < int(page):
                left_pages += [p]
            if int(p) > int(page):
                right_pages += [p]

        return {'post_list': post_list,
                'left_pages': left_pages[-2:],
                'right_pages': right_pages[:2]
                }




# 博客详情页
class Detail(View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        a = get_toc(post.body)
        post.body = a['body']
        post.toc = a['toc']

        # 调用 increase_views 方法，统计访问量
        post.increase_views()
        return render(request, 'blog/detail.html', context = {'post': post})
    def post(self, request):
        pass


# 获取目录，提取body中的h标签
def get_toc(body):
    pattern = re.compile(r'<[hH][1-6]>.*?</[Hh][1-6]>')
    h = pattern.findall(body)
    toc =[]
    for i in range(len(h)):
        a = re.sub('>', ' id="toc-0{}">'.format(i+1), h[i], 1)
        body = re.sub(h[i], a, body)
        a = re.sub('id="', 'href="#', a, 1)
        a = re.sub('<[Hh][1-6]', '<li class="toc-item toc-level-2"><a class="toc-link" ', a)
        a = re.sub('</[Hh][1-6]>', '</a></li>', a)
        toc.append(a)
    return {'body': body, 'toc': ''.join(toc)}


# 归档页面
def Archives(request):
    years = Post.objects.filter(is_show=True,post_type='post').dates('created_time', 'year', order='DESC')
    post_list = Post.objects.filter(is_show=True,post_type='post').order_by('-created_time')
    return render(request, 'blog/archives.html', context={'years':years, 'post_list':post_list})


# 标签页面
def Tags(request):
    # 使用 Count 方法统计文章数，并保存到 num_posts 属性中
    tags = Tag.objects.filter(post__is_show=True,post__post_type='post').annotate(num_posts=Count('post')).filter(num_posts__gt=0).order_by('-num_posts')
    return render(request, 'blog/tags.html', context={'tags': tags})


# 关于页面
def About(request):
    post = Post.objects.filter(post_type='about').first()
    if post:
        post.increase_views() # 调用 increase_views 方法，统计访问量
        return render(request, 'blog/about.html', context={'post': post})
    else:
        return page_not_found(request)

# 我的项目
def Project(request):
    post = Post.objects.filter(post_type='project').first()
    if post:
        post.increase_views() # 调用 increase_views 方法，统计访问量
        return render(request, 'blog/project.html', context={'post': post})
    else:
        return page_not_found(request)

# 搜索请求
def search(request, ):
    # 搜索内容
    if request.method == 'GET':
        q = request.GET.get('q')
        post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q), is_show=True, post_type='post')

        data = {'posts':[]}
        for post in post_list:
            data['posts'].append({
                "title":post.title,
                "permalink":post.get_absolute_url(),
                "text":post.body
            },)
        return HttpResponse(json.dumps(data,ensure_ascii=False),content_type="application/json,charset=utf-8")
    else:
        pass
