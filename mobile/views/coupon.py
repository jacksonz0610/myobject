import os, time
from datetime import datetime

from django.shortcuts import render

# Create your views here.
from myadmin.models import Coupon

def index(request):
    '''展示会员所有的优惠券'''
    cmod = Coupon.objects.filter(member_id=request.session['mobileuser']['id'])
    clist = cmod.filter(status=1)
    context = {'couponlist': clist}
    return render(request, 'mobile/member_coupon.html', context)

def add(request):
    '''添加优惠券'''
    pass

