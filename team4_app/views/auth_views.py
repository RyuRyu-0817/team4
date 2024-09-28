from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from ..forms.auth_forms import CustomRegisterForm, CustomLoginForm
from ..models import CustomUser

"""
新規登録・ログインのviewsを書くところ
"""


def register_view(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()            
            login(request, user, backend='team4_app.backend.CustomUserBackend')
            return redirect('home')

        else:            
            return render(request, 'register.html', {'form': form})
    else:        
        form = CustomRegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home') 
    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})

# def login_view(request):
#     if request.method == 'POST':
#         form = CustomLoginForm(request, data=request.POST)
#         if form.is_valid():
#             username_or_email = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')

#             # ユーザー名またはメールアドレスでログイン
#             user = authenticate(request, username=username_or_email, password=password)
#             if user is None:
#                 # メールアドレスとして認識する
#                 try:
#                     email_user = CustomUser.objects.get(email=username_or_email)
#                     user = authenticate(request, username=email_user.username, password=password)
#                 except CustomUser.DoesNotExist:
#                     user = None

#             if user is not None:                
#                 login(request, user)
#                 return redirect('home')
#         else:
#             print(form.errors)            
#             return render(request, 'login.html', {'form': form})

#     else:
#         form = CustomLoginForm()
    
#     return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/login')
