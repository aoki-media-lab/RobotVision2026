"""第2週-05: 複数の色を同時に追跡する

実行方法 (second で):
    uv run python 05_multi_color.py                  # Webカメラで実行
    uv run python 05_multi_color.py --video 動画.mp4  # 動画ファイルで実行

解説は second/README.md の「05」を参照．
色ごとの HSV の範囲を辞書で管理し，それぞれの色の最も大きい領域の重心に，その色の円を描く．
HSV の範囲は自分の物体に合わせて書き換えること (03 のトラックバーで調べた値を使うとよい)．

キー操作: q 終了 / r 録画開始・停止 / v カメラ⇔録画の切り替え / スペース 一時停止
"""

import cv2
import numpy as np

from common import run

# 色の名前: {"lower": [H, S, V], "upper": [H, S, V], "draw": 描画色 (B, G, R)}
HSV_RANGES = {
    "blue": {"lower": [100, 80, 50], "upper": [125, 255, 255], "draw": (255, 0, 0)},
    "green": {"lower": [45, 80, 50], "upper": [75, 255, 255], "draw": (0, 255, 0)},
    "pink": {"lower": [160, 80, 50], "upper": [175, 255, 255], "draw": (255, 0, 255)},
}


def largest_region_center(mask, min_area):
    """最も大きい領域の重心 (cx, cy) を返す．領域が無ければ None (04 と同じ)"""
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
# hsv_ranges の各色について，HSV のマスクを作り，最も大きい領域の重心を求めて
# {"色の名前": (cx, cy) または None, ...} の辞書で返せ．
#   - HSV への変換は1回だけでよい (色ごとに変換し直すと遅い)
#   - for 文で辞書の items() を回す (第1週 04_control_flow)
def detect_colors(frame, hsv_ranges, min_area=100):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    centers = {}
    # TODO

    return centers


# ============================================================
# 課題2: 重心に円を描く
# ============================================================
# centers の各色について，重心の位置に半径 15 の塗りつぶした円を，その色の "draw" の色で描け．
# 見つからなかった色 (None) は描かない．
def draw_centers(frame, centers, hsv_ranges):
    # TODO

    return frame


# ============================================================
# 自動チェック (ここは編集しなくてよい)
# ============================================================
def run_checks():
    img = np.zeros((100, 200, 3), np.uint8)
    img[10:40, 10:40] = (255, 50, 0)  # 青
    img[50:90, 120:180] = (0, 200, 0)  # 緑
    centers = detect_colors(img, HSV_RANGES)
    assert set(centers) == set(HSV_RANGES), f"課題1: すべての色の名前をキーにすること (今は {list(centers)})"
    assert centers["pink"] is None, "課題1: 見つからない色は None にすること"
    assert np.allclose(centers["blue"], (24.5, 24.5)), f"課題1: blue の重心が違う ({centers['blue']})"
    assert np.allclose(centers["green"], (149.5, 69.5)), f"課題1: green の重心が違う ({centers['green']})"
    print("OK 課題1")

    out = draw_centers(np.zeros((100, 200, 3), np.uint8), centers, HSV_RANGES)
    assert (out[24, 24] == (255, 0, 0)).all() and (out[69, 149] == (0, 255, 0)).all(), "課題2: 円が描かれていない"
    print("OK 課題2")


def process(frame):
    centers = detect_colors(frame, HSV_RANGES, min_area=300)
    return draw_centers(frame, centers, HSV_RANGES)


if __name__ == "__main__":
    run_checks()
    run(process)


# ============================================================
# [観察] 実際に試して，結果と原因をそれぞれ一文で書け
# ============================================================
# 観察1: 3色の物体を用意し，すべてを同時に検出できる HSV の範囲を探せ．
#        ある色の範囲を広げると別の色を誤検出する，ということは起きたか．
#   結果:
#   原因:
#
# 観察2: 背景 (服，机，壁) の中に，誤検出されやすい色はあったか．
#   結果:
#   原因:
