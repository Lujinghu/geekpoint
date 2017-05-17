from django.shortcuts import render, get_object_or_404, redirect
from shop.decorators import check_manager_dec
from shop.models import Shop
from .models import Food, FoodCategory
from .forms import FoodCategoryForm, FoodForm
from django.contrib import messages
from django.core.urlresolvers import reverse

#管理食物信息视图，查询并且返回现在的食物清单
@check_manager_dec
def charge_food(request, shop_id):
    shop = get_object_or_404(Shop, pk=shop_id)
    food_list = Food.objects.query_by_shop(shop)
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
    shop = get_object_or_404(Shop, pk=shop_id)
    food_category_form = FoodCategoryForm()
    food_category_list = shop.foodcategory_set.all()
    context = {
        'shop_id': shop_id,
        'food_category_list': food_category_list,
        'food_category_form': food_category_form,
    }
    if request.method == 'POST':
        form = FoodForm(request.POST)
        if form.is_valid():
            food = form.save(commit=False)
            try:
                food_category = FoodCategory.objects.get(id=request.POST.get('food_category_id'))
                food.category = food_category
            except BaseException:
                pass
            food.shop = shop
            form.save()
            messages.success(request, '食品：{}已经创建！'.format(food.name))
            return redirect(reverse('geekpoint:charge_food', args=[shop_id]))
        else:
            context['form'] = form
    else:
        form = FoodForm()
        context['form'] = form
    return render(request, 'geekpoint/create_food.html', context)


#@login_required()
@check_manager_dec
def create_foodcategory(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id)
    if request.method == 'POST':
        food_category_form = FoodCategoryForm(request.POST)
        if food_category_form.is_valid():
            food_category = food_category_form.save(commit=False)
            food_category.shop = shop
            food_category.save()
            messages.success(request, '你已成功创建食品分类：% s' % food_category.name)
    return redirect(reverse('geekpoint:create_food', args=[shop_id]))


@check_manager_dec
def delete_foodcategory(request, shop_id, food_category_id):
    food_category = get_object_or_404(FoodCategory, id=food_category_id)
    food_category.delete()
    messages.success(request, '食物分类已经删除！')
    return redirect(reverse('geekpoint:create_food', args=[shop_id]))


@check_manager_dec
def edit_food(request, shop_id, food_id):
    food = get_object_or_404(Food, pk=food_id)
    if request.method == 'POST':
        form = FoodForm(request.POST, instance=food)
        if form.is_valid():
            form.save()
            return redirect(reverse('geekpoint:charge_food', args=[shop_id]))
    else:
        form = FoodForm(instance=food)
    return render(request, 'geekpoint/edit_food.html', {'form': form, 'food_id': food_id, 'shop_id': shop_id})


@check_manager_dec
def delete_food(request, shop_id, food_id):
    food = get_object_or_404(Food, pk=food_id)
    food.delete()
    messages.success(request, '食物已经删除！')
    return redirect(reverse('geekpoint:charge_food', kwargs={'shop_id': shop_id}))
