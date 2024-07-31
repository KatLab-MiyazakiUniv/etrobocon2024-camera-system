# flaskサーバ
走行体から画像ファイルを取得するflaskサーバプログラムです。
server()は、"http://"サーバIPアドレス":8000/"にアクセスされたときに実行されます。

## サーバの立て方
etrobocon2024-camera-system/src/server に移動します。
```
$ poetry run python3 flask_server.py
```

## データ送信
ファイルを送信する
```
$ curl -X POST -F "file=@"画像ファイルのパス"" http://"サーバIPアドレス":8000/upload
```