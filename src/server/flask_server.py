"""
走行体から画像ファイルを受信するWebサーバー.

@author Keiya121 CHIHAYATAKU takahashitom
"""

import os
import socket
import platform
from ..detect_object import DetectObject

from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

UPLOAD_FOLDER = 'datafiles'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# '/upload'へのPOSTリクエストに対する操作


@app.route('/images', methods=['POST'])
def get_image() -> jsonify:
    """走行体から、画像ファイルを取得するための関数."""
    # curlコマンドのエラーハンドリング
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    file_name = file.filename

    upload_folder = os.path.join(os.path.dirname(__file__), 'image_data')
    os.makedirs(upload_folder, exist_ok=True)

    # src/server/image_dataに、受信したファイルを保存する。
    file_path = os.path.join(upload_folder, file_name)
    file.save(file_path)

    return jsonify({"message": "File uploaded successfully"}), 200

# '/detect'へのPOSTリクエストに対する操作


@app.route('/detect', methods=['POST'])
def get_detection_image() -> jsonify:
    """走行体から画像ファイルを取得し、物体検出した結果を送信するための関数."""
    # curlコマンドのエラーハンドリング
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    file_name = file.filename

    upload_folder = os.path.join(os.path.dirname(__file__), 'image_data')
    os.makedirs(upload_folder, exist_ok=True)

    # src/server/image_dataに、受信したファイルを保存する
    file_path = os.path.join(upload_folder, file_name)
    file.save(file_path)

    # 取得した画像に対し物体検出を行う
    d = DetectObject()
    detected_img_path = os.path.join(upload_folder, "detected_"+file_name)

    try:
        objects = d.detect_object(img_path=file_path,
                                  save_path=detected_img_path)
        print(objects)

        cls = int(objects[0][5])
        empty_file = os.path.abspath(f"{cls}_skip_camera_action.flag")

        # 空のフラグ管理用ファイルを作成
        with open(empty_file, 'w') as file:
            pass

        return send_file(empty_file,
                         as_attachment=True,
                         download_name=empty_file,
                         mimetype='text/plain'), 200
    except Exception:
        print("Error: detect failed")
        objects = []
        return jsonify({"message": "File uploaded successfully",
                        "detect_results": "detect failed"}), 200


# ポート番号の設定
if __name__ == "__main__":
    ip = "127.0.0.1"

    if platform.system() == "Windows":
        host = platform.node()
    else:
        host = os.uname()[1]

    # if host == "KatLabLaptop":
    if host == "LAPTOP-UNI0BH6G":
        # ソケットを作成し、GoogleのDNSサーバ("8.8.8.8:80")
        # に接続することで、IPアドレスを取得する。
        # 参考: https://qiita.com/suzu12/items/b5c3d16aae55effb67c0
        connect_interface = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        connect_interface.connect(("8.8.8.8", 80))
        ip = connect_interface.getsockname()[0]
        connect_interface.close()

    app.run(host=ip, port=8000)
