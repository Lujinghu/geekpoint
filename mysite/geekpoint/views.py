from django.shortcuts import render, get_object_or_404
from django.contrib import auth
from . import forms
from . import models
from django.utils import timezone
import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

#思考一下，能不能改成一个装饰器??
#不知道能不能用权限控制来控制它，蛋疼，现在就先这样吧
#抽象出来一个check_owner方法，用来检查用户是否商店的主人，从而确定权限
def check_owner(request, shop, message='You are not the owner.', redirect_url='geekpoint:index'):
    pass


# Create your views here.
#定义首页视图，如果用户已经登陆，则显示进入或者注册商户的入口，如果未登录，则显示请登录
def index(request):
    if request.user.is_authenticated():
        user = request.user
        history_order_list = models.Order.objects.query_by_user(user)
        #history_order_list = user.order_set.all().order_by('-created_time')[:5]#注意，可能出现空list，空list不能直接通过if语句判断为空
        charge_shop_list = models.Shop.objects.query_by_user(user)
        context = {'history_order_list': history_order_list, 'charge_shop_list': charge_shop_list}
        return render(request, 'geekpoint/index.html', context)
    return render(request, 'geekpoint/index.html')


#创建商店
@login_required
def create_shop(request):
    if request.method == 'GET':
        form = forms.ShopForm()
        return render(request, 'geekpoint/edit_shop.html', {'form': form})
    form = forms.ShopForm(request.POST)
    if form.is_valid():
        shop = form.save(commit=False)#注意，由于表单中并不包含所有的字段，所以在调用表单对象的save（）方法是，选择不提交，然后额外设置其他的参数
        shop.save()#终于明白了，由于多对多关系的建立，django中是通过额外增加一个第三方的表格来建立这样的多对多关系的，而要建立这样的一个
        #第三方的表格，则必须提供索引，也就是必须两个多对多关系的对象都要先保存好，才能产生索引来使用
        #而不像多对一关系那样，多对一关系只是在其中一个表格保存另一个表格的索引而已。
        shop.shop_manager.add(request.user) #这里出错了，因为多对多字段是一个set，所以不能直接这样赋值
        #shop.shop_manager = request.user
        shop.save()
        return HttpResponseRedirect(reverse('geekpoint:index'))


# 商店管理视图，展示订单信息，以及商店的管理信息
@login_required()
def charge_shop(request, shop_id):
    shop = get_object_or_404(models.Shop, pk=shop_id)
    check_owner(request, shop)
    # order_list = shop.order_set.filter(created_time__day=timezone.now().day)#m妈蛋，这句查询语句出了问题，真是坑爹
    order_list = models.Order.objects.query_by_shop(shop)
    x_order_list = models.Order.objects.query_by_status('x', shop)
    q_order_list = models.Order.objects.query_by_status('q', shop)
    context = {
        'shop': shop,
        'x_order_list': x_order_list,
        'q_order_list': q_order_list,
    }
    return render(request, 'geekpoint/charge_shop.html', context)


#更改商店信息视图,变更成功则返回charge_shop视图
@login_required()
def edit_shop(request, shop_id):
    shop = get_object_or_404(models.Shop, pk=shop_id)  #注意，这里我犯了一个错误，虽然路由的参数会被框架自动传入，可是也得我们在视图函数里面声明参数才行
    if request.method == 'GET':
        check_owner(request, shop)
        form = forms.ShopForm(instance=shop)
        return render(request, 'geekpoint/edit_shop.html', {'form': form})
    form = forms.ShopForm(request.POST, instance=shop)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('geekpoint:charge_shop', kwargs={'shop_id': shop_id}))
    #注意，reverse函数只是根据视图名反向解析出一个url值，而不是响应，所以要用重定向函数生成响应对象


#删除商店
@login_required()
def delete_shop(request, shop_id):
    shop = get_object_or_404(models.Shop, pk=shop_id)
    check_owner(request, shop)
    shop.delete()
    return HttpResponseRedirect(reverse('geekpoint:index'))


#管理食物信息视图，查询并且返回现在的食物清单
@login_required()
def charge_food(request, shop_id):
    shop = get_object_or_404(models.Shop, pk=shop_id)
    check_owner(request, shop)
    food_list = models.Food.objects.query_by_shop(shop)
    return render(request, 'geekpoint/charge_food.html', {'shop': shop, 'food_list': food_list})


