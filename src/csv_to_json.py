"""
CSVファイルをJSONファイルに変換するクラス.

@author Keiya121
"""

import csv
import json
import os
from typing import List


class CSVToJSONConverter:
    """CSVファイルをJSONファイルに変換するクラス."""

    def __init__(self, csv_file_path: str) -> None:
        """コンストラクタ.

        Args:
            csv_file_path (str): CSVファイルのパス
        """
        self.csv_file_path = csv_file_path
        self.json_file_path = self._get_json_file_path()

    def convert(self) -> None:
        """CSVファイルを読み込み、JSONファイルに変換する."""
        data = self._read_csv()
        self._write_json(data)

    def _read_csv(self) -> List[dict]:
        """CSVファイルを読み込み、辞書のリストを返す.

        Return:
              run_log_data (List[dict]): 走行ログデータ
        """
        run_log_data = []
        with open(self.csv_file_path, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file, fieldnames=[
                'brightness', 'rightPWM', 'leftPWM', 'R', 'G', 'B'])
            for row in reader:
                run_log_data.append(row)
        return run_log_data

    def _write_json(self, run_log_data: List[dict]) -> None:
        """データをJSONファイルに書き込む.

        Args:
            run_log_data (List[dict]): 走行ログデータ
        """
        json_data = {'runLog': run_log_data}

        # JSONファイルの保存先フォルダーを確認し、存在しない場合は作成
        os.makedirs(os.path.dirname(self.json_file_path), exist_ok=True)

        with open(self.json_file_path, mode='w',
                  encoding='utf-8') as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=4)

    def _get_json_file_path(self) -> str:
        """JSONファイルのパスを作成する.

        Return:
              json_file_path (str): jsonファイルのパス
        """
        base, _ = os.path.splitext(os.path.basename(self.csv_file_path))
        json_file_path = os.path.join(
            'src', 'server', 'run_log_json', base + '.json')
        return json_file_path
