"""カメラ(または動画ファイル)から画像を読み込み，処理して表示する

    import sys
    from pathlib import Path

    sys.path.append(str(Path(__file__).resolve().parents[1]))

    from common import run

    def process(frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if __name__ == "__main__":
        run(process)

実行時のオプション:
    uv run xxx.py                     # Webカメラ(0番)で実行
    uv run xxx.py --camera 1          # 1番のカメラを使う
    uv run xxx.py --video foo.mp4     # 動画ファイルで実行

q キーで終了する．q 以外のキーは run(process, on_key=関数) で受け取れる．
このファイルを直接実行すると，カメラの映像をそのまま表示する．
    uv run common/camera.py
"""

import argparse
import sys

import cv2


def open_capture(source):
    """カメラ番号(int)または動画ファイルのパス(str)から VideoCapture を作る"""
    if isinstance(source, int) and sys.platform.startswith("win"):
        # Windows では CAP_DSHOW を指定しないとカメラの起動が遅いことがある
        cap = cv2.VideoCapture(source, cv2.CAP_DSHOW)
    else:
        cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        raise RuntimeError(f"カメラ/動画を開けなかった: {source}")
    return cap


def run(process=lambda frame: frame, window="output", on_key=None):
    """カメラ(または動画)から1フレームずつ読み込み，process に渡して結果を表示する

    process(frame) の戻り値は次のどちらか:
      - 画像1枚                          : window という名前のウィンドウに表示する
      - {"ウィンドウ名": 画像, ...} の辞書 : 複数のウィンドウに表示する

    Args:
        process: BGR画像を1枚受け取り，画像(または画像の辞書)を返す関数．省略すると何もしない
        window: 結果を表示するウィンドウ名
        on_key: q 以外のキーが押されたときに呼ばれる関数．押されたキーを1文字の文字列で受け取る
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--camera", type=int, default=0, help="使うカメラの番号")
    parser.add_argument("--video", type=str, default=None, help="カメラの代わりに使う動画ファイル")
    args, _ = parser.parse_known_args()

    source = args.video if args.video is not None else args.camera
    cap = open_capture(source)

    # 動画ファイルは元の速さで再生する
    delay = 1
    if args.video is not None:
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps > 0:
            delay = max(1, int(1000 / fps))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        result = process(frame)
        if isinstance(result, dict):
            for name, img in result.items():
                cv2.imshow(name, img)
        else:
            cv2.imshow(window, result)

        k = cv2.waitKey(delay) & 0xFF
        if k == ord("q"):
            break
        if k != 255 and on_key is not None:  # 255 はキーが押されなかったとき
            on_key(chr(k))

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run()