#新建食品视图，用来新增一个新食品
@login_required()
def create_food(request, shop_id):
    shop = get_object_or_404(models.Shop, pk=shop_id)
    if request.method == 'GET':
        form = forms.FoodForm()
        food_category_form = forms.FoodCategoryForm()
        food_category_list = shop.foodcategory_set.all()
        return render(request, 'geekpoint/create_food.html', {
            'form': form,
            'shop_id': shop_id,
            'food_category_list': food_category_list,
            'food_category_form': food_category_form,
        })
    #check_owner(request, shop)
    form = forms.FoodForm(request.POST)
    if form.is_valid():
        food = form.save(commit=False)
        food.shop = shop
        form.save()
        return HttpResponseRedirect(reverse('geekpoint:charge_food', args=[shop_id]))
        #上面返回渲染的时候出了问题，应该是reverse函数没有用好


def create_foodcategory(request, shop_id):
    if request.method == 'POST':
        food_category_form = forms.FoodCategoryForm(request.POST)
        food_category = food_category_form.save(commit=False)
        food_category.shop = get_object_or_404(models.Shop, id=shop_id)
        food_category.save()
        return HttpResponseRedirect(reverse('geekpoint:create_food', args=[shop_id]))

#变更食品信息
@login_required()
def edit_food(request, food_id):
    food = get_object_or_404(models.Food, pk=food_id)
    check_owner(request, food.shop)
    if request.method == 'GET':
        #渲染一张食物视图表单
        form = forms.FoodForm(instance=food)
        return render(request, 'geekpoint/edit_food.html', {'form': form, 'food_id': food_id})
    form = forms.FoodForm(request.POST, instance=food)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('geekpoint:charge_food', args=[food.shop.pk]))


#删除食品信息
@login_required()
def delete_food(request, food_id):
    food = get_object_or_404(models.Food, pk=food_id)
    check_owner(request, food.shop)
    food.delete()
    return HttpResponseRedirect(reverse('geekpoint:charge_food', kwargs={'shop_id': food.shop.pk }))


#浏览商店视图，可以查看所有的商店信息，并且提供到店消费的链接
@login_required()
def check_all_shop(request):
    shop_list = models.Shop.objects.all()
    return render(request, 'geekpoint/check_all_shop.html', {'shop_list': shop_list})


#商户后台标记订单状态
@login_required()
def shop_mark_order(request, order_id):
    order = get_object_or_404(models.Order, pk=order_id)
    check_owner(request, order.shop)
    order.status = request.POST.get('status')
    order.save()
    return HttpResponseRedirect(reverse('geekpoint:charge_shop', args=[order.shop.pk]))
    #额，之后应该怎么处理？直接返回原来的页面？？


#商户后台删除订单
@login_required()
def shop_delete_order(request, order_id):
    order = get_object_or_404(models.Order, pk=order_id)
    check_owner(request, order.shop)
    order.is_delete_by_shop = True
    order.save()#计划使用软删除
    return HttpResponseRedirect(reverse('geekpoint:charge_shop', args=[order.shop.pk]))


#订食物，如果是GET请求，就返回商店的食物列表的模板供选择，如果是POST，就生成一张订单
@login_required()
def order_food(request, shop_id):
    #如果是get方法，直接返回相关context用于生成点餐页面
    shop = get_object_or_404(models.Shop, pk=shop_id)
    if request.method == 'GET':
        food_list = models.Food.objects.query_by_shop(shop)
        return render(request, 'geekpoint/order_food.html', {'food_list': food_list, 'shop': shop})
    food_id_list = request.POST.getlist('food_id_list')#在点餐页面中是多选框，所以通过POST对象获取多选框的数据，返回值是一个list列表
    #food_num_list = request.POST.getlist('food_num_list')
    #装下逼，使用列表生成式，这样比较pythonic
    food_list = [get_object_or_404(models.Food, pk=food_id) for food_id in food_id_list]
    food_price_list = [food.price for food in food_list]
    total = sum(food_price_list)
    num = models.Order.objects.query_by_today(shop).count()
    order_no = num + 1
    table_no = str(request.POST.get('table_no'))
    order = models.Order.objects.create(
        order_no=order_no,
        shop=shop,
        consumer=request.user,
        table_no=table_no,
        total=total
    )
    #在订单和食物的多对多关联列表中保存数据
    for food in food_list:
        orderfood = models.OrderFood(
                     food=food,
                     order=order,
                     nums=1,
                    )
        orderfood.save()
    return HttpResponseRedirect(reverse('geekpoint:index'))


#获取订单视图
@login_required()
def get_order(request, order_id):
    order = get_object_or_404(models.Order, pk=order_id)
    return render(request, 'geekpoint/order_detail.html', {'order': order})












