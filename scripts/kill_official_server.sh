#!/bin/bash

# テスト用の競技システムのWebサーバをkillする
#  使用条件
#   - テスト用の競技システムが起動している
#   - テスト用の競技システムとLANケーブルで接続している

KILL_SERVER_COMMAND='ps aux | grep node | grep -v "grep" | awk '\''{print $2}'\'' | sudo xargs -r kill -9'
ssh taki@192.168.11.18 "$KILL_SERVER_COMMAND"
