from django.contrib import admin
from django.apps import apps

# すべてのアプリケーションのモデルを取得
models = apps.get_models()

# 各モデルを管理画面に登録
for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        # 既に登録されている場合は無視
        pass