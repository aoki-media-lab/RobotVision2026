"""カメラ(または動画ファイル)のループを回す共通部品

学生は process(frame) -> frame だけを書けばよい．

    from common import run

    def process(frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if __name__ == "__main__":
        run(process)

実行時のオプション:
    uv run python xxx.py                     # Webカメラ(0番)で実行
    uv run python xxx.py --camera 1          # 1番のカメラを使う
    uv run python xxx.py --video foo.mp4     # 動画ファイルで実行(最後まで行くと先頭に戻る)

実行中のキー操作:
    q : 終了
    r : 録画の開始/停止 (recordings/ に保存される)
    v : カメラ ⇔ 最後に録画した動画 の切り替え
    スペース : 一時停止/再開
    それ以外のキーは run(process, on_key=関数) で受け取れる

画面左上の表示:
    FPS        : 1秒あたりに処理できたフレーム数 (カメラの性能にも制限される)
    process ms : process 関数1回にかかった時間 (自分の処理の重さ)
動画ファイルは元の動画の速さで再生する (処理が間に合わないときは遅くなる)．
"""

import argparse
import os
import sys
import time
from pathlib import Path

import cv2
import numpy as np

RECORD_DIR = Path("recordings")


def open_capture(source):
    """カメラ番号(int)または動画ファイルのパス(str)から VideoCapture を作る"""
    if isinstance(source, int):
        # Windows では CAP_DSHOW を使わないとカメラの起動が非常に遅いことがある
        if sys.platform.startswith("win"):
            cap = cv2.VideoCapture(source, cv2.CAP_DSHOW)
        else:
            cap = cv2.VideoCapture(source)
    else:
        if not Path(source).exists():
            raise FileNotFoundError(f"動画ファイルが見つからない: {source}")
        cap = cv2.VideoCapture(str(source))

    if not cap.isOpened():
        raise RuntimeError(f"カメラ/動画を開けなかった: {source}")
    return cap


def to_bgr(img):
    """表示・録画用に，グレースケールや bool の画像を3チャンネルの uint8 に揃える"""
    if img.dtype == bool:
        img = img.astype(np.uint8) * 255
    if img.dtype != np.uint8:
        img = np.clip(img, 0, 255).astype(np.uint8)
    if img.ndim == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    return img


