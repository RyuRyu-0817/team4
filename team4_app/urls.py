from django.urls import path
from .views import auth_views, home_views, knowhow_views, threads_views, profile_views

urlpatterns = [
    # 新規登録・ログインのルーティングはここから
    path('register/', auth_views.register_view, name='register'),
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),

    # ユーザープロフィールページはここから
    path('profile/<int:id>/', profile_views.profile_view, name='user_profile'),
    
    # ホームのルーティングはここから
    path('home/', home_views.index, name='home'),  # home
    
    # ノウハウのルーティングここから
    path('knowhow/', knowhow_views.index, name='knowhow_index'),  # knowhow
    path('knowhow/<int:id>/', knowhow_views.detail, name='knowhow_detail'),
    path('knowhow/create/', knowhow_views.create, name='knowhow_create'),
    path('like_knowhow/', knowhow_views.like_knowhow, name='like_knowhow'),
    path('category/<int:id>', knowhow_views.categories, name='knowhow_category'),

    # スレッドのルーティングここから
    path('thread/', threads_views.index, name='threads_index'),  # threads
    path('thread/<int:id>/', threads_views.detail, name='threads_detail'),
    path('thread/create/', threads_views.create, name='threads_create'),
    path('like_thread/', threads_views.like_thread, name='like_thread'),
]
