from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from ..models import CustomUser, School
from django.contrib.auth import authenticate

class CustomRegisterForm(UserCreationForm):
    school = forms.ModelChoiceField(
        queryset=School.objects.all(), 
        required=True, 
        label='学校名',
        widget=forms.Select(attrs={'id': 'id_school', 'class': 'form-control form-control-lg'})
        )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'school', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if 'ed.jp' not in email:
            raise forms.ValidationError('登録には教育機関のメールアドレスが必要です。')
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        # フォームのschoolフィールドから選択された学校を関連付け
        user.school = self.cleaned_data['school']
        if commit:
            user.save()
        return user

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label='ユーザー名またはメールアドレス')

