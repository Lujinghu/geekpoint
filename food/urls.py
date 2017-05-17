from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^create_food/(?P<shop_id>\d+)$', views.create_food, name='create_food'),
    url(r'^charge_food/(?P<shop_id>\d+)$', views.charge_food, name='charge_food'),
    url(r'^edit_food/(?P<shop_id>\d+)/(?P<food_id>\d+)$', views.edit_food, name='edit_food'),
    url(r'^delete_food/(?P<shop_id>\d+)/(?P<food_id>\d+)$', views.delete_food, name='delete_food'),
    url(r'^create_foodcategory/(?P<shop_id>\d+)$', views.create_foodcategory, name='create_foodcategory'),
    url(r'^delete_food_category/(?P<shop_id>\d+)/(?P<food_category_id>\d+)$', views.delete_foodcategory, name='delete_foodcategory'),
]