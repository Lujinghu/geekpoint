from django.conf.urls import url
from .views import IndexView, ArticleDetailView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index' ),
    url(r'^article/(?P<pk>\d+)/', ArticleDetailView.as_view(), name='article_detail')
]