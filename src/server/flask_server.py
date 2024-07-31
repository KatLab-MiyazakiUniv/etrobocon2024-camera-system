"""
走行体から画像ファイルを受信するWebサーバー.

@author Keiya121 CHIHAYATAKU
"""

import os
import socket
from flask import Flask, request, jsonify

app = Flask(__name__)

UPLOAD_FOLDER = 'datafiles'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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

    if file:
        fileName = file.filename
        # src/server/datafilesに、受信したファイルを保存する。
        filePath = os.path.join(UPLOAD_FOLDER, fileName)
        file.save(filePath)
        return jsonify({"message": "File uploaded successfully",
                        "filePath": filePath}), 200

print(os.uname()[1])
# ポート番号の設定
if __name__ == "__main__":
    ip = "127.0.0.1"
    host = os.uname()[1]
    if host == "KatLabLaptop":
        #参照 https://qiita.com/suzu12/items/b5c3d16aae55effb67c0
        connect_interface = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        connect_interface.connect(("8.8.8.8", 80))
        ip = connect_interface.getsockname()[0]
        connect_interface.close()
    app.run(host=ip, port=8000)
