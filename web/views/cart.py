# 购物车信息管理视图
from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
from django.urls import reverse


def add(request, pid):
    '''添加购物车操作'''
    # 从session中获取当前店铺中所有的菜品信息，并从中选取要加入购物车的菜品信息
    product = request.session['productlist'][pid]
    product['num'] = 1 # 初始化当前菜品的购买量
    # 尝试从session中获取购物车信息
    cartlist = request.session.get('cartlist', {})
    # 判断当前菜品中是否存在要放进购物车的菜品
    if pid in cartlist:
        cartlist[pid]['num'] +=1
    else:
        cartlist[pid] = product
    # 将cartlist购物车信息放入session中
    request.session['cartlist'] = cartlist
    print(cartlist)
    return redirect(reverse('web_index'))

def delete(request, pid):
    '''删除购物车商品操作'''
    cartlist = request.session.get('cartlist', {})
    del cartlist[pid]
    request.session['cartlist'] = cartlist
    print(cartlist)
    return redirect(reverse('web_index'))

def clear(request):
    '''清空购物车操作'''
    request.session['cartlist'] = {}
    return redirect(reverse('web_index'))

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
    return redirect(reverse('web_index'))
