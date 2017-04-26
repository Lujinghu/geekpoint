import time
from django.shortcuts import render, get_object_or_404
from . import forms
from . import models
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import functools
from django.contrib import messages

#再研究一下，能不能将已经查询出来的shop传递给视图函数，这样就可以避免查找两次了
#@login_required()#将两个装饰器合并，节省代码量
#注意，似乎这个装饰器不能用来装饰一个装饰器？只能用来装饰这个装饰器里面的函数
#所以装饰器定义在上面会报错
def check_manager_dec(func):
    '''
    装饰器，用来判断当前用户是否商店的管理人员，从而判断是不是应该拒绝访问
    :param func: 
    :return: 
    '''
    @login_required()
    @functools.wraps(func)#python内置的装饰器，用来给装饰器返回的新函数的__name__属性进行更改，改回跟原来同名就好了
    def wrapper(request, *args, **kwargs):
        '''
        if kwargs.get('shop_id'):#注意，之前直接使用字典索引查询值，，由于没有查找到该值，所以抛出了一个keyerror，正确来说应该使用dict内置的get方法，找不到就会返回false
            shop = get_object_or_404(models.Shop, id=kwargs['shop_id'])
        elif kwargs['order_id']:
            shop = get_object_or_404(models.Order, id=kwargs['order_id']).shop
        if shop.check_manager(request.user):
            #return True
        '''
        shop = get_object_or_404(models.Shop, id=kwargs.get('shop_id'))
        user = request.user
        if shop.check_manager(user):
            return func(request, *args, **kwargs)
    return wrapper

def return_index():
    return HttpResponseRedirect(reverse('geekpoint:index'))


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
        shop.shop_managers.add(request.user)
        #上面有点出错了，因为多对多字段是一个set，所以不能像下面那样当作外键那样直接赋值，应该使用add
        #shop.shop_manager = request.user
        shop.save()
        messages.success(request, "你已经成功创建商店: %s！" % shop.name)
        return HttpResponseRedirect(reverse('geekpoint:index'))
    else:
        return render(request, 'geekpoint/edit_shop.html', {'form': form})


# 商店管理视图，展示订单信息，以及商店的管理信息
#注意，如果装饰器没有参数，就不要带上一个多余的括号，否则，可能就会出现异常
@check_manager_dec
def charge_shop(request, shop_id):
    shop = get_object_or_404(models.Shop, pk=shop_id)
    # order_list = shop.order_set.filter(created_time__day=timezone.now().day)#m妈蛋，这句查询语句出了问题，真是坑爹
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
#优化了一下代码
@check_manager_dec
#@login_required()
def edit_shop(request, shop_id):
    shop = get_object_or_404(models.Shop, pk=shop_id)  #注意，这里我犯了一个错误，虽然路由的参数会被框架自动传入，可是也得我们在视图函数里面声明参数才行
    if request.method == 'POST':
        form = forms.ShopForm(instance=shop, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '商店信息更新成功！')
            return HttpResponseRedirect(reverse('geekpoint:charge_shop', kwargs={'shop_id': shop_id}))
    else:
        form = forms.ShopForm(instance=shop)
    return render(request, 'geekpoint/edit_shop.html', {'form': form})
    #注意，reverse函数只是根据视图名反向解析出一个url值，而不是响应，所以要用重定向函数生成响应对象


#删除商店
@check_manager_dec
#@login_required()
def delete_shop(request, shop_id):
    shop = get_object_or_404(models.Shop, pk=shop_id)
    shop.delete()
    return_index()


#管理食物信息视图，查询并且返回现在的食物清单
#@login_required()
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
#@login_required()
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
    if request.method == 'GET':
        form = forms.FoodForm()
        context['form'] = form
        return render(request, 'geekpoint/create_food.html', context)
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
        return HttpResponseRedirect(reverse('geekpoint:charge_food', args=[shop_id]))
        #上面返回渲染的时候出了问题，应该是reverse函数没有用好
    else:
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
        return HttpResponseRedirect(reverse('geekpoint:create_food', args=[shop_id]))
    else:
        return HttpResponseRedirect(reverse('geekpoint:create_food', args=[shop_id]))


