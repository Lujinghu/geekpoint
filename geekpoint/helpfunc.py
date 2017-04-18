from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
#思考一下，能不能改成一个装饰器??
#权限系统控制不了
#抽象出来一个check_owner方法，用来检查用户是否商店的主人，从而确定权限
#抽象出来一个
def return_index():
    return HttpResponseRedirect(reverse('geekpoint:index'))

def check_manager(request, shop):
    if request.user in shop.shop_managers.all():
        return True
    else:
        return_index()

def check_consumer(request, order):
    if request.user is order.consumer:
        return True
    else:
        return_index()