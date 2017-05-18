from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .decorators import check_manager_dec
from .forms import ShopForm, AddShopManagerForm
from django.contrib import messages
from django.core.urlresolvers import reverse
from .models import Shop
from order.models import Order
from django.contrib.auth.models import User

#创建商店
@login_required
def create_shop(request):
    if request.method == 'POST':
        form = ShopForm(request.POST)
        if form.is_valid():
            shop = form.save()
            shop.add_manager(request.user)
            shop.save()
            messages.success(request, "你已经成功创建商店: %s！" % shop.name)
            return redirect(reverse('geekpoint:index'))
    else:
        form = ShopForm()
    return render(request, 'shop/create_shop.html', {'form': form})


# 商店管理视图，展示订单信息，以及商店的管理信息
@check_manager_dec
def charge_shop(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id)
    context = {'shop': shop}
    return render(request, 'shop/charge_shop.html', context)


@check_manager_dec
def charge_order(request, shop_id):
    shop = get_object_or_404(Shop, pk=shop_id)
    x_order_list = Order.objects.query_by_status('x', shop)
    q_order_list = Order.objects.query_by_status('q', shop)
    f_order_list = Order.objects.query_by_status('f', shop)
    context = {
        'shop': shop,
        'x_order_list': x_order_list,
        'q_order_list': q_order_list,
        'f_order_list': f_order_list,
    }
    messages.info(request, "欢迎您来到订单管理管理后台！")
    return render(request, 'shop/charge_order.html', context)


#更改商店信息视图,变更成功则返回charge_shop视图
@check_manager_dec
def edit_shop(request, shop_id):
    shop = get_object_or_404(Shop, pk=shop_id)
    if request.method == 'POST':
        form = ShopForm(instance=shop, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '商店信息更新成功！')
            return redirect(reverse('geekpoint:charge_shop', kwargs={'shop_id': shop_id}))
    else:
        form = ShopForm(instance=shop)
    return render(request, 'shop/edit_shop.html', {'form': form, 'shop': shop})


#删除商店
@check_manager_dec
def delete_shop(request, shop_id):
    shop = get_object_or_404(Shop, pk=shop_id)
    shop.delete()
    messages.success(request, '商店：{}已经成功删除'.format(shop.name))
    return redirect(reverse('geekpoint:index'))


@check_manager_dec
def add_shop_manager(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id)
    if request.method == 'POST':
        form = AddShopManagerForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            email = cd['email']
            try:
                new_manager = User.objects.get(email=email)
            except BaseException:
                messages.info(request, '该用户不存在！！')
            if shop.add_manager(new_manager):
                messages.success(request, '管理员{}已经添加成功！'.format(email))
            else:
                messages.success(request, '管理员{}已经存在'.format(email))
    else:
        form = AddShopManagerForm()
    context = {'shop': shop, 'form': form}
    return render(request, 'shop:add_shop_manager.html', context)


@check_manager_dec
def delete_shop_manager(request, shop_id, user_id):
    shop = get_object_or_404(Shop, id=shop_id)
    user = get_object_or_404(User, id=user_id)
    if shop.remove_manager(user):
        messages.success(request, '管理员{}已经添加成功！'.format(user))
    else:
        messages.success(request, '管理员{}不存在'.format(user))
    return render(request, 'shop:charge_shop_manager.html', {'shop': shop})