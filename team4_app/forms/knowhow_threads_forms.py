from django import forms
from ..models import ThreadComment


# コメントフォーム．1000文字までのコメントとS3のURLを受け付ける．
class CommentForm(forms.ModelForm):
    class Meta:
        model = ThreadComment
        fields = ['comment', 's3_url']
    