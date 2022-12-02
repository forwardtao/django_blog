# 在这里自定义模板标签
from django import template
from tliublog.models import Category,Sidebar,Article

register  = template.Library()

@register.simple_tag
def get_category_list():
    
    return Category.objects.all()

@register.simple_tag
def get_sidebar_list():

    return Sidebar.get_sidebar()

@register.simple_tag
def  get_new_article():

    return  Article.objects.order_by('-pub_date')[:8]

# @register.simple_tag
# def get_hot_article():
#     # 手动设置热门（admin后台设置）
#     return Article.objects.filter(is_hot=True)[:8]

@register.simple_tag
def get_hot_pageview_article():
    # 通过浏览量判断热门
    return Article.objects.order_by('-pageview')[:2]



@register.simple_tag
def get_archives():
    return Article.objects.dates('add_date','month',order='DESC')[:4]