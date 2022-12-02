from dataclasses import fields
from logging import PlaceHolder
from pyexpat import model
from urllib import request
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile




class LoginForm(forms.Form):
    '''登录表单'''
    username = forms.CharField(label='用户名', max_length=32,widget=forms.TextInput(attrs={'class':'input','placeholder':'用户名/邮箱'}))
    password = forms.CharField(label='密码', min_length=6 ,widget=forms.PasswordInput(attrs={'class':'input','placeholder':'密码'}))

    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username == password:

            raise forms.ValidationError('用户名与密码不能一致')
        return password

class RegisterForm(forms.ModelForm):
    '''注册表单'''
    email = forms.CharField(label='邮箱', max_length=32,widget=forms.TextInput(attrs={'class':'input','placeholder':'邮箱'}))
    password = forms.CharField(label='密码', min_length=6 ,widget=forms.PasswordInput(attrs={'class':'input','placeholder':'密码'}))
    password1 = forms.CharField(label='再次输入密码', min_length=6 ,widget=forms.PasswordInput(attrs={'class':'input','placeholder':'再次输入密码'}))
    class Meta:
        model = User
        fields = ('email','password')

    def clean_email(self):
        '''验证邮箱是否存在'''
        email = self.cleaned_data.get('email')
        exists = User.objects.filter(username=email).exists()
        if exists:
            raise forms.ValidationError('邮箱已存在')
        return email

    def clean_password1(self):
        '''验证密码输入是否一致'''
        password = self.cleaned_data.get('password')
        password1 = self.cleaned_data.get('password1')
        if password1 != password:
            raise forms.ValidationError('密码输入不一致')
        return password1

class ForgetPwdForm(forms.Form):
    '''忘记密码,填写邮箱地址表单'''
    email = forms.EmailField(label='请输入邮箱地址',min_length=4,widget=forms.EmailInput(attrs={'class':'input','placeholder':'邮箱'}))

class ModifyPwdForm(forms.Form):
    '''修改密码表单'''
    password = forms.CharField(label='输入新密码',min_length=6,widget=forms.PasswordInput(attrs={'class':'input','placeholder':'输入新密码'}))

class UserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ("email",)

class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = ("nike_name","desc","gexing","birthday","address","image",)



