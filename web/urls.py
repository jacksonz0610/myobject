"""myobject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from web.views import index, cart, orders

# 大堂点餐端子路由配置
urlpatterns = [
    path('', index.index, name='web_index'),

    # 前台登录退出的路由
    path('login', index.login, name='web_login'),
    path('dologin', index.dologin, name='web_dologin'),
    path('logout', index.logout, name='web_logout'),
    path('verify', index.verify, name='web_verify'),

    # 为url路由添加请求前缀web/，凡是带此前缀的url地址必须登录后才可访问
    path('web/', include([
        path('', index.webindex, name='web_index'),
        #购物车信息管理路由
        path('cart/add/<str:pid>', cart.add, name='web_cart_add'),
        path('cart/delete/<str:pid>', cart.delete, name='web_cart_delete'),
        path('cart/clear', cart.clear, name='web_cart_clear'),
        path('cart/change', cart.change, name='web_cart_change'),

        # 订单处理路由
        path('orders/<int:pIndex>', orders.index, name='web_orders_index'),
        path('orders/insert', orders.insert, name='web_orders_insert'),
        path('orders/detail', orders.detail, name='web_orders_detail'),
        path('orders/status', orders.status, name='web_orders_status'),
    ]))
]
