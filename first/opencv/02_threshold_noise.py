"""第1週 OpenCV-2: 二値化とノイズ除去

実行方法 (first/opencv で):
    uv run python 02_threshold_noise.py                  # Webカメラで実行
    uv run python 02_threshold_noise.py --video 動画.mp4  # 動画ファイルで実行

解説は first/README.md の「OpenCV-2 二値化とノイズ除去」を参照．

進め方:
    1. 課題1〜3 の `...` を埋め，課題4 のバグを直す．実行すると最初に自動チェックが走る
    2. チェックがすべて OK になるとカメラが起動する
    3. トラックバーで閾値・ノイズの量・カーネルの大きさを動かし，ファイル末尾の [観察] に答える

キー操作: q 終了 / r 録画開始・停止 / v カメラ⇔録画の切り替え / スペース 一時停止
"""

import cv2
import numpy as np

from common import Trackbars, run


# ============================================================
# 課題1: 二値化を自分で書く
# ============================================================
# グレースケール画像 gray の画素が閾値 t より大きければ 255，それ以外は 0 にした画像を返せ．
# numpy だけで書くこと (08_numpy_mask の np.where を思い出す)．dtype は uint8．
# 自動チェックでは cv2.threshold(gray, t, 255, cv2.THRESH_BINARY) と結果を比べる．
def threshold_numpy(gray, t):
    return ...  # TODO


# ============================================================
# 課題2: 収縮と膨張でオープニング処理を作る
# ============================================================
# オープニング = 収縮(erode) してから 膨張(dilate) する処理．小さな白い点(ノイズ)が消える．
# k x k の正方形のカーネル (np.ones((k, k), np.uint8)) を使って，
# cv2.erode → cv2.dilate の順に適用した結果を返せ．
# 自動チェックでは cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel) と結果を比べる．
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
# 自動チェック (ここは編集しなくてよい)
# ============================================================
def run_checks():
    rng = np.random.default_rng(0)
    gray = rng.integers(0, 256, (60, 80), dtype=np.uint8)

    out = threshold_numpy(gray, 100)
    assert out is not ..., "課題1 がまだ未記入"
    _, expected = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    assert out.dtype == np.uint8, f"課題1: dtype を uint8 にすること (今は {out.dtype})"
    assert np.array_equal(out, expected), "課題1: cv2.threshold と結果が一致しない (等号の向きに注意)"
    print("OK 課題1")

    mask = np.zeros((60, 80), np.uint8)
    mask[10:50, 20:60] = 255
    mask[5, 5] = 255  # 孤立した白い点
    out = opening(mask, 3)
    assert out is not ..., "課題2 がまだ未記入"
    expected = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    assert np.array_equal(out, expected), "課題2: cv2.morphologyEx の結果と一致しない (順番に注意)"
    assert out[5, 5] == 0, "課題2: 孤立した点が消えていない"
    print("OK 課題2")

    out = add_noise(mask, 0.1, np.random.default_rng(1))
    assert out is not ... and out.shape == mask.shape, "課題3 がまだ未記入"
    changed = (out != mask).mean()
    assert 0.07 < changed < 0.13, f"課題3: 反転した画素の割合が 0.1 付近になっていない ({changed:.3f})"
    assert set(np.unique(out)) <= {0, 255}, "課題3: 値は 0 か 255 だけにすること"
    print("OK 課題3")

    for v, k in [(0, 3), (1, 5), (2, 7), (5, 13)]:
        assert to_odd_ksize(v) == k, f"課題4: to_odd_ksize({v}) は {k} を返すこと (今は {to_odd_ksize(v)})"
    print("OK 課題4")


# ============================================================
# カメラで実行 (チェックが通ったら動く)
# ============================================================
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


def process(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    binary = threshold_numpy(gray, tb["threshold"])
    noisy = add_noise(binary, tb["noise_%"] / 100, rng)
    median = cv2.medianBlur(noisy, to_odd_ksize(tb["median_k"]))
    opened = opening(noisy, max(1, tb["open_k"]))
    return {"noisy": noisy, "median": median, "opening": opened}


if __name__ == "__main__":
    run_checks()
    run(process)


# ============================================================
# [観察] 実際に試して，結果と原因をそれぞれ一文で書け
# ============================================================
# 観察1: 白い紙の上に黒いペンを置いて二値化し，threshold を調整した．
#        そのあと手で紙に影を落とすと何が起きたか．1つの閾値で画面全体をうまく分けられるか．
#   結果:
#   原因:
#
# 観察2: noise_% を大きくしていったとき，median と opening のどちらがノイズに強かったか．
#        「白い点」と「黒い点(白い物体に開いた穴)」で違いはあったか．
#   結果:
#   原因:
#
# 観察3: open_k を大きくしていくと，ノイズ以外に何が消えたか．
#   結果:
#   原因:
