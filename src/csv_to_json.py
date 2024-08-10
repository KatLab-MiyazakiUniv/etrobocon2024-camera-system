"""
CSVファイルをJSONファイルに変換するクラス.

@author Keiya121
"""

import csv
import json
import os
from typing import List


class CSVToJSONConverter:
    def __init__(self, csv_file_path: str) -> None:
        self.csv_file_path = csv_file_path
        self.json_file_path = self._get_json_file_path()

    def convert(self) -> None:
        data = self._read_csv()
        self._write_json(data)

    def _read_csv(self) -> List[dict]:
        data = []
        with open(self.csv_file_path, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file, fieldnames=[
                                    'brightness', 'rightPWM', 'leftPWM', 'R', 'G', 'B'])
            for row in reader:
                data.append(row)
        return data

    def _write_json(self, data: List[dict]) -> None:
        # 'runLog' キーでデータを囲む
        json_data = {'runLog': data}
        with open(self.json_file_path, mode='w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=4)

    def _get_json_file_path(self) -> str:
        # JSONファイルの保存先フォルダーを設定
        base, _ = os.path.splitext(os.path.basename(self.csv_file_path))
        return os.path.join('run_log_json', base + '.json')