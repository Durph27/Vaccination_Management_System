from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, RegisterCandidateForm
from .models import User
from apps.candidates.models import Candidate


def login_view(request):
    if request.user.is_authenticated:
        return redirect('candidates:dashboard')

    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        if user:
            login(request, user)
            messages.success(request, f'Chào mừng, {user.get_full_name() or user.username}!')
            next_url = request.GET.get('next', '')
            # Prevent open redirect: only allow safe internal redirects
            if next_url and next_url.startswith('/') and not next_url.startswith('//'):
                return redirect(next_url)
            return redirect('candidates:dashboard')
        messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng.')
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Bạn đã đăng xuất.')
    return redirect('accounts:login')


def register_view(request):
    form = RegisterCandidateForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.role = User.ROLE_CANDIDATE
        user.save()
        # Create linked Candidate profile
        Candidate.objects.create(
            user=user,
            full_name=user.get_full_name(),
            phone=user.phone,
        )
        login(request, user)
        messages.success(request, 'Đăng ký thành công!')
        return redirect('candidates:dashboard')
    return render(request, 'accounts/register.html', {'form': form})

