from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, school_name, password=None):
        if not email:
            raise ValueError('Email address is required')
        if not username:
            raise ValueError('Username is required')
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            school_name=school_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, username, email, school_name, password=None):
        user = self.create_user(
            username=username,
            email=email,
            school_name=school_name,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    
class School(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='学校名')

    def __str__(self):
        return self.name
    
class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='学校名')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'  # Emailでログイン
    REQUIRED_FIELDS = ['username', 'school_name']
    # def __str__(self):
    #     return self.email
    def has_perm(self, perm, obj=None):
        return True
    def has_module_perms(self, app_label):
        return True
    @property
    def is_staff(self):
        return self.is_admin


class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True, verbose_name='カテゴリ名')

    def __str__(self):
        return self.category_name


class KnowHow(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='投稿者ID')
    categories = models.ManyToManyField('Category', related_name='knowhow', verbose_name='カテゴリID')
    title = models.CharField(max_length=100, verbose_name='タイトル')
    discription = models.TextField(verbose_name='説明')    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='投稿日時')
    s3_url = models.CharField(max_length=1000, verbose_name='S3のURL', blank=True)

    def __str__(self):
        return self.title

class KnowHowLike(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='ユーザー')
    knowhow = models.ForeignKey(KnowHow, on_delete=models.CASCADE, verbose_name='ノウハウ')

    def __str__(self):
        return f"{self.user.username} liked {self.knowhow.title}" 

class KnowHowComment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='投稿者ID')
    knowhow = models.ForeignKey('KnowHow', on_delete=models.CASCADE, verbose_name='ノウハウID')
    comment = models.TextField(verbose_name='コメント')     # text    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='投稿日時')
    s3_url = models.CharField(max_length=1000, verbose_name='S3のURL', blank=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.knowhow.title}"     


class Thread(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='投稿者ID')
    categories = models.ManyToManyField('Category', related_name='thread', verbose_name='カテゴリID')
    title = models.CharField(max_length=100, verbose_name='タイトル')
    discription = models.TextField(verbose_name='説明')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='投稿日時')
    s3_url = models.CharField(max_length=1000, verbose_name='S3のURL', blank=True)

    def __str__(self):
        return self.title

# ThreadLikeモデル
class ThreadLike(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='ユーザー')
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, verbose_name='スレッド')

    def __str__(self):
        return f"{self.user.username} liked {self.thread.title}"  # ユーザーといいねされたスレッドを表示


class ThreadComment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='投稿者ID')
    thread_id = models.ForeignKey('Thread', on_delete=models.CASCADE, verbose_name='スレッドID')
    comment = models.TextField(verbose_name='コメント')
    num_favorites = models.IntegerField(default=0, verbose_name='いいね数')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='投稿日時')
    s3_url = models.CharField(max_length=1000, verbose_name='S3のURL', blank=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.thread_id.title}"  # コメントの投稿者とノウハウを表示

