#url(r'^check_all_shop$', views.check_all_shop, name='check_all_shop'),
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^create_shop$', views.create_shop, name='create_shop'),
    url(r'^charge_shop/(?P<shop_id>\d+)$', views.charge_shop, name='charge_shop'),
    url(r'edit_shop/(?P<shop_id>\d+)$', views.edit_shop, name='edit_shop'),
    url(r'delete_shop/(?P<shop_id>\d+)$', views.delete_shop, name='delete_shop'),
]