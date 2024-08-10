"""
走行体と通信するWebサーバー.

@author Keiya121 CHIHAYATAKU
"""

from src.csv_to_json import CSVToJSONConverter
import os
import socket
import platform

from flask import Flask, request, jsonify, send_file


app = Flask(__name__)


# '/images'へのPOSTリクエストに対する操作


@app.route('/images', methods=['POST'])
def getImage() -> jsonify:
    """走行体から、画像ファイルを取得するための関数."""
    # curlコマンドのエラーハンドリング
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    fileName = file.filename

    UPLOAD_FOLDER = 'image_data'
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # src/server/image_dataに、受信したファイルを保存する。
    filePath = os.path.join(UPLOAD_FOLDER, fileName)
    file.save(filePath)
    return jsonify({"message": "File uploaded successfully"}), 200

# '/run-log'へのPOSTリクエストに対する操作


@app.route('/run-log', methods=['POST'])
def getRunLog() -> jsonify:
    """走行体から、実行ログのcsvファイルを取得するための関数."""
    # curlコマンドのエラーハンドリング
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    fileName = file.filename

    UPLOAD_FOLDER = 'run_log_csv'
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # src/server/run_log_csvに、受信したファイルを保存する。
    filePath = os.path.join(UPLOAD_FOLDER, fileName)
    file.save(filePath)

    # CSVファイルをJSONに変換する
    converter = CSVToJSONConverter(filePath)
    converter.convert()

    return jsonify({"message": "File uploaded successfully"}), 200

# '/run-log'へのGETリクエストに対する操作


@app.route('/run-log', methods=['GET'])
def sendRunLog() -> jsonify:
    """Webアプリに実行ログのjsonファイルを送信するための関数."""

    STORAGE_FOLDER = 'run_log_json'

    # 保存されたファイルのリストを取得
    files = os.listdir(STORAGE_FOLDER)

    if not files:
        return jsonify({"error": "No files available"}), 404

    # 一旦最後のファイルを送信
    fileName = files[-1]
    filePath = os.path.join(STORAGE_FOLDER, fileName)

    return send_file(filePath, as_attachment=True), 200


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
