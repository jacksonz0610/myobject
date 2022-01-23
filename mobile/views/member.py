import os, time
from datetime import datetime

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

# 课后作业

def edit(request):
    '''加载会员资料的编辑模板'''
    return render(request, 'mobile/member_data.html')

def update(request):
    '''会员资料的编辑'''
    try:
        # 获取原图片
        oldavatar = request.POST['oldavatar']
        # 图片的上传操作
        myfile = request.FILES.get("avatar")
        if not myfile:
            avatar = oldavatar
            print('no file')
        else:
            avatar = str(time.time()) + '.' + myfile.name.split('.').pop()
            destination = open("./static/uploads/member/" + avatar, "wb+")
            for chunk in myfile.chunks():
                destination.write(chunk)
            destination.close()
            print('执行完毕')

        ob = Member.objects.get(id=request.session['mobileuser']['id'])
        ob.nickname = request.POST['nickname']
        if request.POST['mobile'] != '':
            ob.mobile = request.POST['mobile']
        ob.avatar = avatar
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': '修改成功！'}
        # request.session['mobileuser'] = ob.toDict()

        # 判断并删除老图片
        if myfile:
            os.remove("./static/uploads/member/" + oldavatar)

    except Exception as err:
        print(err)
        context = {'info': '修改失败！'}

        # 判断并删除新图片
        if myfile:
            os.remove("./static/uploads/member/" + avatar)
    return render(request, 'mobile/member.html', context)

def editPwd(request):
    return render(request, 'mobile/member_pwd.html')

def updatePwd(request):
    pass