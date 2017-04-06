from django.shortcuts import render
from django.views import generic
from .models import Article, Category
import markdown2

# Create your views here.
class IndexView(generic.ListView):
    template_name = "blog/index.html"
    context_object_name = "article_list"

    #因为所有的ListView中都依靠该函数从数据库中读取并且返回数据集合，所以如果没有自定义这个方法，就要提供model属性以指明数据表
    def get_queryset(self):
        article_list = Article.objects.filter(status='p')
        for article in article_list:
            article.body = markdown2.markdown(article.body)
        return article_list

    #下面的方法用于传递给模板一个以字典形式存储的额外参数
    def get_context_data(self, **kwargs):
        kwargs['category_list'] = Category.objects.all().order_by('name')
        return super(IndexView, self).get_context_data(**kwargs)


class ArticleDetailView(generic.DetailView):
    template_name = "blog/article_detail.html"
    model = Article