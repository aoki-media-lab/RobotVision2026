"""第2週-03 [課題]: HSV による色の抽出

実行方法 (second で):
    uv run 03_hsv_color.py                  # Webカメラで実行
    uv run 03_hsv_color.py --video 動画.mp4  # 動画ファイルで実行

解説は second/README.md の「03」を参照．

進め方:
    1. 課題1〜3 の `...` を埋めて実行すると，カメラが起動する
    2. トラックバーで HSV の範囲を動かし，手元の物体(ペンのキャップなど)だけが白くなるよう調整する
    3. second/README.md の [観察] に答える

q キーで終了する．
"""

import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[1]))
from common import Trackbars, run


# ============================================================
# 課題1: HSV の範囲でマスクを作る
# ============================================================
# BGR の画像を HSV に変換し，lower 以上 upper 以下の画素を 255，それ以外を 0 にしたマスクを返す．
#   OpenCV の HSV は H: 0〜179 (角度の半分), S: 0〜255, V: 0〜255
#   使う関数: cv2.cvtColor (変換コードは cv2.COLOR_BGR2HSV)，cv2.inRange
def hsv_mask(frame, lower, upper):
    """
    Args:
        frame: BGR画像 (高さ, 幅, 3)
        lower: [H, S, V] の下限
        upper: [H, S, V] の上限
    Returns:
        マスク画像 (高さ, 幅)．範囲内が 255，範囲外が 0 (dtype は uint8)
    """
    hsv = ...  # TODO
    mask = ...  # TODO
    return mask


# ============================================================
# 課題2: 赤のマスク
# ============================================================
# 赤は H が 0 付近と 179 付近の両端にまたがるので，1回の範囲指定では取れない．
# hsv_mask を2回使い，2つのマスクの「または」をとって返せ．
#   範囲1: H 0〜h_width, 範囲2: H (179 - h_width)〜179．S と V はどちらも s_min〜255, v_min〜255
#   使う関数: cv2.bitwise_or (または 08_numpy_mask の | を使ってもよい)
def red_mask(frame, h_width, s_min, v_min):
    mask1 = ...  # TODO
    mask2 = ...  # TODO
    return ...  # TODO


# ============================================================
# 課題3: マスクした部分だけ元の色を残す
# ============================================================
# マスクが 255 の画素は frame の色のまま，0 の画素は黒にした画像を返せ．
#   使う関数: cv2.bitwise_and(frame, frame, mask=mask)  (np.where を使ってもよい)
def apply_mask(frame, mask):
    return ...  # TODO


# ============================================================
# カメラで実行
# ============================================================
def process(frame):
    lower = [tb["H_min"], tb["S_min"], tb["V_min"]]
    upper = [tb["H_max"], tb["S_max"], tb["V_max"]]
    mask = hsv_mask(frame, lower, upper)
    return {"result": apply_mask(frame, mask), "mask": mask}


if __name__ == "__main__":
    # 名前: (初期値, 最大値)
    tb = Trackbars(
        "params",
        {
            "H_min": (0, 179),
            "H_max": (30, 179),
            "S_min": (60, 255),
            "S_max": (255, 255),
            "V_min": (60, 255),
            "V_max": (255, 255),
        },
    )
    run(process)
