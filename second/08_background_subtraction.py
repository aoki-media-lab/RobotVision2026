"""第2週-08: 背景差分 — 自分で作る方法と OpenCV の方法を比べる

実行方法 (second で):
    uv run 08_background_subtraction.py                  # Webカメラで実行
    uv run 08_background_subtraction.py --video 動画.mp4  # 動画ファイルで実行
    uv run 08_background_subtraction.py --video image_data/opticalflow.avi

解説は second/README.md の「08」を参照．
色を使わずに「動いているもの」を取り出す方法を4つ並べて比べる．
    (a) 静的背景差分 : 最初のフレームを背景とし，その背景との差 (撮り直すときは起動し直す)
    (b) フレーム間差分: 1つ前のフレームとの差
    (c) 移動平均背景 : 背景を少しずつ更新しながら，その背景との差
    (d) MOG          : OpenCV の背景差分 (画素ごとに背景の色の分布を学習する)
(a)〜(c) は numpy と簡単な OpenCV の関数だけで書いている．
q キーで終了する．
"""

import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[1]))
from common import Trackbars, run


def diff_mask(a, b, th):
    """グレースケール画像 a と b の差の絶対値が th より大きい画素を 255 にしたマスク"""
    diff = cv2.absdiff(a, b)  # uint8 のまま a - b とすると負の値が回り込むので absdiff を使う
    return np.where(diff > th, 255, 0).astype(np.uint8)


def update_background(bg, gray, alpha):
    """移動平均で背景を更新する: (1 - alpha) * bg + alpha * gray
    小さな変化が切り捨てられないよう，背景は float32 で持つ"""
    return ((1 - alpha) * bg + alpha * gray).astype(np.float32)


def process(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    th = tb["threshold"]

    if state["static_bg"] is None:
        state["static_bg"] = gray
        state["prev"] = gray
        state["avg_bg"] = gray.astype(np.float32)

    m_static = diff_mask(gray, state["static_bg"], th)
    m_frame = diff_mask(gray, state["prev"], th)
    m_avg = diff_mask(gray, state["avg_bg"].astype(np.uint8), th)
    m_mog = subtractor.apply(frame)

    state["prev"] = gray
    state["avg_bg"] = update_background(state["avg_bg"], gray, tb["alpha_%"] / 100)

    return {
        "input": frame,
        "(a) static": m_static,
        "(b) frame diff": m_frame,
        "(c) running avg": m_avg,
        "(d) MOG": m_mog,
    }


if __name__ == "__main__":
    tb = Trackbars(
        "params",
        {
            "threshold": (30, 255),  # (a)(b)(c) の差の閾値
            "alpha_%": (5, 100),  # (c) の更新の速さ [%]
        },
    )
    # MOG は1回だけ作り，毎フレーム同じものに apply する
    subtractor = cv2.bgsegm.createBackgroundSubtractorMOG()
    # フレームをまたいで覚えておく値
    state = {"static_bg": None, "prev": None, "avg_bg": None}
    run(process)
