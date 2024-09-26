from django.urls import path
from .views import knowhow_views,  threads_views

urlpatterns = [
    # 新規登録・ログインのルーティングはここから

    # ノウハウのルーティングここから
    path('', knowhow_views.index, name='index'),  # knowhow

    # スレッドのルーティングここから
    path('', threads_views.index, name='index'),  # threads
]