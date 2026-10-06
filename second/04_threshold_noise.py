"""第2週-04 [課題]: 二値化とノイズ除去

実行方法 (second で):
    uv run 04_threshold_noise.py                  # Webカメラで実行
    uv run 04_threshold_noise.py --video 動画.mp4  # 動画ファイルで実行

解説は second/README.md の「04」を参照．

進め方:
    1. 課題1〜3 の `...` を埋め，課題4 のバグを直して実行すると，カメラが起動する
    2. トラックバーで閾値・ノイズの量・カーネルの大きさを動かし，second/README.md の [観察] に答える

q キーで終了する．
"""

import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[1]))
from common import Trackbars, run


# ============================================================
# 課題1: 二値化を自分で書く
# ============================================================
# グレースケール画像 gray の画素が閾値 t より大きければ 255，それ以外は 0 にした画像を返せ．
# numpy だけで書くこと (08_numpy_mask の np.where を思い出す)．dtype は uint8．
# cv2.threshold(gray, t, 255, cv2.THRESH_BINARY) と同じ結果になる．
def threshold_numpy(gray, t):
    return ...  # TODO


# ============================================================
# 課題2: 収縮と膨張でオープニング処理を作る
# ============================================================
# オープニング = 収縮(erode) してから 膨張(dilate) する処理．小さな白い点(ノイズ)が消える．
# k x k の正方形のカーネル (np.ones((k, k), np.uint8)) を使って，
# cv2.erode → cv2.dilate の順に適用した結果を返せ．
# cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel) と同じ結果になる．
def opening(mask, k):
    kernel = ...  # TODO
    eroded = ...  # TODO
    return ...  # TODO


# ============================================================
# 課題3: ごま塩ノイズを加える
# ============================================================
# 二値画像 mask のうち，割合 ratio (0〜1) の画素をランダムに選び，値を反転(0⇔255)した画像を返せ．
# ノイズ除去の効果を確かめるために使う．
#   ヒント: rng.random(mask.shape) < ratio で「選ばれた画素」の bool 配列が作れる
#           反転は 255 - mask で計算できる
def add_noise(mask, ratio, rng):
    noisy = mask.copy()
    selected = ...  # TODO
    noisy[selected] = ...  # TODO
    return noisy


# ============================================================
# 課題4: バグ修正
# ============================================================
# トラックバーの値 v から cv2.medianBlur のカーネルの大きさを決めている．
# トラックバーを偶数にすると medianBlur がエラーで落ちる．
# medianBlur のカーネルの大きさは 3 以上の奇数でなければならない．
# v = 0, 1, 2, ... に対して 3, 5, 7, ... を返すように直せ．
def to_odd_ksize(v):
    return v


# ============================================================
# カメラで実行
# ============================================================
def process(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    binary = threshold_numpy(gray, tb["threshold"])
    noisy = add_noise(binary, tb["noise_%"] / 100, rng)
    median = cv2.medianBlur(noisy, to_odd_ksize(tb["median_k"]))
    opened = opening(noisy, max(1, tb["open_k"]))
    return {"noisy": noisy, "median": median, "opening": opened}


if __name__ == "__main__":
    tb = Trackbars(
        "params",
        {
            "threshold": (120, 255),  # 二値化の閾値
            "noise_%": (5, 30),  # 加えるノイズの割合 [%]
            "median_k": (1, 10),  # medianBlur のカーネル (to_odd_ksize で奇数に変換)
            "open_k": (3, 15),  # オープニングのカーネルの大きさ
        },
    )
    rng = np.random.default_rng()
    run(process)
