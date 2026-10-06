"""第2週 発展課題: numpy だけで収縮・膨張・メディアンフィルタを作る

実行方法 (second/advanced で):
    uv run erode_numpy.py

for 文で1画素ずつ処理すると非常に遅い．numpy のスライスで「画像をずらしたもの」を
k*k 枚作り，それらの最小値・最大値・中央値をとると高速に書ける．
実行すると，OpenCV の関数と結果が一致するかと，速度を表示する．

ルール:
    - cv2 の関数は使わない (numpy のみ)
    - 画像の端は「端の画素を外側に延長する」(np.pad の mode="edge") でよい
      ただし cv2.erode / cv2.dilate の既定の端の扱いとは異なるので，比べるときは端を除く
"""

import time

import cv2
import numpy as np


def shifted_stack(img, k):
    """img を上下左右に最大 k//2 ずらした画像を k*k 枚重ねた配列 (k*k, 高さ, 幅) を返す"""
    # TODO: np.pad とスライスを使って書く
    ...


def erode_numpy(img, k):
    """k x k の正方形カーネルによる収縮 (近傍の最小値)"""
    ...  # TODO


def dilate_numpy(img, k):
    """k x k の正方形カーネルによる膨張 (近傍の最大値)"""
    ...  # TODO


def median_numpy(img, k):
    """k x k のメディアンフィルタ (近傍の中央値)"""
    ...  # TODO


def compare(name, mine_fn, cv_fn, img, k):
    t0 = time.perf_counter()
    mine = mine_fn(img, k)
    t1 = time.perf_counter()
    ref = cv_fn(img, k)
    t2 = time.perf_counter()
    assert mine is not None, f"{name} がまだ未記入"
    r = k // 2
    ok = np.array_equal(mine[r:-r, r:-r], ref[r:-r, r:-r])
    print(f"{name:7s} k={k}: {'一致' if ok else '不一致'}  numpy {1000 * (t1 - t0):6.1f} ms / OpenCV {1000 * (t2 - t1):6.1f} ms")


if __name__ == "__main__":
    rng = np.random.default_rng(0)
    img = rng.integers(0, 256, (480, 640), dtype=np.uint8)
    for k in (3, 5):
        kernel = np.ones((k, k), np.uint8)
        compare("erode", erode_numpy, lambda x, k: cv2.erode(x, kernel), img, k)
        compare("dilate", dilate_numpy, lambda x, k: cv2.dilate(x, kernel), img, k)
        compare("median", median_numpy, lambda x, k: cv2.medianBlur(x, k), img, k)

# 考察: OpenCV は numpy 版より何倍速かったか．k を大きくすると差はどう変わるか．
#       OpenCV はどのような工夫で速くしていると考えられるか (調べてよい)．
