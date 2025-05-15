# Pythonの公式イメージをベースとして使用
FROM python:3.9-slim

# 作業ディレクトリを設定
WORKDIR /app

# 依存関係ファイルをコピーし、インストール
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY . .

# Cloud Runがリッスンするポート (環境変数 PORT で指定される。デフォルト8080)
# EXPOSE命令はドキュメンテーション目的であり、実際にポートを開くのはCMD/ENTRYPOINT
# Cloud Runではコンテナが $PORT 環境変数の値でリッスンすることを期待
# gunicorn はデフォルトで8000番ポートを使用するため、ここで $PORT を指定

# コンテナ起動時に実行するコマンド
# gunicornを使用してFlaskアプリケーションを起動
# 0.0.0.0 は全てのネットワークインターフェースでリッスン
# ${PORT} はCloud Runによって提供される環境変数 (ローカルテストでは8080を想定)
CMD exec gunicorn --bind 0.0.0.0:${PORT} --workers 1 --threads 8 --timeout 0 app:app