"""第2週-07 [課題]: 複数の色を同時に追跡する

実行方法 (second で):
    uv run 07_multi_color.py                  # Webカメラで実行
    uv run 07_multi_color.py --video 動画.mp4  # 動画ファイルで実行

解説は second/README.md の「07」を参照．
色ごとの HSV の範囲を辞書で管理し，それぞれの色の最も大きい領域の重心に，その色の円を描く．
HSV の範囲 (main の hsv_ranges) は自分の物体に合わせて書き換えること (05 のトラックバーで調べた値を使うとよい)．
q キーで終了する．
"""

import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[1]))
from common import run

def largest_region_center(mask, min_area):
    """最も大きい領域の重心 (cx, cy) を返す．領域が無ければ None (06 と同じ)"""
    n_labels, _, stats, centroids = cv2.connectedComponentsWithStats(mask)
    if n_labels < 2:
        return None
    i = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    if stats[i, cv2.CC_STAT_AREA] < min_area:
        return None
    return float(centroids[i, 0]), float(centroids[i, 1])


# ============================================================
# 課題1: 色ごとに重心を求める
# ============================================================
def detect_colors(frame, hsv_ranges, min_area=300):
    """hsv_ranges の各色について，HSV のマスクを作り，最も大きい領域の重心を求めて
    {"色の名前": (cx, cy) または None, ...} の辞書で返せ．
    HSV への変換は1回だけでよい (色ごとに変換し直すと遅い)"""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    centers = {}
    # TODO

    return centers


# ============================================================
# 課題2: 重心に円を描く
# ============================================================
def draw_centers(frame, centers, hsv_ranges):
    """centers の各色について，重心の位置に半径 15 の塗りつぶした円を，その色の "draw" の色で描け．
    見つからなかった色 (None) は描かない"""
    # TODO

    return frame


def process(frame):
    centers = detect_colors(frame, hsv_ranges)
    return draw_centers(frame, centers, hsv_ranges)


if __name__ == "__main__":
    # 色の名前: {"lower": [H, S, V], "upper": [H, S, V], "draw": 描画色 (B, G, R)}
    hsv_ranges = {
        "blue": {"lower": [100, 80, 50], "upper": [125, 255, 255], "draw": (255, 0, 0)},
        "green": {"lower": [45, 80, 50], "upper": [75, 255, 255], "draw": (0, 255, 0)},
        "pink": {"lower": [160, 80, 50], "upper": [175, 255, 255], "draw": (255, 0, 255)},
    }
    run(process)
