"""競技システムインタフェース.

競技システムとの通信を行うクラス.
@author: YKhm20020
"""
import requests
# TODO: 詳細な画像処理を実装した後にimport追加
# from image_processing import ImageProcessing
from PIL import Image


class ResponseError(Exception):
    """レスポンスエラー用の例外."""

    def __init__(self, message: str):
        """コンストラクタ.

        Args:
            message (string): エラーメッセージ
        """
        super().__init__(message)


class OfficialInterface:
    """競技システムとの通信を行うクラス."""

    SERVER_IP = "192.168.100.1"    # 競技システムのIPアドレス
    TEAM_ID = 93                   # チームID

    @classmethod
    def upload_snap(cls, img_path: str) -> bool:
        """フィグ画像をアップロードする.

        Args:
            img_path (str): アップロードする画像のパス

        Returns:
            success (bool): 通信が成功したか(成功:true/失敗:false)
        """
        url = f"http://{cls.SERVER_IP}/snap"
        # リクエストヘッダー
        headers = {
            "Content-Type": "image/jpeg"
        }
        # リクエストパラメータ
        params = {
            "id": cls.TEAM_ID
        }

        try:
            # サイズが正しくない場合はリサイズする
            img = Image.open(img_path)
            width, height = img.size
            # if not (width == 640 and height == 480):
            #     ImageProcessing.resize_img(img_path, img_path, 640, 480)

            # bytes型で読み込み
            with open(img_path, "rb") as image_file:
                image_data = image_file.read()

            # APIにリクエストを送信
            response = requests.post(url, headers=headers,
                                     data=image_data, params=params)
            # レスポンスのステータスコードが201の場合、通信成功
            if response.status_code != 201:
                raise ResponseError("Failed to send fig image.")
            success = True
        except Exception as e:
            print(e)
            success = False
        return success


if __name__ == "__main__":
    print("test-start")
    OfficialInterface.upload_snap("../tests/testdata/img/Fig1/Fig1-1.jpeg")
    print("test-end")
