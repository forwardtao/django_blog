import email
from multiprocessing import context
# import pwd
import re
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate, login,logout
from django.urls import is_valid_path
from .forms import LoginForm,RegisterForm,ForgetPwdForm,ModifyPwdForm, UserForm, UserProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth.hashers import make_password  #引入将密码转为hash值

from .models import EmailVertifyRecord,UserProfile
from utils.email_send import send_register_email
from django.contrib.auth.decorators import login_required





class MyBackend(ModelBackend):
    '''邮箱登录注册'''
    def authenticate(self, request, username=None, password=None, **kwargs):
        try :
            user = User.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password): #加密明文密码
                return user
        except Exception as e:
            return None

def active_user(request,active_code):
    '''修改用户状态，比对邮箱链接验证码'''
    all_records = EmailVertifyRecord.objects.filter(code=active_code)
    if all_records:
        for record in all_records:
            email = record.email
            user = User.objects.get(email=email)
            user.is_staff = True
            user.save
    else:
        return HttpResponse('链接有误/失效')
    return redirect('users:login')


# Create your views here.
def login_view(request):
    '''登录视图'''
    # if request.method == 'POST':
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')
    #     user = authenticate(request,username=username,password=password)
    #     if user is not None:
    #         login(request,user)
    #         return HttpResponse('登录成功')
    #     else:
    #         return HttpResponse('登录失败')                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              

    #     print(username,password)

    # return render(request,'users/login.html')
    if request.method != 'POST':
        form = LoginForm()
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                #登录成功跳转到个人中心
                return redirect('users:user_profile')
            else:
                #登录失败验证不通过
                return HttpResponse('账号或者密码错误')
    context = {'form':form}
    return render(request, 'users/login.html', context)

def register(request):
    
    '''注册视图'''
    if request.method != 'POST':
        form = RegisterForm()

    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data.get('password'))
            new_user.username = form.cleaned_data.get('email')
            new_user.save()

            #发送邮件
            send_register_email(form.cleaned_data.get('email'),'register')
            return HttpResponse('注册成功')
    context = {'form':form}
    return render(request, 'users/register.html',context)

def forget_pwd(request):

    if request.method == 'GET':
        form = ForgetPwdForm()
    elif request.method == 'POST':
        form = ForgetPwdForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            exists = User.objects.filter(email=email).exists()
            if exists:
                send_register_email(email,'forget')
                return HttpResponse('邮件已发送请查收！')
            else:
                return HttpResponse('邮箱还未注册，请前往注册')
    return render(request,'users/forget_pwd.html',{'form':form})
            
    

def forget_pwd_url(request,active_code):

    if request.method !='POST':
        form = ModifyPwdForm()
    else:
        form = ModifyPwdForm(request.POST)
        if form.is_valid():
            record = EmailVertifyRecord.objects.get(code=active_code)
            email = record.email
            user = User.objects.get(email=email)
            user.username = email
            user.password = make_password(form.cleaned_data.get('password')) 
            user.save()
            return HttpResponse('密码修改成功')
        else:
            return HttpResponse('密码修改失败')
    return render(request,'users/reset_pwd.html',{'form':form})
    

@login_required(login_url='users:login')
def user_profile(request):
    '''用户中心'''
    user = User.objects.get(username=request.user)
    return render(request,'users/user_profile.html',{'user':user})


def logout_view(request):
    '''退出登录'''
    logout(request)
    return redirect('users:login')

@login_required(login_url='users:login')
def edit_user(request):
    '''编辑用户信息'''
    user = User.objects.get(id=request.user.id) #当前登录用户
    if request.method == "POST":
        try:

            user_profile = user.userprofile
            form = UserForm(request.POST,instance=user)  #instance 显示默认信息
            #user_profile和user是一对一关系，第一次注册时默认没有数据，注册成功才会在个人中心设置信息
            # 第一次注册是空表单，如果设置了数据以后编辑就是修改，应该默认显示原有数据
            user_profile_form = UserProfileForm(request.POST,request.FILES,instance=user_profile)
            if form.is_valid() and user_profile_form.is_valid():
                form.save()
                user_profile_form.save()
                return redirect("users:user_profile")
        except UserProfile.DoesNotExist:
            form = UserForm(request.POST,instance=user)  
            user_profile_form = UserProfileForm(request.POST,request.FILES)
            if form.is_valid() and user_profile_form.is_valid():
                form.save()
                user_profile_form.save()
                return redirect("users:user_profile")
    else:
        try:
            userprofile = user.userprofile
            form = UserForm(instance=user)
            user_profile_form = UserProfileForm(instance=userprofile) 
        except UserProfile.DoesNotExist:
            form = UserForm(instance=user)
            user_profile_form = UserProfileForm()  # 显示空表单

    return render(request,'users/edit_user.html',locals())