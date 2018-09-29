from django import forms
from captcha.fields import CaptchaField
from .models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=8)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


class ResetForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=8)
    password2 = forms.CharField(required=True, max_length=8)


class UploadForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class ModifyUserInfoForm(forms.ModelForm):
    class Meta:
        model= UserProfile
        fields = ['nick_name', 'birthday', 'gender', 'moblie', 'address']

