from django import forms

# コメントフォーム．1000文字までのコメントとS3のURLを受け付ける．
class CommentForm(forms.Form):
    comment = forms.CharField(label='コメント', max_length=1000)
    s3_url = forms.CharField(label='S3のURL', max_length=1000, required=False)
    