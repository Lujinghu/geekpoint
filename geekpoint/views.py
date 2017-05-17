import time
from django.shortcuts import render, get_object_or_404
from . import forms
from . import models
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from shop.decorators import check_manager_dec


#定义首页视图，如果用户已经登陆，则显示进入或者注册商户的入口，如果未登录，则显示请登录
def index(request):
    if request.user.is_authenticated():
        user = request.user
        history_order_list = models.Order.objects.query_by_user(user)
        charge_shop_list = models.Shop.objects.query_by_user(user)
        context = {'history_order_list': history_order_list, 'charge_shop_list': charge_shop_list}
        return render(request, 'geekpoint/index.html', context)
    return render(request, 'geekpoint/index.html')






#浏览商店视图，可以查看所有的商店信息，并且提供到店消费的链接
@login_required()
def check_all_shop(request):
    shop_list = models.Shop.objects.all()
    return render(request, 'geekpoint/check_all_shop.html', {'shop_list': shop_list})











