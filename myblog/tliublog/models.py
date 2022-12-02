from distutils.command.upload import upload
from email.headerregistry import Address
from email.policy import default
from http.client import UNSUPPORTED_MEDIA_TYPE
from pyexpat import model
from re import I, M
from tabnanny import verbose
from this import d
from unittest.util import _MAX_LENGTH
from django.db import models
from django.forms import DateTimeField
from django.test import tag
from django.contrib.auth.models import User
from django.utils.functional import cached_property #缓存装饰器
from django.template.loader import render_to_string # 渲染模板


# Create your models here.
class Category(models.Model):
    '''博客的分类模型'''
    name = models.CharField(max_length=50,verbose_name='分类名称')
    desc = models.TextField(max_length=200,blank=True,default='', verbose_name='分类描述')
    add_date = models.DateTimeField(auto_now_add=True,verbose_name='添加时间')
    pub_date = models.DateTimeField(auto_now_add=True,verbose_name='修改时间')
    

    class Meta:
        verbose_name = "博客分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
 

class Tag(models.Model):
    '''文章标签'''
    name = models.CharField(max_length=50,verbose_name="文章标签")
    add_date = models.DateTimeField(auto_now_add=True,verbose_name='添加时间')
    pub_date = models.DateTimeField(auto_now_add=True,verbose_name='修改时间')

    class Meta:
        verbose_name = "文章标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name



class Article(models.Model):
    '''文章'''
    title = models.CharField(max_length=50,verbose_name='文章标题')
    desc = models.TextField(max_length=200,verbose_name="文章描述")
    category = models.ForeignKey(Category,on_delete=models.CASCADE,verbose_name="文章分类")
    content = models.TextField(verbose_name="文章内容")
    tags = models.ForeignKey(Tag,on_delete=models.CASCADE,verbose_name="文章标签")
    author = models.ForeignKey(User, verbose_name="作者", on_delete=models.CASCADE)
    is_hot = models.BooleanField(default=False,verbose_name="是否热门")  # 手动热门推荐
    pageview = models.IntegerField(default=0,verbose_name="浏览量")
    add_date = models.DateTimeField(auto_now_add=True,verbose_name='添加时间')
    pub_date = models.DateTimeField(auto_now_add=True,verbose_name='修改时间')
    

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name
        ordering = ['-pub_date']

    def __str__(self):
        return self.title

class Sidebar(models.Model):
    # 侧边栏的模型数据

    STATUS = (
        (1, '隐藏'),
        (2, '展示')
    )

    DISPLAY_TYPE = (
        (1, '搜索'),
        (2, '最新文章'),
        (3, '最热文章'),
        (4, '最近评论'),
        (5, '文章归档'),
        (6, 'HTML')
    )
    title = models.CharField(max_length=50, verbose_name="模块名称")
    display_type = models.PositiveBigIntegerField(default=1,choices=DISPLAY_TYPE,verbose_name="展示类型")
    content = models.CharField(max_length=500,blank=True,default='',verbose_name="内容",help_text="如果设置的不是HTML类型,可为空")
    sort = models.PositiveIntegerField(default=1,verbose_name="排序",help_text="序号越大越靠前")
    status = models.PositiveIntegerField(default=2,choices=STATUS,verbose_name="状态")
    add_date = models.DateTimeField(auto_now_add=True,verbose_name="发布时间")


    class Meta:
        verbose_name = "侧边栏"
        verbose_name_plural = verbose_name
        ordering = ['-sort']
    def __str__(self):
        return self.title

    @classmethod   # 类方法装饰器，这个就变成了这个类的一个方法，可以调用
    def get_sidebar(cls):
        return cls.objects.filter(status=2)  # 允许展示的模块

    @property   #成为一个类属性，调用的时候不需要后面（），是只读的，用户没办法修改
    def get_content(self):
        if self.display_type == 1:
            context = {}
            return render_to_string('tliublog/sidebar/search.html', context)
        elif self.display_type == 2:
            context = {}
            return render_to_string('tliublog/sidebar/new_article.html',context)
        elif self.display_type == 3:
            context = {}
            return render_to_string('tliublog/sidebar/hot_article.html', context)
        elif self.display_type == 4:  
            context = {}
            return render_to_string('tliublog/sidebar/comment.html', context)
        elif self.display_type == 5:   # 文章归档
            context = {}
            return render_to_string('tliublog/sidebar/archives.html', context)
        elif self.display_type == 6:   # 自定义侧边栏
           
            return self.content   # 在侧边栏直接使用这里的html，模板中必须使用safe过滤器去渲染HTML


    
    
    