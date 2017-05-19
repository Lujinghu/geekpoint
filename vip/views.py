from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Vip
from shop.decorators import check_manager_dec
from shop.models import Shop
from django.contrib import messages
from django.core.urlresolvers import reverse

@check_manager_dec
def vip_add(request, shop_id, user_id):
    user = get_object_or_404(User, id=user_id)
    shop = get_object_or_404(Shop, id=shop_id)
    vip = Vip.objects.create(shop=shop, user=user)
    return redirect(reverse('shop:vip_charge', shop_id))


@check_manager_dec
def vip_deactive(request, shop_id, user_id):
    user = get_object_or_404(User, id=user_id)
    shop = get_object_or_404(Shop, id=shop_id)
    vip = Vip.objects.get(shop=shop, user=user)
    vip.deactive()
    messages.success(request, 'vip用户{}已被禁用'.format(user))
    return redirect(reverse('shop:vip_charge', shop_id))


@check_manager_dec
def vip_active(request, shop_id, user_id):
    user = get_object_or_404(User, id=user_id)
    shop = get_object_or_404(Shop, id=shop_id)
    vip = Vip.objects.get(shop=shop, user=user)
    vip.active()
    messages.success(request, 'vip用户{}已被激活'.format(user))
    return redirect(reverse('shop:vip_charge', shop_id))
