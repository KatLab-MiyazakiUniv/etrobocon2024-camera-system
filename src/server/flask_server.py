'''ロボットの走行情報を提供するWebサーバ.

 @author  desty505 aridome222 miyashita64
'''
import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>aaaaaa</h1>'

# ポート番号の設定
if __name__ == "__main__":
    ip = "127.0.0.1"
    host = os.uname()[1]
    if host == "KatLabLaptop":
        ip = ""
    app.run(host=ip, port=8000)
