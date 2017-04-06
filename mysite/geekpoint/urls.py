from django.conf.urls import include, url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create_shop$', views.create_shop, name='create_shop'),
    url(r'^charge_shop/(?P<shop_id>\d+)$', views.charge_shop, name='charge_shop'),
    url(r'edit_shop/(?P<shop_id>\d+)$', views.edit_shop, name='edit_shop'),
    url(r'delete_shop/(?P<shop_id>\d+)$', views.delete_shop, name='delete_shop'),
    url(r'^create_food/(?P<shop_id>\d+)$', views.create_food, name='create_food'),
    url(r'^charge_food/(?P<shop_id>\d+)$', views.charge_food, name='charge_food'),
    url(r'^edit_food/(?P<food_id>\d+)$', views.edit_food, name='edit_food'),
    url(r'^delete_food/(?P<food_id>\d+)$', views.delete_food, name='delete_food'),
    url(r'^order_mark/(?P<order_id>\d+)$', views.shop_mark_order, name='order_mark'),
    url(r'^order_delete/(?P<order_id>\d+)$', views.shop_delete_order, name='order_delete'),
    url(r'^check_all_shop$', views.check_all_shop, name='check_all_shop'),
    url(r'^order_food/(?P<shop_id>\d+)$', views.order_food, name='order_food'),
    url(r'^get_order/(?P<order_id>\d+)$', views.get_order, name='get_order'),
]