"""第2週-05: 色で抽出した領域にラベルを付ける

実行方法 (second で):
    uv run 05_color_labeling.py                  # Webカメラで実行
    uv run 05_color_labeling.py --video 動画.mp4  # 動画ファイルで実行

解説は second/README.md の「05」を参照．
03 の HSV マスクは「どの画素が対象の色か」しか分からない．
ラベリング (連結成分分析) で「つながった白い領域」ごとに番号を振ると，
領域ごとの位置・大きさ・重心が分かり，「物体がどこにあるか」が求まる．
q キーで終了する．
"""

import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[1]))
from common import Trackbars, run


def hsv_mask(frame, lower, upper):
    """HSV の範囲でマスクを作り，メディアンフィルタでノイズを除く"""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
    return cv2.medianBlur(mask, 5)


def largest_regions(mask, n, min_area):
    """面積の大きい順に最大 n 個の領域を返す．min_area より小さい領域は返さない．

    戻り値: [(x, y, w, h, area, cx, cy), ...]
    """
    n_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask)
    # ラベル 0 は背景なので除き，面積の大きい順に並べる
    order = 1 + np.argsort(-stats[1:, cv2.CC_STAT_AREA])
    regions = []
    for i in order[:n]:
        x, y, w, h, area = stats[i]
        if area < min_area:
            break
        cx, cy = centroids[i]
        regions.append((int(x), int(y), int(w), int(h), int(area), float(cx), float(cy)))
    return regions


def draw_regions(frame, regions):
    """各領域の外接矩形 (赤) と重心 (黄) を描く"""
    for x, y, w, h, area, cx, cy in regions:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.circle(frame, (int(cx), int(cy)), 5, (0, 255, 255), -1)
        cv2.putText(frame, f"area {area}", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
    return frame


def process(frame):
    mask = hsv_mask(frame, [tb["H_min"], tb["S_min"], tb["V_min"]], [tb["H_max"], 255, 255])
    regions = largest_regions(mask, max(1, tb["n"]), tb["min_area"])
    return {"result": draw_regions(frame, regions), "mask": mask}


if __name__ == "__main__":
    tb = Trackbars(
        "params",
        {
            "H_min": (0, 179),
            "H_max": (30, 179),
            "S_min": (60, 255),
            "V_min": (60, 255),
            "n": (2, 10),  # 取り出す領域の数
            "min_area": (300, 5000),
        },
    )
    run(process)
