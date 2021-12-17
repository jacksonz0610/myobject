# 自定义中间件类，登录判断
from django.shortcuts import redirect
from django.urls import reverse

import re

class ShopMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print('启动shopmiddleware中间件!')
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        path = request.path
        print('当前访问的路由是', path)

        # 判断管理后台是否登录
        # 定义后台不登录也可以直接访问的url列表
        urllist = ['/myadmin/login', '/myadmin/logout', '/myadmin/dologin', '/myadmin/verify']
        # 判断当前请求url是否以/myadmin开头，并且不再urllist中
        if re.match(r'^/myadmin', path) and (path not in urllist):
            # 判断是否登录
            if 'adminuser' not in request.session:
                # 重定向到登录页
                return redirect(reverse('myadmin_login'))

        # 判断大堂点餐请求的判断，判断是否登录（session中是否有webuser）
        if re.match(r'^/web', path):
            # 判断是否登录（在于session中是否有webuser）
            if 'webuser' not in request.session:
                # 重定向到登录页
                return redirect(reverse('web_login'))

        # 判断移动端的登录
        # 定义后台不登录也可以直接访问的url列表
        urllist = ['/mobile/register', '/mobile/logout', '/mobile/doregister']
        # 判断当前请求url是否以/mobile开头，并且不再urllist中
        if re.match(r'^/mobile', path) and (path not in urllist):
            # 判断是否登录（在于session中是否有mobileuser）
            if 'mobileuser' not in request.session:
                # 重定向到登录页
                return redirect(reverse('mobile_register'))

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response