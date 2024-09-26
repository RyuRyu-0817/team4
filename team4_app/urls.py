from django.urls import path
from .views import auth_views, home_views, knowhow_views, threads_views

urlpatterns = [
    # 新規登録・ログインのルーティングはここから
    path('register/', auth_views.register_view, name='register'),
    path('login/', auth_views.login_view, name='login'),
    
    # ホームのルーティングはここから
    path('home/', home_views.index, name='home'),  # home
    
    # ノウハウのルーティングここから
    path('knowhow/', knowhow_views.index, name='knowhow_index'),  # knowhow
    # path('knowhow/<int:id>/', knowhow_views.???)
    # path('knowhow/create/', knowhow_views.???)

    # スレッドのルーティングここから
    path('thread/', threads_views.index, name='threads_index'),  # threads
    path('thread/<int:id>/', threads_views.detail, name='threads_detail'),
    path('thread/create/', threads_views.create, name='threads_create')
]
