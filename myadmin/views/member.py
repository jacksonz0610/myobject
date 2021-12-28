from django.shortcuts import render
from myadmin.models import Member
from django.core.paginator import Paginator
from datetime import datetime

def index(request, pIndex=1):
    '''浏览信息'''
    umod = Member.objects
    ulist = umod.filter(status__lt=9)
    # 判断并处理状态搜索条件
    mywhere = []
    kw = request.GET.get('keyword', None)
    if kw:
        ulist = ulist.filter(nickname__contains=kw)
        mywhere.append('keyword=' + kw)

    status = request.GET.get('status', '')
    if status != '':
        ulist = ulist.filter(status=status)
        mywhere.append('status'+status)
    ulist = ulist.order_by('id')
    # 执行分页处理
    pIndex = int(pIndex)
    page = Paginator(ulist, 5)
    maxpages = page.num_pages
    # 判断当前页是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)# 获取当前页数据
    plist = page.page_range# 获取页码列表信息
    context = {'member': list2, 'plist': plist, 'pIndex': pIndex, 'maxpages': maxpages, 'mywhere': mywhere}
    return render(request, "myadmin/member/index.html", context)

# 代码没有修改不可用，管理员端会员信息删除
def delete(request, uid=0):
    '''执行信息删除'''
    try:
        ob = Member.objects.get(id=uid)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': '删除成功！'}
    except Exception as err:
        print(err)
        context = {'info': '删除失败！'}
    return render(request, 'myadmin/info.html', context)
