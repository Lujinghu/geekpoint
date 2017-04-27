import time
from django.shortcuts import render, get_object_or_404
from . import forms
from . import models
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import functools
from django.contrib import messages


def check_manager_dec(func):
    '''
    装饰器，用来判断当前用户是否商店的管理人员，从而判断是不是应该拒绝访问
    :param func: 
    :return: 
    '''
    @login_required()
    @functools.wraps(func)#python内置的装饰器，用来给装饰器返回的新函数的__name__属性进行更改，改回跟原来同名就好了
    def wrapper(request, *args, **kwargs):
        shop = get_object_or_404(models.Shop, id=kwargs.get('shop_id'))
        user = request.user
        if shop.check_manager(user):
            return func(request, *args, **kwargs)
        else:
            messages.error(request, '对不起，您不是这家商店的管理员，无权进行该操作！！')
            return HttpResponseRedirect(reverse('geekpoint:index'))
    return wrapper


#定义首页视图，如果用户已经登陆，则显示进入或者注册商户的入口，如果未登录，则显示请登录
def index(request):
    if request.user.is_authenticated():
        user = request.user
        history_order_list = models.Order.objects.query_by_user(user)
        charge_shop_list = models.Shop.objects.query_by_user(user)
        context = {'history_order_list': history_order_list, 'charge_shop_list': charge_shop_list}
        return render(request, 'geekpoint/index.html', context)
    return render(request, 'geekpoint/index.html')


#创建商店
@login_required
def create_shop(request):
    if request.method == 'GET':
        form = forms.ShopForm()
        return render(request, 'geekpoint/create_shop.html', {'form': form})
    form = forms.ShopForm(request.POST)
    if form.is_valid():
        shop = form.save()
        shop.shop_managers.add(request.user)
        shop.save()
        messages.success(request, "你已经成功创建商店: %s！" % shop.name)
        return HttpResponseRedirect(reverse('geekpoint:index'))
    else:
        return render(request, 'geekpoint/create_shop.html', {'form': form})


# 商店管理视图，展示订单信息，以及商店的管理信息
@check_manager_dec
def charge_shop(request, shop_id):
    shop = get_object_or_404(models.Shop, pk=shop_id)
    order_list = models.Order.objects.query_by_shop(shop)
    x_order_list = models.Order.objects.query_by_status('x', shop)
    q_order_list = models.Order.objects.query_by_status('q', shop)
    context = {
        'shop': shop,
        'x_order_list': x_order_list,
        'q_order_list': q_order_list,
    }
    messages.info(request, "欢迎您来到商店管理后台！")
    return render(request, 'geekpoint/charge_shop.html', context)


#更改商店信息视图,变更成功则返回charge_shop视图
@check_manager_dec
def edit_shop(request, shop_id):
    shop = get_object_or_404(models.Shop, pk=shop_id)
    if request.method == 'POST':
        form = forms.ShopForm(instance=shop, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '商店信息更新成功！')
            return HttpResponseRedirect(reverse('geekpoint:charge_shop', kwargs={'shop_id': shop_id}))
    else:
        form = forms.ShopForm(instance=shop)
    return render(request, 'geekpoint/edit_shop.html', {'form': form, 'shop': shop})


#删除商店
@check_manager_dec
def delete_shop(request, shop_id):
    shop = get_object_or_404(models.Shop, pk=shop_id)
    shop.delete()
    messages.success(request, '商店：{}已经成功删除'.format(shop.name))
    return HttpResponseRedirect(reverse('geekpoint:index'))


#管理食物信息视图，查询并且返回现在的食物清单
@check_manager_dec
def charge_food(request, shop_id):
    shop = get_object_or_404(models.Shop, pk=shop_id)
    food_list = models.Food.objects.query_by_shop(shop)
    food_category_list = shop.foodcategory_set.all()
    context = {
        'shop': shop,
        'food_list': food_list,
        'food_category_list': food_category_list,
    }
    return render(request, 'geekpoint/charge_food.html', context)


#新建食品视图，用来新增一个新食品
@check_manager_dec
def create_food(request, shop_id):
    shop = get_object_or_404(models.Shop, pk=shop_id)
    food_category_form = forms.FoodCategoryForm()
    food_category_list = shop.foodcategory_set.all()
    context = {
        'shop_id': shop_id,
        'food_category_list': food_category_list,
        'food_category_form': food_category_form,
    }
    if request.method == 'POST':
        form = forms.FoodForm(request.POST)
        if form.is_valid():
            food = form.save(commit=False)
            try:
                food_category = models.FoodCategory.objects.get(id=request.POST.get('food_category_id'))
                food.category = food_category
            except BaseException:
                pass
            food.shop = shop
            form.save()
            messages.success(request, '食品：{}已经创建！'.format(food.name))
            return HttpResponseRedirect(reverse('geekpoint:charge_food', args=[shop_id]))
        else:
            context['form'] = form
    else:
        form = forms.FoodForm()
        context['form'] = form
    return render(request, 'geekpoint/create_food.html', context)