def draw_status(img, fps, process_ms, recording, source_name):
    """画面左上に FPS と状態を描く"""
    text = f"FPS: {fps:5.1f}  process: {process_ms:5.1f} ms  [{source_name}]"
    cv2.putText(img, text, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 3)
    cv2.putText(img, text, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
    if recording:
        cv2.circle(img, (img.shape[1] - 20, 20), 8, (0, 0, 255), -1)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--camera", type=int, default=0, help="使うカメラの番号")
    parser.add_argument("--video", type=str, default=None, help="カメラの代わりに使う動画ファイル")
    # 以下は動作確認用(授業では使わない)
    parser.add_argument("--max-frames", type=int, default=None, help=argparse.SUPPRESS)
    parser.add_argument("--headless", action="store_true", help=argparse.SUPPRESS)
    args, _ = parser.parse_known_args(argv)
    args.headless = args.headless or bool(os.environ.get("RV_HEADLESS"))
    return args


def run(process, window="output", show_input=True, on_key=None, argv=None):
    """カメラ(または動画)から1フレームずつ読み込み，process に渡して結果を表示する

    process(frame) の戻り値は次のどちらか:
      - 画像1枚 (np.ndarray)               : window に表示する
      - {"ウィンドウ名": 画像, ...} の辞書 : 複数のウィンドウに表示する

    Args:
        process: BGR画像を1枚受け取り，画像(または画像の辞書)を返す関数
        window: 結果を表示するウィンドウ名
        show_input: True なら入力画像も "input" ウィンドウに表示する
        on_key: q, r, v, スペース 以外のキーが押されたときに呼ばれる関数 (引数はキーの文字)
        argv: コマンドライン引数(テスト用．通常は指定しない)
    """
    args = parse_args(argv)

    camera_source = args.camera
    source = args.video if args.video is not None else camera_source
    cap = open_capture(source)
    last_recording = None

    writer = None
    paused = False
    fps = 0.0
    process_ms = 0.0
    prev_time = time.perf_counter()
    n_frames = 0
    frame = None

    while True:
        if not paused or frame is None:
            ret, frame = cap.read()
            if not ret:
                if isinstance(source, int):
                    print("カメラから画像を取得できなかった")
                    break
                # 動画ファイルは最後まで行ったら先頭に戻す
                if args.max_frames is not None:
                    break
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

        # 学生が書いた処理を呼ぶ(入力画像を書き換えられても大丈夫なようにコピーを渡す)
        t0 = time.perf_counter()
        result = process(frame.copy())
        t1 = time.perf_counter()
        process_ms = 0.9 * process_ms + 0.1 * (1000 * (t1 - t0)) if process_ms > 0 else 1000 * (t1 - t0)
        outputs = result if isinstance(result, dict) else {window: result}

        # FPS (前フレームからの経過時間で計算し，表示がちらつかないよう平滑化)
        now = time.perf_counter()
        dt = now - prev_time
        prev_time = now
        if dt > 0:
            fps = 0.9 * fps + 0.1 * (1.0 / dt) if fps > 0 else 1.0 / dt

        source_name = "camera" if isinstance(source, int) else Path(source).name
        if writer is not None:
            writer.write(frame)

        n_frames += 1
        if args.max_frames is not None and n_frames >= args.max_frames:
            break
        if args.headless:
            continue

        if show_input:
            cv2.imshow("input", frame)
        for i, (name, img) in enumerate(outputs.items()):
            img = to_bgr(img).copy()
            if i == 0:
                draw_status(img, fps, process_ms, writer is not None, source_name)
            cv2.imshow(name, img)

        # 動画ファイルは元の動画の速さで再生する
        delay = 1
        if not isinstance(source, int):
            video_fps = cap.get(cv2.CAP_PROP_FPS)
            if video_fps and 0 < video_fps <= 120:
                elapsed_ms = 1000 * (time.perf_counter() - t0)
                delay = max(1, int(1000 / video_fps - elapsed_ms))
        key = cv2.waitKey(delay) & 0xFF
        if key == ord("q"):
            break
        elif key == ord(" "):
            paused = not paused
        elif key == ord("r"):
            if writer is None:
                RECORD_DIR.mkdir(exist_ok=True)
                last_recording = RECORD_DIR / time.strftime("%Y%m%d_%H%M%S.mp4")
                h, w = frame.shape[:2]
                rec_fps = cap.get(cv2.CAP_PROP_FPS)
                if not rec_fps or rec_fps <= 0 or rec_fps > 120:
                    rec_fps = 30
                writer = cv2.VideoWriter(
                    str(last_recording), cv2.VideoWriter_fourcc(*"mp4v"), rec_fps, (w, h)
                )
                print(f"録画開始: {last_recording}")
            else:
                writer.release()
                writer = None
                print(f"録画終了: {last_recording}")
        elif key == ord("v"):
            if writer is not None:
                print("録画中は切り替えられない．r で録画を止めてから v を押す")
                continue
            if isinstance(source, int):
                if last_recording is None:
                    print("まだ録画していない．r で録画してから v を押す")
                    continue
                new_source = str(last_recording)
            else:
                new_source = camera_source
            cap.release()
            source = new_source
            cap = open_capture(source)
            frame = None
            print(f"入力を切り替えた: {source}")
        elif key != 255 and on_key is not None:
            on_key(chr(key))

    if writer is not None:
        writer.release()
    cap.release()
    cv2.destroyAllWindows()


def tile(images, cols=2, labels=None, width=None):
    """複数の画像を格子状に並べて1枚にする (比較表示用)

    Args:
        images: 画像のリスト (グレースケールとカラーが混ざっていてもよい)
        cols: 1行に並べる枚数
        labels: 各画像の左上に書く文字列のリスト (省略可)
        width: 1枚あたりの幅 (省略すると最初の画像の幅)．高さは縦横比を保って決まる
    """
    first = to_bgr(images[0])
    w = width or first.shape[1]
    h = int(first.shape[0] * w / first.shape[1])
    cells = []
    for i, img in enumerate(images):
        cell = cv2.resize(to_bgr(img), (w, h))
        if labels is not None and i < len(labels):
            cv2.putText(cell, labels[i], (10, h - 12), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 4)
            cv2.putText(cell, labels[i], (10, h - 12), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
        cells.append(cell)
    while len(cells) % cols != 0:
        cells.append(np.zeros_like(cells[0]))
    rows = [np.hstack(cells[i : i + cols]) for i in range(0, len(cells), cols)]
    return np.vstack(rows)
