from datetime import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
from django.urls import reverse

from myadmin.models import Member, Shop, Category, Product, Payment, Orders, OrderDetail


def index(request):
    '''移动端首页'''
    # 获取并判断店铺信息是否存在
    shopinfo = request.session.get('shopinfo', None)
    if shopinfo == None:
        return redirect(reverse('mobile_shop'))
    clist = Category.objects.filter(shop_id=shopinfo['id'], status=1)
    productlist = {}
    for vo in clist:
        plist = Product.objects.filter(category_id=vo.id, status=1)
        productlist[vo.id] = plist
    context = {'categorylist': clist, 'productlist': productlist.items(), 'cid': clist[0]}
    return render(request, 'mobile/index.html', context)

def register(request):
    '''移动端会员注册/登录表单'''
    return render(request, 'mobile/register.html')

def doRegister(request):
    '''移动端执行会员登录注册'''
    # 模拟短信验证
    verifycode = '1234' # request.session['verifycode']
    if verifycode != request.POST['code']:
        context = {'info': '验证码错误！'}
        return render(request, 'mobile/register.html', context)
    try:
        # 根据手机号码获取当前会员信息
        member = Member.objects.get(mobile=request.POST['mobile'])
    except Exception as err:
        context = {'info': '此账户信息不存在！'}
        print(err)
        # 执行当前会员注册操作
        ob = Member()
        ob.mobile = request.POST['mobile']
        ob.nickname = '顾客'
        ob.status = 1
        ob.avatar = 'moren.png'
        ob.create_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.save()
        member = ob
    # 检验当前会员状态是否正常
    if member.status == 1:
        # 将当前会员的信息转成字典并放入session中
        request.session['mobileuser'] = member.toDict()
        return redirect(reverse('mobile_index'))
    else:
        context = {'info': '此账户信息禁用！'}
        return render(request, 'mobile/register.html', context)

def shop(request):
    '''移动端选择店铺页面'''
    context = {'shoplist': Shop.objects.filter(status=1)}
    return render(request, 'mobile/shop.html', context)

def seleteShop(request):
    '''移动端执行移动端店铺选择操作'''
    # 获取选择的店铺信息并放值到session中
    sid = request.GET['sid']
    ob = Shop.objects.get(id=sid)
    request.session['shopinfo'] = ob.toDict()
    request.session['cartlist'] = {} # 清空购物车
    # 跳转到首页
    return redirect(reverse('mobile_index'))

def addOrders(request):
    '''移动端下单表单页'''
    cartlist = request.session.get('cartlist', {})
    total_money = 0
    # 遍历购物车中的菜品并累加总金额
    for vo in cartlist.values():
        total_money += vo['num'] * vo['price']
    request.session['total_money'] = total_money
    return render(request, 'mobile/addOrders.html')

def doAddOrders(request):
    '''执行订单添加'''
    try:
        # 执行订单数据的添加
        od = Orders()
        od.shop_id = request.session['shopinfo']['id']
        od.member_id = request.session['mobileuser']['id']
        od.user_id = 0
        od.money = request.session['total_money']
        od.status = 1
        od.payment_status = 2 # 1未支付2已支付3已退款
        od.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        od.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        od.save()

        # 支付信息添加
        op = Payment()
        op.order_id = od.id
        op.member_id = request.session['mobileuser']['id']
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
    except Exception as err:
        print(err)
    return render(request, 'mobile/orderinfo.html', {'order': od})
