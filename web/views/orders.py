# 订单信息管理视图
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime

# Create your views here.
from django.urls import reverse
from myadmin.models import Payment, Orders, OrderDetail, User, Member


def index(request, pIndex=1):
    '''浏览订单信息'''
    umod = Orders.objects
    sid = request.session['shopinfo']['id']# 获取当前店铺id号
    ulist = umod.filter(shop_id=sid)
    mywhere = []

    # 获取、判断并封装状态status搜索条件
    status = request.GET.get('status', '')
    if status != '':
        ulist = ulist.filter(status=status)
        mywhere.append("status=" + status)

    ulist = ulist.order_by('-id')
    # 执行分页处理
    pIndex = int(pIndex)
    page = Paginator(ulist, 5)
    maxpages = page.num_pages
    # 判断当前页是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)  # 获取当前页数据
    plist = page.page_range  # 获取页码列表信息

    for vo in list2:
        if vo.member_id == 0:
            vo.membername = '大堂顾客'
        else:
            member = Member.objects.only('mobile').get(id=vo.member_id)
            vo.membername = member.mobile

    context = {'orderslist': list2, 'plist': plist, 'pIndex': pIndex, 'maxpages': maxpages, 'mywhere': mywhere}
    return render(request, "web/list.html", context)

def insert(request):
    '''执行订单添加'''
    try:
        # 执行订单数据的添加
        od = Orders()
        od.shop_id = request.session['shopinfo']['id']
        od.member_id = 0
        od.user_id = request.session['webuser']['id']
        od.money = request.session['total_money']
        od.status = 1
        od.payment_status = 2 # 1未支付2已支付3已退款
        od.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        od.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        od.save()

        # 支付信息添加
        op = Payment()
        op.order_id = od.id
        op.member_id = 0
        op.type = 2
        op.bank = request.GET.get('bank', 3)
        op.money = request.session['total_money']
        op.status = 2# 1未支付2已支付3已退款
        op.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        op.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        op.save()

        # 执行订单详情的添加
        cartlist = request.session.get('cartlist', {})# 获取购物车中的菜品信息
        # 遍历购物车中的菜品并添加到购物详情列表
        for item in cartlist.values():
            ov = OrderDetail()
            ov.order_id = od.id
            ov.product_id = item['id']
            ov.product_name = item['name']
            ov.price = item['price']
            ov.quantity = item['num']
            ov.status = 1# 1正常9删除
            ov.save()

        del request.session['cartlist']
        del request.session['total_money']
        return HttpResponse('Y')
    except Exception as err:
        print(err)
        return HttpResponse('N')

def detail(request):
    '''加载订单详情'''
    oid = request.GET.get('oid', 0)
    dlist = OrderDetail.objects.filter(order_id=oid)
    context = {'detaillist': dlist}
    return render(request, 'web/detail.html', context)

def status(request):
    '''修改订单状态'''
    try:
        oid=request.GET.get('oid', 0)
        ob = Orders.objects.get(id=oid)
        ob.status = request.GET['status']
        ob.save()
        return HttpResponse('Y')
    except Exception as err:
        print(err)
        return HttpResponse('N')