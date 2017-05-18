from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from shop.decorators import check_manager_dec
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from shop.models import Shop
from .models import Order, OrderFood
from food.models import Food
import time
from cart.cart import Cart
from django.views.decorators.http import require_POST, require_GET

# Create your views here.
#商户后台标记订单状态
@check_manager_dec
def shop_mark_order(request, shop_id, order_id):
    order = get_object_or_404(Order, pk=order_id)
    #order.status = request.POST.get('status')
    #order.save()
    order.change_status(request.POST.get('status'))
    messages.success(request, '订单状态已更改！')
    return redirect(reverse('shop:charge_shop', args=[shop_id]))


@check_manager_dec
def shop_delete_order(request, shop_id, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.delete_by_shop()
    messages.success(request, '订单已经删除')
    return redirect(reverse('shop:charge_shop', args=[shop_id]))


#订食物，如果是GET请求
@require_GET
@login_required()
def order_food(request, shop_id, food_category_id=None):
    shop = get_object_or_404(Shop, pk=shop_id)
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
    return render(request, 'order/order_food.html', context)


@require_POST
@login_required()
def order_create(request, shop_id):
    cart = Cart(request)
    shop = get_object_or_404(Shop, id=shop_id)
    while True:
        try:
            num = Order.objects.query_by_today(shop).count() + 1
            order = Order.objects.create(
                order_no=num,
                shop=shop,
                consumer=request.user,
                table_no=cart.table_no,
                total=cart.get_total_price(),
            )
            break
        except BaseException:
            pass
    order.order_no = str(int(time.mktime(order.created_time.timetuple()))) + str(order.order_no)
    order.save()
    #在订单和食物的多对多关联列表中保存数据
    i = 0
    for food in cart:
        orderfood = OrderFood(
                     food=food,
                     order=order,
                     nums=food['quantity'],
                    )
        orderfood.save()
        i += 1
    cart.clear()
    messages.success(request, '恭喜你，你已经成功下单！')
    return redirect(reverse('order:get_order', args=[order.id]))


#获取订单视图
@login_required()
def get_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'order/order_detail.html', {'order': order})


#消费者删除订单视图
@login_required()
def consumer_delete_order(request, order_id):
    order = Order.objects.get(id=order_id)
    if order.check_consumer(request.user):
        order.delete_by_consumer()
        messages.success(request, '删除订单成功！')
        return redirect(reverse('geekpoint:index'))


@check_manager_dec
def get_today_order(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id)
    today_order_list = Order.objects.query_by_today(shop)