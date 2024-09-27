from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from ..models import CustomUser
from django.contrib.auth import authenticate

class CustomRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'school_name', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if 'ed.jp' not in email:
            raise forms.ValidationError('登録には「ed.jp」のメールアドレスが必要です。')
        return email

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label="Username or Email")

    def clean(self):
        username_or_email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        user = CustomUser.objects.filter(email=username_or_email).first()
        if user:
            # ここに入るということは，username_or_emailはemailだった
            username_or_email = user.username        
        print(username_or_email)
        print(password)
        self.user_cache = authenticate(self.request, username=username_or_email, password=password)
        if self.user_cache is None:            
            raise forms.ValidationError('Invalid username/email or password')

        return self.cleaned_data

