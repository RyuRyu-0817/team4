from django.shortcuts import render
from .forms import UserRegisterForm
from django.contrib import messages
"""
新規登録・ログインのviewsを書くところ
"""


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=password)
            messages.success(request, 'ユーザ登録が完了しました。ログインしてください。')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'ログインに失敗しました。ユーザ名またはパスワードが間違っています。')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})
