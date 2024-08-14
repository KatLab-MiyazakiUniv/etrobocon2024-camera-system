help:
	@echo "カメラシステムを実行する"
	@echo " $$ make run"
	@echo "Pytestを実行する"
	@echo " $$ make test"
	@echo "全てのソースコードをフォーマットする"
	@echo " $$ make format"
	@echo "全てのソースコードのスタイルをチェックする"
	@echo " $$ make check_style"
	@echo "カバレッジレポートの表示"
	@echo " $$ make coverage"
	@echo "サーバの立ち上げ"
	@echo " $$ make server"
	@echo "実行ログディレクトリ内の全てのファイルを削除する"
	@echo " $$ make clean"

run:
	poetry run python src

test:
	poetry run pytest

format:
	poetry run python -m autopep8 -i -r src/ tests/

check_style:
	poetry run python -m pycodestyle src/ tests/
	poetry run python -m pydocstyle src/ tests/

coverage:
	poetry run coverage run -m pytest
	poetry run coverage report

server:
	poetry run python -m src.server.flask_server

clean:
	rm -rf src/server/run_log_csv/*
	rm -rf src/server/run_log_json/*
