from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^order_mark/(?P<shop_id>\d+)/(?P<order_id>\d+)$', views.shop_mark_order, name='order_mark'),
    url(r'^shop_delete_order/(?P<shop_id>\d+)/(?P<order_id>\d+)$', views.shop_delete_order, name='shop_delete_order'),
    url(r'^order_food/(?P<shop_id>\d+)$', views.order_food, name='order_food'),
    url(r'^order_food/(?P<shop_id>\d+)/(?P<food_category_id>\d+)$', views.order_food, name='order_food'),
    url(r'^get_order/(?P<order_id>\d+)$', views.get_order, name='get_order'),
    url(r'^consumer_delete_order/(?P<order_id>\d+)$', views.consumer_delete_order, name='consumer_delete_order'),
]