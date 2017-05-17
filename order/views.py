from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from shop.decorators import check_manager_dec
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from shop.models import Shop
from .models import Order, OrderFood
from food.models import Food
import time

# Create your views here.
#商户后台标记订单状态
@check_manager_dec
def shop_mark_order(request, shop_id, order_id):
    order = get_object_or_404(Order, pk=order_id)
    #order.status = request.POST.get('status')
    #order.save()
    order.change_status(request.POST.get('status'))
    messages.success(request, '订单状态已更改！')
    return redirect(reverse('geekpoint:charge_shop', args=[shop_id]))


@check_manager_dec
def shop_delete_order(request, shop_id, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.delete_by_shop()
    messages.success(request, '订单已经删除')
    return redirect(reverse('geekpoint:charge_shop', args=[shop_id]))


#订食物，如果是GET请求，就返回商店的食物列表的模板供选择，如果是POST，就生成一张订单
@login_required()
def order_food(request, shop_id, food_category_id=None):
    shop = get_object_or_404(Shop, pk=shop_id)
    if request.method == 'GET':
        if food_category_id:
            food_list = Food.objects.query_by_category(shop, food_category_id)
        else:
            food_list = Food.objects.query_by_shop(shop)
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
        food = get_object_or_404(Food, id=food_id)
        food_list.append(food)
        food_number = int(request.POST.get(str(food_id)+'_number'))
        food_number_list.append(food_number)
        food_price_list.append(food.price)
        total += food.price * food_number
    table_no = str(request.POST.get('table_no'))
    while True:
        try:
            num = Order.objects.query_by_today(shop).count() + 1
            order = Order.objects.create(
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
        orderfood = OrderFood(
                     food=food,
                     order=order,
                     nums=food_number_list[i],
                    )
        orderfood.save()
        i += 1
    messages.success(request, '恭喜你，你已经成功下单！')
    return redirect(reverse('geekpoint:get_order', args=[order.id]))


#获取订单视图
@login_required()
def get_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'geekpoint/order_detail.html', {'order': order})


#消费者删除订单视图
@login_required()
def consumer_delete_order(request, order_id):
    order = Order.objects.get(id=order_id)
    if order.check_consumer(request.user):
        order.delete_by_consumer()
        messages.success(request, '删除订单成功！')
        return redirect(reverse('geekpoint:index'))
