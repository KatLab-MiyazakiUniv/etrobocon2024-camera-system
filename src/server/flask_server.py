"""
走行体と通信するWebサーバー.

@author Keiya121 CHIHAYATAKU KakinokiKanta takahashitom
"""

import os
import socket
import platform
from flask_cors import CORS
from ..csv_to_json import CSVToJSONConverter
from ..official_interface import OfficialInterface
from ..detect_object import DetectObject
from ..image_processor import ImageProcessor

from flask import Flask, request, jsonify, send_file

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'datafiles'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# サーバ起動確認用


@app.route('/', methods=['GET'])
def health_check() -> jsonify:
    """サーバ起動確認のための関数.

    Return:
        jsonify (string, int):
        レスポンスメッセージ,ステータスコード
    """
    return jsonify({"message": "I'm healty!"}), 200


# '/images'へのPOSTリクエストに対する操作


@app.route('/images', methods=['POST'])
def get_image() -> jsonify:
    """走行体から、画像ファイルを取得するための関数.

    Return:
            jsonify (string, int): レスポンスメッセージ,ステータスコード
    """
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

    # 画像の先鋭化処理を行う
    sharpened_file_path = ImageProcessor.sharpen_image(file_path)

    if sharpened_file_path:
        # 先鋭化した画像ファイルを競技システムに送信する
        OfficialInterface.upload_snap(sharpened_file_path)
        return jsonify({"message":
                        "Sharpened File uploaded successfully"}), 200
    else:
        # 受け取った画像ファイルを競技システムに送信する
        OfficialInterface.upload_snap(file_path)
        return jsonify({"message": "File uploaded successfully"}), 200

# '/detect'へのPOSTリクエストに対する操作


@app.route('/detect', methods=['POST'])
def get_detection_image() -> jsonify:
    """走行体から画像ファイルを取得し、物体検出した結果を送信するための関数.

    Return:
            jsonify (string, int): レスポンスメッセージ,ステータスコード
    """
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

        # 判定したふぃぐの向きがが正面だった場合、競技システムに送信する
        if cls == 0:
            # 画像の先鋭化処理を行う
            sharpened_file_path = ImageProcessor.sharpen_image(file_path)

            if sharpened_file_path:
                # 先鋭化したふぃぐ画像を競技システムに送信する
                OfficialInterface.upload_snap(sharpened_file_path)
            else:
                # ふぃぐ画像をそのまま競技システムに送信する
                OfficialInterface.upload_snap(file_path)

        return send_file(empty_file,
                         as_attachment=True,
                         download_name=empty_file,
                         mimetype='text/plain'), 200
    except Exception:
        print("Error: detect failed")
        objects = []
        cls = -1
        empty_file = os.path.abspath(f"{cls}_skip_camera_action.flag")

        # 空のフラグ管理用ファイルを作成
        with open(empty_file, 'w') as file:
            pass

        OfficialInterface.upload_snap(file_path)

        return send_file(empty_file,
                         as_attachment=True,
                         download_name=empty_file,
                         mimetype='text/plain'), 200

# '/run-log'へのPOSTリクエストに対する操作


@app.route('/run-log', methods=['POST'])
def get_run_log() -> jsonify:
    """走行体から、実行ログのcsvファイルを取得するための関数.

    Return:
            jsonify (string, int): レスポンスメッセージ,ステータスコード
    """
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
    """Webアプリに実行ログのjsonファイルを送信するための関数.

    Return:
            jsonify (string, int): レスポンスメッセージ,ステータスコード
    """
    # jsonファイルを指定するための変数
    latest = request.args.get('latest')

    # リクエストにクエリパラメータが存在しない場合
    if latest is None:
        return jsonify({"error": "Query parameter 'latest' is required"}), 400

    # クエリパラメータが整数かどうかの判定
    try:
        latest = int(latest)
    except ValueError:
        return jsonify({"error":
                        "Query parameter 'latest' must be an integer"}), 400

    # jsonファイルが保存されているディレクトリを指定
    storage_folder = os.path.join(os.path.dirname(__file__), 'run_log_json')

    # jsonファイルのリストを取得
    files = os.listdir(storage_folder)

    # jsonファイルが存在するかをチェック
    if not files:
        return jsonify({"error": "No files available"}), 404

    # クエリパラメータの指定したファイルが存在しない場合
    if latest == 0 or latest > len(files):
        return jsonify({"error": "'latest' is out of range"}), 404

    # 最後のファイルを送信
    file_name = files[-latest]
    file_path = os.path.join(storage_folder, file_name)

    return send_file(file_path, as_attachment=True), 200


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

    app.run(host=ip, port=8000, threaded=True)
