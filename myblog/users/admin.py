from django.contrib import admin
from django.contrib.auth.models import User
# Register your models here.
from .models import UserProfile,EmailVertifyRecord
#这个用户选项就是官方默认通过Useradmin 这个类注册到后台的，那么我们也引入进来，后边继承这个类

from django.contrib.auth.admin import UserAdmin


#取消关联注册User
admin.site.unregister(User)

#定义关联对象的样式，sta
class UserProfileInline(admin.StackedInline):
    model = UserProfile

class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline]

admin.site.register(User,UserProfileAdmin)

@admin.register(EmailVertifyRecord)
class Admin(admin.ModelAdmin):
    '''admin view for'''
    list_display = ('code',)
