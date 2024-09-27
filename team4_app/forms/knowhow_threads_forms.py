from django import forms
from ..models import ThreadComment, Thread, Category, KnowHow
from django.db import models

"""
ノウハウ部分
"""

class KnowhowCreateForm(forms.ModelForm):
    class Meta:
        model = KnowHow
        fields = ['title', 'discription', 'categories', 's3_url']  # 必要なフィールドを指定

    # カテゴリの選択を可能に
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(), 
        widget=forms.CheckboxSelectMultiple,
        label="カテゴリ"
    )
    
    # ファイルアップロード用のフィールド
    s3_url = forms.FileField(required=False, label="ファイルアップロード")

# コメントフォーム．1000文字までのコメントとS3のURLを受け付ける．
class KnowhowCommentCreateForm(forms.ModelForm):
    class Meta:
        model = ThreadComment
        fields = ['comment', 's3_url']

"""
スレッド部分
"""

# この線で合ってる気もするんで一応これ残しておきたいんですけど，viewを変更したんで，一回下のmodelformでやってみますね
# いけたっす！！！また共有しますね！
# Formで作ってみた盤(?)　了解っす！はーい！
# class ThreadForm(forms.Form):
#     title = models.CharField(max_length=100, verbose_name='タイトル')
#     discription = models.TextField(verbose_name='説明')
#     # カテゴリの選択を可能に
#     categories = forms.ModelMultipleChoiceField(
#         queryset=Category.objects.all(), 
#         widget=forms.CheckboxSelectMultiple,
#         label="カテゴリ"
#     )
    
#     # ファイルアップロード用のフィールド
#     s3_url = forms.FileField(required=False, label="ファイルアップロード")

class ThreadCreateForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title', 'discription', 'categories', 's3_url']  # 必要なフィールドを指定

    # カテゴリの選択を可能に
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(), 
        widget=forms.CheckboxSelectMultiple,
        label="カテゴリ"
    )
    
    # ファイルアップロード用のフィールド
    s3_url = forms.FileField(required=False, label="ファイルアップロード")

# コメントフォーム．1000文字までのコメントとS3のURLを受け付ける．
class ThreadCommentCreateForm(forms.ModelForm):
    class Meta:
        model = ThreadComment
        fields = ['comment', 's3_url']

