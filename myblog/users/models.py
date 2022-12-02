from tabnanny import verbose
from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class UserProfile(models.Model):

    USER_GENER_TYPE = (('male','男'),('female','女'),)

    owner = models.OneToOneField(User,on_delete=models.CASCADE,verbose_name = '用户')
    nike_name = models.CharField('昵称',max_length=50,blank=True,default='')
    birthday = models.DateField('生日',null=True,blank=True)
    gender = models.CharField('性别',max_length=6,choices = USER_GENER_TYPE,default='male')
    address = models.CharField('地址',max_length=100,blank=True,default='')
    desc = models.TextField('个人简介',max_length=200,blank=True,default='')
    gexing = models.CharField('个性签名',max_length=100,blank=True,default='')
    image =  models.ImageField(upload_to = 'image/%Y%m',default='image/default.png',max_length = 100,verbose_name='用户头像')


    class Meta:
        verbose_name = '用户数据'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.owner.username

class EmailVertifyRecord(models.Model):
    '''邮箱验证码校验'''
    send_type_choice = (('register','注册'),('forget','找回密码'))
    
    code = models.CharField('验证码',max_length=20)
    email = models.EmailField('邮箱',max_length=35)
    send_type = models.CharField(choices=send_type_choice,default='register', max_length=20)

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.code