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
from django.urls import path
from mobile.views import index, member, cart, address

# 会员移动端子路由配置
urlpatterns = [
    path('', index.index, name='mobile_index'),
    # 会员注册或登录
    path('register', index.register, name='mobile_register'),
    path('doregister', index.doRegister, name='mobile_doregister'),
    path('shop', index.shop, name='mobile_shop'),
    path('shop/select', index.seleteShop, name='mobile_selectshop'),
    # 订单处理
    path('orders/add', index.addOrders, name='mobile_addorders'),
    path('orders/doadd', index.doAddOrders, name='mobile_doaddorders'),

    # 会员中心
    path('member', member.index, name='mobile_member_index'),
    path('member/orders', member.orders, name='mobile_member_orders'),
    path('member/detail', member.detail, name='mobile_member_detail'),
    path('member/logout', member.logout, name='mobile_member_logout'),
    path('member/data/edit', member.edit, name='mobile_member_data_edit'),
    path('member/data/update', member.update, name='mobile_member_data_update'),

    # 会员收货地址管理路由
    path('member/address/index', address.index, name='mobile_address_index'),
    path('member/address/add', address.add, name='mobile_address_add'),
    path('member/address/insert', address.insert, name='mobile_address_insert'),
    path('member/address/delete/<int:aid>', address.delete, name='mobile_address_delete'),
    path('member/address/edit/<int:aid>', address.edit, name='mobile_address_edit'),
    path('member/address/update/<int:aid>', address.update, name='mobile_address_update'),

    #购物车信息管理路由
    path('cart/add', cart.add, name='mobile_cart_add'),
    path('cart/delete', cart.delete, name='mobile_cart_delete'),
    path('cart/clear', cart.clear, name='mobile_cart_clear'),
    path('cart/change', cart.change, name='mobile_cart_change'),
]