from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name='index'),  # ルートURLにアクセスした際に、views.indexが呼ばれる
]

