"""第2週-09: オプティカルフロー (特徴点の追跡)

実行方法 (second で):
    uv run 09_optical_flow.py                  # Webカメラで実行
    uv run 09_optical_flow.py --video image_data/opticalflow.avi

解説は second/README.md の「09」を参照．
    cv2.goodFeaturesToTrack : 追跡しやすい点 (角のような点) を選ぶ
    cv2.calcOpticalFlowPyrLK: 各点が次のフレームでどこに移ったかを Lucas-Kanade 法で求める
追跡に失敗した点は捨てるので，そのままでは点が減り続ける．
点が少なくなったとき，または一定フレームごとに点を選び直す．
q キーで終了する．
"""

import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[1]))
from common import Trackbars, run


def detect(gray):
    """追跡する点を選ぶ．戻り値は (N, 1, 2) の配列，見つからなければ None"""
    return cv2.goodFeaturesToTrack(
        gray,
        maxCorners=max(1, tb["maxCorners"]),
        qualityLevel=max(1, tb["quality_%"]) / 100,
        minDistance=7,
        blockSize=7,
    )


def track(prev_gray, gray, p0):
    """p0 の各点を prev_gray から gray へ追跡し，成功した点の (前の位置, 今の位置) を (N, 2) の配列で返す"""
    empty = np.empty((0, 2), np.float32)
    if p0 is None or len(p0) == 0:
        return empty, empty
    win = max(3, tb["winSize"])
    p1, status, _ = cv2.calcOpticalFlowPyrLK(
        prev_gray, gray, p0, None, winSize=(win, win), maxLevel=tb["maxLevel"]
    )
    if p1 is None:
        return empty, empty
    ok = status.ravel() == 1
    return p0.reshape(-1, 2)[ok], p1.reshape(-1, 2)[ok]


def process(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if state["prev_gray"] is None:
        state.update(prev_gray=gray, points=detect(gray), flow_mask=np.zeros_like(frame))
        return frame

    good0, good1 = track(state["prev_gray"], gray, state["points"])

    # 前の位置から今の位置へ線を引き，今の位置に円を描く (OpenCV 5 では座標を int にする)
    for p, q in zip(good0, good1):
        cv2.line(state["flow_mask"], (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), (0, 255, 0), 2)
        cv2.circle(frame, (int(q[0]), int(q[1])), 4, (0, 0, 255), -1)
    output = cv2.add(frame, state["flow_mask"])

    # 点が少なくなったら，または interval フレームごとに点を選び直す (線も消す)
    state["count"] += 1
    if len(good1) < 10 or state["count"] % max(1, tb["interval"]) == 0:
        state["points"] = detect(gray)
        state["flow_mask"] = np.zeros_like(frame)
    else:
        state["points"] = good1.reshape(-1, 1, 2)
    state["prev_gray"] = gray
    return output


if __name__ == "__main__":
    tb = Trackbars(
        "params",
        {
            "maxCorners": (100, 500),
            "quality_%": (10, 100),  # qualityLevel [%]
            "winSize": (15, 51),
            "maxLevel": (2, 5),  # 画像ピラミッドの段数
            "interval": (30, 300),  # 何フレームごとに点を選び直すか
        },
    )
    # フレームをまたいで覚えておく値
    state = {"prev_gray": None, "points": None, "flow_mask": None, "count": 0}
    run(process)
