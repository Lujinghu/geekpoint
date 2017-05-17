import functools
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
from .models import Shop
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
        shop = get_object_or_404(Shop, id=kwargs.get('shop_id'))
        user = request.user
        if shop.check_manager(user):
            return func(request, *args, **kwargs)
        else:
            messages.error(request, '对不起，您不是这家商店的管理员，无权进行该操作！！')
            return redirect(reverse('geekpoint:index'))
    return wrapper
