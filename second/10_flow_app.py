"""第2週-10: オプティカルフローでボールを動かすアプリ

実行方法 (second で):
    uv run 10_flow_app.py                  # Webカメラで実行
    uv run 10_flow_app.py --video 動画.mp4  # 動画ファイルで実行

解説は second/README.md の「10」を参照．
画面の中の動きの向きに合わせて，スタジアムのボールを上下左右に動かす．
たくさんの点の動きから「全体としてどちらに動いたか」を決める方法を2つ切り替えて比べられる．
    method 0: 最も大きく動いた1点の動きを使う
    method 1: 全点の動きの合計を使う
q キーで終了する．
"""

import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[1]))
from common import Trackbars, run


def motion_vector(good0, good1, method):
    """たくさんの点の動き (good1 - good0) を1つのベクトル (dx, dy) にまとめる"""
    if len(good0) == 0:
        return 0.0, 0.0
    d = good1 - good0  # 各点の (dx, dy)
    if method == 0:
        v = d[np.argmax(np.linalg.norm(d, axis=1))]  # 最も大きく動いた点
    else:
        v = d.sum(axis=0)  # 全点の合計
    return float(v[0]), float(v[1])


def direction(dx, dy, threshold):
    """大きいほうの成分が threshold 以上なら，その向き ("left" など) を返す．小さければ None"""
    if max(abs(dx), abs(dy)) < threshold:
        return None
    if abs(dx) >= abs(dy):
        return "right" if dx > 0 else "left"
    return "down" if dy > 0 else "up"


def track(gray):
    """09 と同じ追跡 (10 フレームごとに点を選び直す)"""
    good0 = good1 = np.empty((0, 2), np.float32)
    p0 = state["points"]
    if p0 is not None and len(p0) > 0:
        p1, st, _ = cv2.calcOpticalFlowPyrLK(state["prev_gray"], gray, p0, None, winSize=(15, 15), maxLevel=2)
        if p1 is not None:
            ok = st.ravel() == 1
            good0, good1 = p0.reshape(-1, 2)[ok], p1.reshape(-1, 2)[ok]
    state["count"] += 1
    if len(good1) < 10 or state["count"] % 10 == 0:
        state["points"] = cv2.goodFeaturesToTrack(gray, maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)
    else:
        state["points"] = good1.reshape(-1, 1, 2)
    state["prev_gray"] = gray
    return good0, good1


def process(frame):
    h, w = frame.shape[:2]
    stadium = cv2.resize(stadium_src, (w, h))
    bh, bw = ball.shape[:2]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if state["prev_gray"] is None:
        state.update(prev_gray=gray, ball=[w // 2, h // 2])

    good0, good1 = track(gray)
    dx, dy = motion_vector(good0, good1, tb["method"])
    d = direction(dx, dy, max(1, tb["threshold"]))

    step = tb["step"]
    moves = {"left": (-step, 0), "right": (step, 0), "up": (0, -step), "down": (0, step)}
    if d is not None:
        state["ball"][0] += moves[d][0]
        state["ball"][1] += moves[d][1]
    # はみ出さないように制限
    state["ball"][0] = max(bw // 2, min(state["ball"][0], w - (bw - bw // 2)))
    state["ball"][1] = max(bh // 2, min(state["ball"][1], h - (bh - bh // 2)))

    cx, cy = state["ball"]
    output = stadium.copy()
    output[cy - bh // 2 : cy - bh // 2 + bh, cx - bw // 2 : cx - bw // 2 + bw] = ball

    for p, q in zip(good0, good1):
        cv2.line(frame, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), (0, 255, 0), 2)
    return {"output": output, "flow": frame}


if __name__ == "__main__":
    image_dir = Path(__file__).resolve().parent / "image_data"
    ball = cv2.imread(str(image_dir / "ball.png"))
    stadium_src = cv2.imread(str(image_dir / "stadium.png"))
    tb = Trackbars(
        "params",
        {
            "method": (0, 1),  # 0: 最も大きく動いた1点，1: 全点の合計
            "threshold": (30, 300),  # 動いたとみなす移動量 [px/フレーム]
            "step": (10, 50),  # ボールを1回に動かす量 [px]
        },
    )
    # フレームをまたいで覚えておく値
    state = {"prev_gray": None, "points": None, "count": 0, "ball": None}
    run(process)