#@login_required()
@check_manager_dec
def delete_foodcategory(request, food_category_id):
    food_category = get_object_or_404(models.FoodCategory, id=food_category_id)
    food_category.delete()
    return HttpResponseRedirect(reverse('geekpoint:create_food', args=[food_category.shop.id]))

#变更食品信息;问题，想办法将它跟创建食品的视图合并
#@login_required()
@check_manager_dec
def edit_food(request, food_id):
    food = get_object_or_404(models.Food, pk=food_id)
    if request.method == 'GET':
        #渲染一张食物视图表单
        form = forms.FoodForm(instance=food)
        return render(request, 'geekpoint/edit_food.html', {'form': form, 'food_id': food_id})
    form = forms.FoodForm(request.POST, instance=food)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('geekpoint:charge_food', args=[food.shop.pk]))
    else:
        return render(request, 'geekpoint/edit_food.html', {'form': form, 'food_id': food_id})


#删除食品信息
#@login_required()
@check_manager_dec
def delete_food(request, food_id):
    food = get_object_or_404(models.Food, pk=food_id)
    food.delete()
    return HttpResponseRedirect(reverse('geekpoint:charge_food', kwargs={'shop_id': food.shop.pk }))


#浏览商店视图，可以查看所有的商店信息，并且提供到店消费的链接
@login_required()
def check_all_shop(request):
    shop_list = models.Shop.objects.all()
    return render(request, 'geekpoint/check_all_shop.html', {'shop_list': shop_list})


#商户后台标记订单状态
@check_manager_dec
#@login_required()
def shop_mark_order(request, order_id):
    order = get_object_or_404(models.Order, pk=order_id)
    order.status = request.POST.get('status')
    order.save()
    return HttpResponseRedirect(reverse('geekpoint:charge_shop', args=[order.shop.pk]))
    #额，之后应该怎么处理？直接返回原来的页面？？


#商户后台删除订单
#@login_required()
@check_manager_dec
def shop_delete_order(request, order_id):
    order = get_object_or_404(models.Order, pk=order_id)
    order.is_delete_by_shop = True
    order.save()#计划使用软删除
    return HttpResponseRedirect(reverse('geekpoint:charge_shop', args=[order.shop.pk]))


#订食物，如果是GET请求，就返回商店的食物列表的模板供选择，如果是POST，就生成一张订单
@login_required()
def order_food(request, shop_id, food_category_id=None):
    #如果是get方法，直接返回相关context用于生成点餐页面
    shop = get_object_or_404(models.Shop, pk=shop_id)
    '''
    if request.method == 'GET':
        food_category_id = request.GET.get('food_category_id')
        if food_category_id:
            food_list = models.Food.objects.query_by_category(shop, food_category_id)
        else:
            food_list = models.Food.objects.query_by_shop(shop)
        
    '''
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
    food_id_list = request.POST.getlist('food_id_list')#在点餐页面中是多选框，所以通过POST对象获取多选框的数据，返回值是一个list列表
    #food_num_list = request.POST.getlist('food_num_list')
    #装下逼，使用列表生成式，这样比较pythonic
    #food_list = [get_object_or_404(models.Food, pk=food_id) for food_id in food_id_list]
    #food_number_list = [request.POST.get(str(food.id)+'_number') for food in ]
    food_list = []
    food_number_list = []
    food_price_list = []
    total = 0
    for food_id in food_id_list:
        food = get_object_or_404(models.Food, id=food_id)
        food_list.append(food)
        food_number = int(request.POST.get(str(food_id)+'_number'))#注意，除了好久的bug我才发现了这个问题，因为从表单中捕捉到的值都是字符串，不能上来就用来计算总价
        food_number_list.append(food_number)
        food_price_list.append(food.price)
        total += food.price * food_number
        #return render(request, 'geekpoint/test.html', {'food_id_list': food_id_list, 'food_number_list': food_number_list, 'food_price_list': food_price_list, 'total': total})
    #food_price_list = [food.price for food in food_list]
    #total = sum(food_price_list)
    table_no = str(request.POST.get('table_no'))
    #尝试解决并发环境下订单号重复问题
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
    #check_consumer(request, order)
    if order.check_consumer(request.user):
        order.is_delete_by_consumer = True
        order.save()
        return HttpResponseRedirect(reverse('geekpoint:index'))









