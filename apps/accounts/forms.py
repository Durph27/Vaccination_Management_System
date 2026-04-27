from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Tên đăng nhập',
        widget=forms.TextInput(attrs={'placeholder': 'Nhập tên đăng nhập', 'autofocus': True})
    )
    password = forms.CharField(
        label='Mật khẩu',
        widget=forms.PasswordInput(attrs={'placeholder': 'Nhập mật khẩu'})
    )


class RegisterCandidateForm(UserCreationForm):
    first_name = forms.CharField(label='Tên', max_length=50)
    last_name = forms.CharField(label='Họ', max_length=50)
    phone = forms.CharField(label='Số điện thoại', max_length=15)
    email = forms.EmailField(label='Email')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2']
