from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from myadmin.models import Payment, Orders, OrderDetail, Member, Shop


def index(request):
    '''个人中心首页'''
    return render(request, 'mobile/member.html')

def orders(request):
    '''个人中心浏览订单'''
    mod = Orders.objects
    mid = request.session['mobileuser']['id'] # 获取当前会员id号
    olist = mod.filter(member_id=mid)

    # 获取、判断并封装状态status搜索条件
    status = request.GET.get('status', '')
    if status != '':
        olist = olist.filter(status=status)

    list2 = olist.order_by('-id')

    # 遍历当前订单，封装订单详情信息
    orders_status = ['无', '排队中', '已撤销', '已完成']
    for vo in list2:
        plist = OrderDetail.objects.filter(order_id=vo.id)[:4] # 获取头4条
        vo.plist = plist
        vo.status_info = orders_status[vo.status]

    context = {'orderslist': list2}
    return render(request, 'mobile/member_orders.html', context)

def detail(request):
    '''个人中心中的订单详情'''
    pid = request.GET.get('pid', 0)
    order = Orders.objects.get(id=pid)
    plist = OrderDetail.objects.filter(order_id=order.id)
    order.plist = plist
    shop = Shop.objects.only('name').get(id=order.shop_id)
    order.shopname = shop.name
    orders_status = ['无', '排队中', '已撤销', '已完成']
    order.status_info = orders_status[order.status]
    return render(request, 'mobile/member_detail.html', {'order': order})

def logout(request):
    '''会员退出'''
    return render(request, 'mobile/register.html')

