"""第1週 OpenCV-1: HSV による色の抽出

実行方法 (first/opencv で):
    uv run python 01_hsv_color.py                  # Webカメラで実行
    uv run python 01_hsv_color.py --video 動画.mp4  # 動画ファイルで実行

解説は first/README.md の「OpenCV-1 HSV による色の抽出」を参照．

進め方:
    1. 課題1〜3 の `...` を埋める．実行すると最初に自動チェックが走る
    2. チェックがすべて OK になるとカメラが起動する
    3. トラックバーで HSV の範囲を動かし，手元の物体(ペンのキャップなど)だけが白くなるよう調整する
    4. ファイル末尾の [観察] に答える

キー操作: q 終了 / r 録画開始・停止 / v カメラ⇔録画の切り替え / スペース 一時停止
"""

import cv2
import numpy as np

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
# 自動チェック (ここは編集しなくてよい)
# ============================================================
def make_test_image():
    """色の分かっているパッチを並べたテスト画像 (BGR)"""
    colors = {
        "orange": (0, 128, 255),
        "blue": (255, 80, 0),
        "green": (0, 200, 0),
        "red_low": (0, 0, 230),  # H ≒ 0
        "red_high": (60, 0, 230),  # H ≒ 172 (紫寄りの赤)
        "white": (255, 255, 255),
        "black": (0, 0, 0),
    }
    img = np.zeros((40, 40 * len(colors), 3), np.uint8)
    for i, bgr in enumerate(colors.values()):
        img[:, 40 * i : 40 * (i + 1)] = bgr
    return img, list(colors)


def patch_values(mask, names):
    assert mask is not ..., "まだ未記入の課題がある"
    assert isinstance(mask, np.ndarray), "マスクは numpy 配列で返すこと"
    assert mask.ndim == 2, f"マスクは2次元 (高さ, 幅) にすること．今の shape: {mask.shape}"
    return {name: int(mask[20, 40 * i + 20]) for i, name in enumerate(names)}


def run_checks():
    img, names = make_test_image()

    m = patch_values(hsv_mask(img, [10, 100, 100], [25, 255, 255]), names)
    assert m["orange"] == 255, "課題1: オレンジ (H≒15) が抽出されていない"
    assert all(m[n] == 0 for n in names if n != "orange"), f"課題1: オレンジ以外も抽出されている: {m}"
    print("OK 課題1")

    m = patch_values(red_mask(img, 10, 100, 100), names)
    assert m["red_low"] == 255 and m["red_high"] == 255, f"課題2: 赤の両端が抽出されていない: {m}"
    assert all(m[n] == 0 for n in names if not n.startswith("red")), f"課題2: 赤以外も抽出されている: {m}"
    print("OK 課題2")

    mask = hsv_mask(img, [10, 100, 100], [25, 255, 255])
    out = apply_mask(img, mask)
    assert out is not ..., "課題3 がまだ未記入"
    assert out.shape == img.shape, "課題3: 出力は入力と同じ shape のカラー画像にすること"
    assert (out[20, 20] == img[20, 20]).all(), "課題3: マスクが 255 の画素は元の色のままにすること"
    assert (out[20, 60] == 0).all(), "課題3: マスクが 0 の画素は黒にすること"
    print("OK 課題3")


# ============================================================
# カメラで実行 (チェックが通ったら動く)
# ============================================================
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


def process(frame):
    lower = [tb["H_min"], tb["S_min"], tb["V_min"]]
    upper = [tb["H_max"], tb["S_max"], tb["V_max"]]
    mask = hsv_mask(frame, lower, upper)
    return {"result": apply_mask(frame, mask), "mask": mask}


if __name__ == "__main__":
    run_checks()
    run(process)


# ============================================================
# [観察] 実際に試して，結果と原因をそれぞれ一文で書け
# ============================================================
# 観察1: 部屋の照明を暗くする(またはカメラを手で覆って暗くする)と，マスクはどう変わったか．
#        H・S・V のどの範囲を広げると耐えられるようになったか．それはなぜか．
#   結果:
#   原因:
#
# 観察2: 抽出したい物体と同じような色の物体(服，背景など)を画面に入れると何が起きたか．
#        HSV の範囲の調整だけで解決できるか．できないなら何の情報が足りないか．
#   結果:
#   原因:
#
# 観察3: 物体をカメラに近づけたり傾けたりして，光の反射(テカリ)が入ると何が起きたか．
#   結果:
#   原因:
