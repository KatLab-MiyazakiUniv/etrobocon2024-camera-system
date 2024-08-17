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
        """コンストラクタ."""
        self.csv_file_path = csv_file_path
        self.json_file_path = self._get_json_file_path()

    def convert(self) -> None:
        """CSVファイルを読み込み、JSONファイルに変換する."""
        data = self._read_csv()
        self._write_json(data)

    def _read_csv(self) -> List[dict]:
        """CSVファイルを読み込み、辞書のリストを返す."""
        data = []
        with open(self.csv_file_path, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file, fieldnames=[
                'brightness', 'rightPWM', 'leftPWM', 'R', 'G', 'B'])
            for row in reader:
                data.append(row)
        return data

    def _write_json(self, data: List[dict]) -> None:
        """データをJSONファイルに書き込む."""
        json_data = {'runLog': data}

        # JSONファイルの保存先フォルダーを確認し、存在しない場合は作成
        os.makedirs(os.path.dirname(self.json_file_path), exist_ok=True)

        with open(self.json_file_path, mode='w',
                  encoding='utf-8') as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=4)

    def _get_json_file_path(self) -> str:
        """JSONファイルのパスを作成する."""
        base, _ = os.path.splitext(os.path.basename(self.csv_file_path))
        return os.path.join('src', 'server', 'run_log_json', base + '.json')
