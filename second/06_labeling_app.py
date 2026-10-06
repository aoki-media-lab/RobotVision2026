"""第2週-06: 色の物体の動きでボールを動かすアプリ

実行方法 (second で):
    uv run 06_labeling_app.py                  # Webカメラで実行
    uv run 06_labeling_app.py --video 動画.mp4  # 動画ファイルで実行

解説は second/README.md の「06」を参照．
05 で求めた「最も大きい領域の重心」にボールを置くと，物体を動かしてボールを操作できる．
q キーで終了する．
"""

import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[1]))
from common import Trackbars, run


def hsv_mask(frame, lower, upper):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
    return cv2.medianBlur(mask, 5)


def largest_region_center(mask, min_area):
    """最も大きい領域の重心 (cx, cy) を返す．領域が無ければ None"""
    n_labels, _, stats, centroids = cv2.connectedComponentsWithStats(mask)
    if n_labels < 2:
        return None
    i = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))  # ラベル 0 (背景) を除いて最大
    if stats[i, cv2.CC_STAT_AREA] < min_area:
        return None
    return int(centroids[i, 0]), int(centroids[i, 1])


def paste_center(bg, fg, cx, cy):
    out = bg.copy()
    h, w = fg.shape[:2]
    x0, y0 = cx - w // 2, cy - h // 2
    out[y0 : y0 + h, x0 : x0 + w] = fg
    return out


def clamp_center(cx, cy, bg_w, bg_h, fg_w, fg_h):
    cx = max(fg_w // 2, min(cx, bg_w - (fg_w - fg_w // 2)))
    cy = max(fg_h // 2, min(cy, bg_h - (fg_h - fg_h // 2)))
    return cx, cy


def process(frame):
    h, w = frame.shape[:2]
    stadium = cv2.resize(stadium_src, (w, h))
    fg_h, fg_w = ball.shape[:2]

    mask = hsv_mask(frame, [tb["H_min"], tb["S_min"], tb["V_min"]], [tb["H_max"], 255, 255])
    center = largest_region_center(mask, tb["min_area"])
    if center is None:
        cx, cy = w // 2, h // 2  # 見つからなければ中央に置く
    else:
        cx, cy = center
    cx, cy = clamp_center(cx, cy, w, h, fg_w, fg_h)
    return {"output": paste_center(stadium, ball, cx, cy), "mask": mask}


if __name__ == "__main__":
    image_dir = Path(__file__).resolve().parent / "image_data"
    ball = cv2.imread(str(image_dir / "ball.png"))
    stadium_src = cv2.imread(str(image_dir / "stadium.png"))
    tb = Trackbars(
        "params",
        {
            "H_min": (0, 179),
            "H_max": (30, 179),
            "S_min": (60, 255),
            "V_min": (60, 255),
            "min_area": (300, 5000),
        },
    )
    run(process)
