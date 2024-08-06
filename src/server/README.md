# flaskサーバ
走行体から画像ファイルを取得するflaskサーバプログラムです。
server()は、"http://"サーバIPアドレス":8000/"にアクセスされたときに実行されます。

## サーバの立て方

etrobocon2024-camera-system/ディレクトリ内で以下のコマンドを実行する。$から前は含まない。
```
<~etrobocon2024-camera-system>$ poetry run python3 src/server/flask_server.py
```
上のコマンドで実行出来ない場合は，次のコマンドを実行する
```
<~etrobocon2024-camera-system>$ poetry run python src/server/flask_server.py
```

## データ送信
ファイルを送信する
```
$ curl -X POST -F "file=@"画像ファイルのパス"" http://"サーバIPアドレス":8000/upload
```