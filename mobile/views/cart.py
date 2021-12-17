# 购物车信息管理视图
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

# Create your views here.
from django.urls import reverse
from myadmin.models import Product


def add(request):
    '''添加购物车操作'''
    # 尝试从session中获取购物车信息
    cartlist = request.session.get('cartlist', {})
    # 获取要购买的菜品信息，并从中选取要加入购物车的菜品信息
    pid = request.GET.get('pid', None)
    if pid is not None:
        product = Product.objects.get(id=pid).toDict()
        product['num'] = 1
        # 判断当前菜品中是否存在要放进购物车的菜品
        if pid in cartlist:
            cartlist[pid]['num'] +=1
        else:
            cartlist[pid] = product
        # 将cartlist购物车信息放入session中
        request.session['cartlist'] = cartlist
    # print(cartlist)
    # 响应json格式的购物车数据
    return JsonResponse({'cartlist': cartlist})

def delete(request):
    '''删除购物车商品操作'''
    cartlist = request.session.get('cartlist', {})
    del cartlist[pid]
    request.session['cartlist'] = cartlist
    print(cartlist)
    # 响应json格式的购物车数据
    return JsonResponse({'cartlist': cartlist})

def clear(request):
    '''清空购物车操作'''
    request.session['cartlist'] = {}
    # 响应json格式的购物车数据
    return JsonResponse({'cartlist': {}})

def change(request):
    '''更改购物车操作'''
    # 获取要求改的菜品id
    cartlist = request.session.get('cartlist', {})
    pid = request.GET.get('pid', 0)
    # 要修改的数量
    m = int(request.GET.get('num', 1))
    if m < 1:
        m = 1
    cartlist[pid]['num'] = m
    request.session['cartlist'] = cartlist
    # 响应json格式的购物车数据
    return JsonResponse({'cartlist': cartlist})
