from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True, verbose_name='カテゴリ名')


class KnowHow(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='投稿者ID')
    categories = models.ManyToManyField('Category', related_name='knowhow', verbose_name='カテゴリID')
    title = models.CharField(max_length=100, verbose_name='タイトル')
    discription = models.TextField(verbose_name='説明')
    num_favorites = models.IntegerField(default=0, verbose_name='いいね数')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='投稿日時')
    s3_url = models.CharField(max_length=1000, verbose_name='S3のURL', blank=True)


class KnowHowComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='投稿者ID')
    knowhow = models.ForeignKey('KnowHow', on_delete=models.CASCADE, verbose_name='ノウハウID')
    comment = models.TextField(verbose_name='コメント')     # text
    num_favorites = models.IntegerField(default=0, verbose_name='いいね数')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='投稿日時')
    s3_url = models.CharField(max_length=1000, verbose_name='S3のURL', blank=True)


class Thread(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='投稿者ID')
    categories = models.ManyToManyField('Category', related_name='thread', verbose_name='カテゴリID')
    title = models.CharField(max_length=100, verbose_name='タイトル')
    discription = models.TextField(verbose_name='説明')
    num_favorites = models.IntegerField(default=0, verbose_name='いいね数')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='投稿日時')
    s3_url = models.CharField(max_length=1000, verbose_name='S3のURL', blank=True)


class ThreadComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='投稿者ID')
    thread_id = models.ForeignKey('Thread', on_delete=models.CASCADE, verbose_name='スレッドID')
    comment = models.TextField(verbose_name='コメント')
    num_favorites = models.IntegerField(default=0, verbose_name='いいね数')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='投稿日時')
    s3_url = models.CharField(max_length=1000, verbose_name='S3のURL', blank=True)

