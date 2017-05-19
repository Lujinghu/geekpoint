from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^vip_add/(?P<shop_id>\d+)/(?P<user_id>\d+)/$', views.vip_add, name='vip_add'),
    url(r'^vip_deactive/(?P<shop_id>\d+)/(?P<user_id>\d+)/$', views.vip_deactive, name='vip_deactive'),
    url(r'^vip_active/(?P<shop_id>\d+)/(?P<user_id>\d+)/$', views.vip_active, name='vip_active'),
]