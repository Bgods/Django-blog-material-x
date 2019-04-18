# _*_ coding:utf-8 _*_

from django.shortcuts import render
from django.views import View





# 主页
class Home(View):
    def get(self, request):
        return render(request, 'home.html')

    def post(self,request):
        pass


# 404页面
def page_not_found(request):
    return render(request, '404.html')

# 500页面
def server_error(request):
    return render(request, '500.html')

