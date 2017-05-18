from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from food.models import Food
from .cart import Cart
from .forms import CartAddFoodForm

@require_POST
def cart_add(request, shop_id, food_id=None):
    cart = Cart(request)
    if food_id:
        food = get_object_or_404(Food, food_id)
        form = CartAddFoodForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(food=food, quantity=cd['quantity'], update_quantity=cd['update'])
            return redirect('cart:cart_detail')
    food_id_list = request.POST.getlist('food_id_list')
    table_no = str(request.POST.get('table_no'))
    message = str(request.POST.get('message'))
    cart.table_no = table_no
    cart.message = message
    food_list = []
    food_quantity_list = []
    for food_id in food_id_list:
        food = get_object_or_404(Food, id=food_id)
        food_list.append(food)
        food_quantity = int(request.POST.get(str(food_id)+'_number'))
        food_quantity_list.append(food_quantity)
        cart.add(food=food, quantity=food_quantity, update_quantity=False)
        return redirect('cart:cart_detail', args=(shop_id, ))


def cart_remove(request, food_id):
    cart = Cart(request)
    food = get_object_or_404(Food, food_id)
    cart.remove(food)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    #对餐车对象迭代会得到字典
    for item in cart:
        item['update_quantity_form'] = CartAddFoodForm(
            initial={'quantity': item['quantity'], 'update': True}
        )
    return render(request, 'cart.detail.html', {'cart': cart})