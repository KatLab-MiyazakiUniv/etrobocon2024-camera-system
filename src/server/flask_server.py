"""
走行体から画像ファイルを受信するWebサーバー.

@author Keiya121 CHIHAYATAKU KakinokiKanta
"""

from flask import Flask, request, jsonify
import os
import sys
import socket
import platform

# 実行ファイルより上位ディレクトリのファイルを相対インポートできないため
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from official_interface import OfficialInterface # noqa


app = Flask(__name__)

UPLOAD_FOLDER = 'datafiles'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# サーバ起動確認用


@app.route('/', methods=['GET'])
def healthCheck() -> jsonify:
    """サーバ起動確認のための関数."""
    return jsonify({"message": "I'm healty!"}), 200


# '/upload'へのPOSTリクエストに対する操作
@app.route('/upload', methods=['POST'])
def getImageFile() -> jsonify:
    """走行体から、画像ファイルを取得するための関数."""
    # curlコマンドのエラーハンドリング
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    fileName = file.filename
    # src/server/datafilesに、受信したファイルを保存する。
    filePath = os.path.join(UPLOAD_FOLDER, fileName)
    file.save(filePath)

    # TODO: 現在は、1枚目のフィグ画像、プラレール画像の場合に競技システムへアップロードしている
    if fileName == 'Fig_1.jpeg' or fileName == 'Pla.jpeg':
        OfficialInterface.upload_snap(filePath)

    return jsonify({"message": "File uploaded successfully",
                    "filePath": filePath}), 200


# ポート番号の設定
if __name__ == "__main__":
    ip = "127.0.0.1"

    if platform.system() == "Windows":
        host = platform.node()
    else:
        host = os.uname()[1]

    if host == "KatLabLaptop":
        # ソケットを作成し、GoogleのDNSサーバ("8.8.8.8:80")
        # に接続することで、IPアドレスを取得する。
        # 参考: https://qiita.com/suzu12/items/b5c3d16aae55effb67c0
        connect_interface = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        connect_interface.connect(("8.8.8.8", 80))
        ip = connect_interface.getsockname()[0]
        connect_interface.close()

    app.run(host=ip, port=8000)
