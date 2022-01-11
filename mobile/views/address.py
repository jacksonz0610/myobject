from django.shortcuts import render, redirect
from django.urls import reverse

from myadmin.models import Address, Member

def index(request):
    '''浏览会员收货地址信息'''
    amod = Address.objects.filter(member_id=request.session['mobileuser']['id'])
    alist = amod.filter(status__lt=9)
    context = {'addresslist': alist}
    return render(request, 'mobile/member_address.html', context)

def add(request):
    '''加载地址添加模板'''
    return render(request, 'mobile/member_addAddress.html')

def insert(request):
    '''执行添加地址'''
    try:
        ob = Address()
        ob.member_id = request.session['mobileuser']['id']
        ob.name = request.POST['name']
        ob.mobile = request.POST['mobile']
        ob.province = request.POST['province']
        ob.city = request.POST['city']
        ob.district = request.POST['district']
        if request.POST['detail']:
            ob.detail = request.POST['detail']
        if request.POST['postalCode']:
            ob.postalCode = request.POST['postalCode']
        ob.status = 1
        ob.save()
        context = {'info': '添加成功！'}
    except Exception as err:
        print(err)
        print('地址添加失败')
        context = {'info': '添加失败！'}
    return redirect(reverse('mobile_address_index'))

def delete(request, aid=0):
    '''删除地址'''
    try:
        ob = Address.objects.get(id=aid)
        ob.status = 9
        ob.save()
    except Exception as err:
        print(err)
        print('地址删除失败')
    return redirect(reverse('mobile_address_index'))

def edit(request, aid=0):
    '''加载地址编辑模板'''
    ob = Address.objects.get(id=aid)
    context = {'address': ob, 'address_id': aid}
    return render(request, 'mobile/member_editAddress.html', context)

def update(request, aid=0):
    '''执行地址编辑'''
    try:
        ob = Address.objects.get(id=aid)
        ob.name = request.POST['name']
        ob.mobile = request.POST['mobile']
        ob.province = request.POST['province']
        ob.city = request.POST['city']
        ob.district = request.POST['district']
        ob.detail = request.POST['detail']
        ob.postalCode = request.POST['postalCode']
        ob.save()
    except Exception as err:
        print(err)
        print('修改失败')
    return redirect(reverse('mobile_address_index'))

