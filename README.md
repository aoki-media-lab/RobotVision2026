# Robot Vision 2026

## 授業の構成

| 週 | 内容 | 資料 |
| --- | --- | --- |
| 第1週 | Python と OpenCV の基礎 (演習) | [first/](first/README.md) |
| 第2週 | カメラの映像を処理する (演習) | [second/](second/README.md) |
| 第3・4週 | CV の主要テーマを班で調査・実装し，発表する | [themes/](themes/README.md) |
| 第5・6週 | 第3・4週のテーマを活用し，Webカメラを使ったアプリを班で制作・発表する | [project/](project/README.md) |

- ChatGPT や Gemini などの生成AI の利用は認める．ただし発表の質疑では，使った技術の原理と，
  うまくいかない理由を自分の言葉で説明できることを求める
- 実験環境のPCでは GPU が使えない．すべて CPU のみで動作させること

### 講義スライド
- 第1週スライド (後日公開)
- 第2週スライド (後日公開)
- 調査テーマ・最終発表の説明スライド (後日公開)

## ソースコードのダウンロード
コマンドプロンプト(Power Shell，ターミナル)上で以下のコマンドを実行し，ソースコードをダウンロードできる．
Windowsの場合，ダウンロードしたファイルは `C:\Users\E(ユーザ名)\RobotVision2026` に保存される．
```shell
git clone https://github.com/aoki-media-lab/RobotVision2026.git
```

## 環境構築
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
   授業で共通して使う部品 (`common/`) もこのときにインストールされ，どのフォルダからでも
   `from common import run` で使えるようになる．
```shell
cd RobotVision2026
uv sync
```
3. プログラムは `uv run python` を付けて実行する．
```shell
# 例: first/python_basics/01_variables.py を実行する場合
cd first/python_basics
uv run python 01_variables.py

# カメラを使うプログラムは，動画ファイルでも実行できる
cd second
uv run python 08_optical_flow.py --video image_data/opticalflow.avi
```

## ディレクトリ構成

```
RobotVision2026/
├── common/        授業で共通して使う部品 (カメラのループ，FPS表示，録画，トラックバー)
├── first/         第1週: Python の基礎 (python_basics/)，OpenCV の基礎 (opencv/)
├── second/        第2週: 色・ラベリング・背景差分・オプティカルフロー
├── themes/        第3・4週: 調査テーマのカード，参考資料 (reference/)
└── project/       第5・6週: アプリ制作のルール
```

## FAQ
- Q. プログラム実行時にエラーが発生する
  - A1. 必要なパッケージがインストールされていない可能性がある．
  RobotVision2026 のディレクトリで `uv sync` を実行し，パッケージをインストールする．
  - A2. `ModuleNotFoundError: No module named 'common'` と出る場合も，`uv sync` を実行する．
  - A3. 演習のファイルで `AssertionError: 課題◯ がまだ未記入` と出るのは正常．メッセージの課題を解く．
- Q. カメラが開けない / 別のカメラが開く
  - A. `--camera 1` のようにカメラの番号を指定する．
- Q. (Windows) カメラの起動が遅い
  - A. `common.run` を使うプログラムでは自動で対策している．
  自分で `cv2.VideoCapture(0)` を書く場合は，`cv2.VideoCapture(0, cv2.CAP_DSHOW)` に書き換える．
