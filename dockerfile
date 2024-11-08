# Pythonイメージを使用
FROM python:3.9-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なファイルをコピー
COPY . /app

# パッケージのインストール
RUN pip install --no-cache-dir -r requirements.txt

# ボットを起動
CMD ["python3", "main.py"]
