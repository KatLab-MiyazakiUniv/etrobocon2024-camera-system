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

# '/run-log'へのPOSTリクエストに対する操作


@app.route('/run-log', methods=['POST'])
def get_run_log() -> jsonify:
    """走行体から、実行ログのcsvファイルを取得するための関数."""
    # curlコマンドのエラーハンドリング
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    file_name = file.filename

    upload_folder = os.path.join(os.path.dirname(__file__), 'run_log_csv')
    os.makedirs(upload_folder, exist_ok=True)

    # src/server/run_log_csvに、受信したファイルを保存する。
    file_path = os.path.join(upload_folder, file_name)
    file.save(file_path)

    # CSVファイルをJSONに変換する
    converter = CSVToJSONConverter(file_path)
    converter.convert()

    return jsonify({"message": "File uploaded successfully"}), 200

# '/run-log'へのGETリクエストに対する操作


@app.route('/run-log', methods=['GET'])
def send_run_log() -> jsonify:
    """Webアプリに実行ログのjsonファイルを送信するための関数."""
    storage_folder = os.path.join(os.path.dirname(__file__), 'run_log_json')

    # 保存されたファイルのリストを取得
    files = os.listdir(storage_folder)

    if not files:
        return jsonify({"error": "No files available"}), 404

    # 一旦最後のファイルを送信
    file_name = files[-1]
    file_path = os.path.join(storage_folder, file_name)

    return send_file(file_path, as_attachment=True), 200


# ポート番号の設定
if __name__ == "__main__":
    ip = "127.0.0.1"

    if platform.system() == "Windows":
        host = platform.node()
    else:
        host = os.uname()[1]

    if host == "KatlabLaptop":
        # ソケットを作成し、GoogleのDNSサーバ("8.8.8.8:80")
        # に接続することで、IPアドレスを取得する。
        # 参考: https://qiita.com/suzu12/items/b5c3d16aae55effb67c0
        connect_interface = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        connect_interface.connect(("8.8.8.8", 80))
        ip = connect_interface.getsockname()[0]
        connect_interface.close()

    app.run(host=ip, port=8000)
