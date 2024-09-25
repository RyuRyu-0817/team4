仮想環境を構築
```
python -m venv venv
```

仮想環境を有効化(windowsの人違うかも)
```
source venv/bin/activate
```

pipで必要なパッケージインストール(requirements.txt)に書いてます
```
pip install -r < requirements.txt
```

manage.pyがある階層に入って以下を実行するとローカルでサーバ立ち上がります
```
python manage.py runserver
```