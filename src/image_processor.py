"""
画像処理に関するクラス.

@author bizyutyu
"""

import cv2
import numpy as np
import os


class ImageProcessor:
    """CSVファイルをJSONファイルに変換するクラス."""

    @staticmethod
    def sharpen_image(image_path: str) -> str:
        """画像の先鋭化処理を行うメソッド.

        手法：カラー画像のアンシャープマスクを用いる

        Args:
            image_path(str): 先鋭化対象の画像パス
        Return:
            sharpened_image_path: 先鋭化後画像パス

        Raises:
            FileNotFoundError: 画像が見つからない場合に発生
        """
        try:
            # 読み込み
            img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

            if img is None:
                raise FileNotFoundError(f"'{image_path}' is not found")

            # アンシャープマスクを適用する
            blurred = cv2.GaussianBlur(img, (0, 0), 2)  # ぼかし処理

            # 引数: 元画像, 元の画像に対する加重係数（強度）
            # ブラー画像, ブラー画像に対する減重係数(強度), 画像の明るさ(0は無視)
            result = cv2.addWeighted(img, 2.5, blurred, -1.5, 0)  # 差分から鮮明化

            # 出力パスの生成
            dir_path = os.path.dirname(image_path)
            file_name = os.path.basename(image_path)
            output_path = os.path.join(dir_path, f"Sharpened_{file_name}")

            # 先鋭化画像保存処理
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            cv2.imwrite(output_path, result)

            return output_path

        except FileNotFoundError as e:
            print("Error:", e)
            return None

# if __name__ == '__main__':

# import argparse

#     parser = argparse.ArgumentParser(description="画像処理に関するプログラム")

#     parser.add_argument("-ipath", "--image_path", type=str,
#                   default=IMAGE_DIR_PATH/'test_image.jpeg', help='入力画像')

#     args = parser.parse_args()

#     sharpened_image = ImageProcessor.sharpen_image(args.input_path)

#     if sharpened_image:
#         print(f"先鋭化完了。結果は {output_path} に保存しています。")
#     else:
#         print("先鋭化失敗。")
