# Robot Vision 2026

### 講義スライド
- 1週目スライド (後日公開)
- 2週目スライド (後日公開)
- 3週目スライド (後日公開)

### 講義で使うソースコードのダウンロード
コマンドプロンプト(Power Shell，ターミナル)上で以下のコマンドを実行し，ソースコードをダウンロードできる．
Windowsの場合，ダウンロードしたファイルは `C:\Users\E(ユーザ名)\RobotVision2026` に保存される．
```shell
git clone https://github.com/aoki-media-lab/RobotVision2026.git
```

### 環境構築
パッケージ管理には [uv](https://docs.astral.sh/uv/) を使う．
Python 本体(3.12.10)も uv が自動でダウンロードするため，別途インストールする必要はない．

1. uv をインストールする．
```shell
# Windows (Power Shell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```
2. ダウンロードしたディレクトリに移動し，必要なパッケージをインストールする．
```shell
cd RobotVision2026
uv sync
```
3. プログラムは `uv run` を付けて実行する．
```shell
# 例: first/show_image.py を実行する場合
cd first
uv run python show_image.py
# Jupyter Lab を起動する場合
uv run jupyter lab
```

### faq
- Q. プログラム実行時にエラーが発生する
  - A1. 必要なパッケージがインストールされていない可能性がある．
  RobotVision2026 のディレクトリで `uv sync` を実行し，パッケージをインストールする．
  - A2. (自身のPCを使用している場合)ファイルが存在するディレクトリでプログラムを実行する必要がある．
    例えば，first/show_image.pyを実行する場合，firstディレクトリで `uv run python show_image.py` を実行する．
- Q. (Windows) カメラの起動が遅い
  - A. PCによっては `cap = cv2.VideoCapture()` 実行に時間を要する．
  `VideoCapture` の引数に `cv2.CAP_DSHOW` を追加することで解決することができる．
  ソースコード内の `cv2.VideoCapture(0)` を `cv2.VideoCapture(0, cv2.CAP_DSHOW)` に書き換える．
