# flaskサーバ
走行体や走行ログ確認用Webアプリと通信を行うflaskサーバプログラム。
server()は、"http://"サーバIPアドレス":8000/"にアクセスされたときに実行される。

## サーバの立て方

etrobocon2024-camera-system/ディレクトリ内で以下のコマンドを実行する。$から前は含まない。
```
<~etrobocon2024-camera-system>$ poetry run python3 -m src.server.flask_server
```
上のコマンドで実行出来ない場合は，次のコマンドを実行する。
```
<~etrobocon2024-camera-system>$ poetry run python -m src.server.flask_server
```

## データ送信
画像ファイルを送信する
```
$ curl -X POST -F "file=@"画像ファイルのパス"" http://サーバIPアドレス:8000/images
```

実行ログを送信する
```
$ curl -X POST -F "file=@"画像ファイルのパス"" http://サーバIPアドレス:8000/run-log
```