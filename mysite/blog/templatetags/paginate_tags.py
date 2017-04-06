from django import template
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
#这行代码应该在每个自定义标签的开头，用来向框架注册标签
register = template.Library()

#装饰器，用来注册为标签
@register.simple_tag(takes_context=True)
def paginate(context, object_list, page_count):#模板标签接收参数
    left = 3
    right = 3

    paginator = Paginator(object_list, page_count)
    page = context['request'].GET.get('page')#从上下文字典中取得request对象，再从中取出get信息

    try:
        object_list = paginator.page(page)
        context['current_page'] = int(page)
        pages = get_left(context['current_page'], left, paginator.num_pages) + get_right(context['current_page'], right, paginator.num_pages)
    except PageNotAnInteger:
        object_list = paginator.page(1)
        

