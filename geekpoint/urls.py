from django.conf.urls import include, url
from . import views

#尝试定义两个不同的url匹配同一个view函数，这样会更简单一点，理论上只要为视图函数赋予一个恰当的初值就可以了，然后另外定义一个不带参数的路由URL来提供匹配
#注意，我之前在这个地方出国过错误，误以为只要给视图函数赋予一个default值就可以了，也试过将url上的路由参数使用*正则匹配符来进行匹配，然而并不行
#可以使用巧妙的include方法来简化下面的路由，也就是将路由参数提前，然后将后面的不同的部分include进来
'''
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create_shop$', views.create_shop, name='create_shop'),
    url(r'^(?P<shop_id>\d+)/', include([
        url(r'^charge_shop$', views.charge_shop, name='charge_shop'),
        url(r'^edit_shop$', views.edit_shop, name='edit_shop'),
        url(r'^delete_shop$', views.delete_shop, name='delete_shop'),
        url(r'^create_food$', views.create_food, name='create_food'),
        url(r'^charge_food$', views.charge_food, name='charge_food'),
        url(r'^order_food$', views.order_food, name='order_food'),
        url(r'^create_foodcategory', views.create_foodcategory, name='create_foodcategory'),
        url(r'^(?P<food_category_id>\d+)/order_food$', views.order_food, name='order_food'),
    ])),
    url(r'^(?P<food_id>\d+)/', include([
        url(r'^edit_food$', views.edit_food, name='edit_food'),
        url(r'^delete_food$', views.delete_food, name='delete_food'),
    ])),
    url(r'^(?P<order_id>\d+)/', include([
        url(r'^order_mark$', views.shop_mark_order, name='order_mark'),
        url(r'^shop_delete_order$', views.shop_delete_order, name='shop_delete_order'),
        url(r'^get_order$', views.get_order, name='get_order'),
        url(r'^consumer_delete_order$', views.consumer_delete_order, name='consumer_delete_order'),
    ])),
    url(r'^check_all_shop$', views.check_all_shop, name='check_all_shop'),
    url(r'^(?P<food_category_id>\d+)/', include([
        url(r'^delete_foodcategory$', views.delete_foodcategory, name='delete_foodcategory'),
    ])),
]
'''
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create_shop$', views.create_shop, name='create_shop'),
    url(r'^charge_shop/(?P<shop_id>\d+)$', views.charge_shop, name='charge_shop'),
    url(r'edit_shop/(?P<shop_id>\d+)$', views.edit_shop, name='edit_shop'),
    url(r'delete_shop/(?P<shop_id>\d+)$', views.delete_shop, name='delete_shop'),
    url(r'^create_food/(?P<shop_id>\d+)$', views.create_food, name='create_food'),
    url(r'^charge_food/(?P<shop_id>\d+)$', views.charge_food, name='charge_food'),
    url(r'^edit_food/(?P<shop_id>\d+)/(?P<food_id>\d+)$', views.edit_food, name='edit_food'),
    url(r'^delete_food/(?P<shop_id>\d+)/(?P<food_id>\d+)$', views.delete_food, name='delete_food'),
    url(r'^order_mark/(?P<shop_id>\d+)/(?P<order_id>\d+)$', views.shop_mark_order, name='order_mark'),
    url(r'^shop_delete_order/(?P<shop_id>\d+)/(?P<order_id>\d+)$', views.shop_delete_order, name='shop_delete_order'),
    url(r'^check_all_shop$', views.check_all_shop, name='check_all_shop'),
    url(r'^order_food/(?P<shop_id>\d+)$', views.order_food, name='order_food'),
    url(r'^order_food/(?P<shop_id>\d+)/(?P<food_category_id>\d+)$', views.order_food, name='order_food'),
    url(r'^get_order/(?P<order_id>\d+)$', views.get_order, name='get_order'),
    url(r'^create_foodcategory/(?P<shop_id>\d+)$', views.create_foodcategory, name='create_foodcategory'),
    url(r'^consumer_delete_order/(?P<order_id>\d+)$', views.consumer_delete_order, name='consumer_delete_order'),
    url(r'^delete_food_category/(?P<shop_id>\d+)/(?P<food_category_id>\d+)$', views.delete_foodcategory, name='delete_foodcategory'),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^logout-then-login/$', 'django.contrib.auth.views.logout_then_login', name='logout_then_login'),
    url(r'^password-change/$', 'django.contrib.auth.views.password_change', name='password_change'),
    url(r'^password-change/done/$', 'django.contrib.auth.views.password_change_done', name='password_change_done'),
    url(r'^password-reset/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
    url(r'^password-reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    #url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', name='password_reset_confirm'),
    url(r'^password-reset/complete/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),
    url(r'^register/$', views.register, name='register'),
]