from unicodedata import category
from urllib.request import Request
from django.shortcuts import render,get_object_or_404
from .models import Category,Article
from django.db.models import Q,F
from django.core.paginator import Paginator

# Create your views here.


def Index_view(request):

    # category_list = Category.objects.all()
    article_list = Article.objects.all()
    print(article_list)
    paginator = Paginator(article_list,2) #第二个参数2代表每页显示几个
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj':page_obj}
    return render(request,"tliublog/index.html",context)


def category_list(request,category_id):
    # 获取分类下的所有文章
    category = get_object_or_404(Category,id=category_id)
    article_list = category.article_set.all()
    paginator = Paginator(article_list,2) #第二个参数2代表每页显示几个
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'category':category,'page_obj':page_obj}
    
    return render(request,'tliublog/list.html',context)


def article_detail(request,article_id):
    # 文章详情页
    article = get_object_or_404(Article,id = article_id)
    
    # 通过文章id来实现上下篇
    prev_article = Article.objects.filter(id__lt=article_id).last() #上一篇
    next_article = Article.objects.filter(id__gt=article_id).first() #下一篇
    Article.objects.filter(id=article_id).update(pageview = F('pageview')+1)
    # 通过发布日期来实现上下篇
    # date_prev_article = Article.objects.filter(add_date__lt=article.add_date).last() #上一篇
    # date_next_article = Article.objects.filter(add_date__gt=article.add_date).first() #下一篇
    # print(date_prev_article)
    # print(date_next_article)

    context = {"article":article, "prev_article":prev_article,"next_article":next_article}

    return render(request, "tliublog/detail.html",context)


def search(request):

    keyword = request.GET.get('keyword')
    if not keyword:
        article_list = Article.objects.all()
    else:
        article_list = Article.objects.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword) | Q(content__icontains=keyword))
    paginator = Paginator(article_list,2) #第二个参数2代表每页显示几个
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context  = {'page_obj':page_obj}
    return render(request,'tliublog/index.html',context)



def archives(request,year,month):

    article_list = Article.objects.filter(add_date__year=year,add_date__month=month)
    paginator = Paginator(article_list,2) #第二个参数2代表每页显示几个
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj':page_obj,'year':year,'month':month}
    return render(request,'tliublog/archives_list.html',context)