#@login_required()
@check_manager_dec
def create_foodcategory(request, shop_id):
    shop = get_object_or_404(models.Shop, id=shop_id)
    if request.method == 'POST':
        food_category_form = forms.FoodCategoryForm(request.POST)
        if food_category_form.is_valid():
            food_category = food_category_form.save(commit=False)
            food_category.shop = shop
            food_category.save()
            messages.success(request, '你已成功创建食品分类：% s' % food_category.name)
    return HttpResponseRedirect(reverse('geekpoint:create_food', args=[shop_id]))


@check_manager_dec
def delete_foodcategory(request, shop_id, food_category_id):
    food_category = get_object_or_404(models.FoodCategory, id=food_category_id)
    food_category.delete()
    messages.success(request, '食物分类已经删除！')
    return HttpResponseRedirect(reverse('geekpoint:create_food', args=[shop_id]))


@check_manager_dec
def edit_food(request, shop_id, food_id):
    food = get_object_or_404(models.Food, pk=food_id)
    if request.method == 'POST':
        form = forms.FoodForm(request.POST, instance=food)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('geekpoint:charge_food', args=[shop_id]))
    form = forms.FoodForm(instance=food)
    return render(request, 'geekpoint/edit_food.html', {'form': form, 'food_id': food_id, 'shop_id': shop_id})


@check_manager_dec
def delete_food(request, shop_id, food_id):
    food = get_object_or_404(models.Food, pk=food_id)
    food.delete()
    messages.success(request, '食物已经删除！')
    return HttpResponseRedirect(reverse('geekpoint:charge_food', kwargs={'shop_id': shop_id}))


#浏览商店视图，可以查看所有的商店信息，并且提供到店消费的链接
@login_required()
def check_all_shop(request):
    shop_list = models.Shop.objects.all()
    return render(request, 'geekpoint/check_all_shop.html', {'shop_list': shop_list})


#商户后台标记订单状态
@check_manager_dec
def shop_mark_order(request, shop_id, order_id):
    order = get_object_or_404(models.Order, pk=order_id)
    order.status = request.POST.get('status')
    order.save()
    messages.success(request, '订单状态已更改！')
    return HttpResponseRedirect(reverse('geekpoint:charge_shop', args=[shop_id]))


@check_manager_dec
def shop_delete_order(request, shop_id, order_id):
    order = get_object_or_404(models.Order, pk=order_id)
    order.is_delete_by_shop = True
    order.save()
    messages.success(request, '订单已经删除')
    return HttpResponseRedirect(reverse('geekpoint:charge_shop', args=[shop_id]))


#订食物，如果是GET请求，就返回商店的食物列表的模板供选择，如果是POST，就生成一张订单
@login_required()
def order_food(request, shop_id, food_category_id=None):
    shop = get_object_or_404(models.Shop, pk=shop_id)
    if request.method == 'GET':
        if food_category_id:
            food_list = models.Food.objects.query_by_category(shop, food_category_id)
        else:
            food_list = models.Food.objects.query_by_shop(shop)
        food_category_list = shop.foodcategory_set.all()
        context = {
            'food_list': food_list,
            'shop': shop,
            'food_category_list': food_category_list,
        }
        return render(request, 'geekpoint/order_food.html', context)
    food_id_list = request.POST.getlist('food_id_list')
    food_list = []
    food_number_list = []
    food_price_list = []
    total = 0
    for food_id in food_id_list:
        food = get_object_or_404(models.Food, id=food_id)
        food_list.append(food)
        food_number = int(request.POST.get(str(food_id)+'_number'))
        food_number_list.append(food_number)
        food_price_list.append(food.price)
        total += food.price * food_number
    table_no = str(request.POST.get('table_no'))
    while True:
        try:
            num = models.Order.objects.query_by_today(shop).count() + 1
            order = models.Order.objects.create(
                order_no=num,
                shop=shop,
                consumer=request.user,
                table_no=table_no,
                total=total
            )
            break
        except BaseException:
            pass
    #下面也是一种尝试，不想使用简单的订单数量来作为单号，尝试加入一些复杂一点的元素,也就是加上时间戳作为单号
    order.order_no = str(int(time.mktime(order.created_time.timetuple()))) + str(order.order_no)
    order.save()
    #在订单和食物的多对多关联列表中保存数据
    i = 0
    for food in food_list:
        orderfood = models.OrderFood(
                     food=food,
                     order=order,
                     nums=food_number_list[i],
                    )
        orderfood.save()
        i += 1
    messages.success(request, '恭喜你，你已经成功下单！')
    return HttpResponseRedirect(reverse('geekpoint:get_order', args=[order.id]))


#获取订单视图
@login_required()
def get_order(request, order_id):
    order = get_object_or_404(models.Order, pk=order_id)
    return render(request, 'geekpoint/order_detail.html', {'order': order})


#消费者删除订单视图
@login_required()
def consumer_delete_order(request, order_id):
    order = models.Order.objects.get(id=order_id)
    if order.check_consumer(request.user):
        order.is_delete_by_consumer = True
        order.save()
        messages.success(request, '删除订单成功！')
        return HttpResponseRedirect(reverse('geekpoint:index'))

def register(request):
    if request.method == 'POST':
        user_form = forms.UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.save()
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = forms.UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})








