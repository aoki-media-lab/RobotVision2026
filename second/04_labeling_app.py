"""第2週-04: 色の物体の動きでボールを動かすアプリ

実行方法 (second で):
    uv run python 04_labeling_app.py                  # Webカメラで実行
    uv run python 04_labeling_app.py --video 動画.mp4  # 動画ファイルで実行

解説は second/README.md の「04」を参照．
03 で求めた「最も大きい領域の重心」にボールを置くと，物体を動かしてボールを操作できる．
しかし重心はフレームごとにぶれるので，ボールががたがた震える．
ここでは「過去の位置との重み付き平均」でぶれを抑え，その副作用も観察する．

キー操作: q 終了 / r 録画開始・停止 / v カメラ⇔録画の切り替え / スペース 一時停止
"""

from pathlib import Path

import cv2
import numpy as np

from common import Trackbars, run

IMAGE_DIR = Path(__file__).resolve().parent / "image_data"


# ---------- 01, 03 で作ったもの (完成済み) ----------
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
    return float(centroids[i, 0]), float(centroids[i, 1])


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


# ============================================================
# 課題1: 位置をなめらかにする (指数移動平均)
# ============================================================
# 新しく観測した位置 new と，これまでの推定位置 prev から，次の推定位置を返せ．
#     推定位置 = alpha * new + (1 - alpha) * prev        (0 < alpha <= 1)
# alpha = 1 なら観測値そのまま，alpha が小さいほど過去を重視してなめらかになる．
# prev が None (最初のフレーム) のときは new をそのまま返す．
# new, prev は (x, y) のタプル．戻り値も (x, y) のタプル (float のままでよい)．
def smooth(prev, new, alpha):
    if prev is None:
        return new
    return ...  # TODO


# ============================================================
# 課題2: 物体を見失ったときの扱い
# ============================================================
# 物体が見つからなかった (new が None の) とき，ボールが中央に飛んで戻ったりしないよう，
# これまでの推定位置 prev をそのまま返せ．prev も None なら None を返す．
# 見つかったときは課題1 の smooth を使う．
def update(prev, new, alpha):
    # TODO

    return smooth(prev, new, alpha)


# ============================================================
# 自動チェック (ここは編集しなくてよい)
# ============================================================
def run_checks():
    got = smooth(None, (10.0, 20.0), 0.5)
    assert got == (10.0, 20.0), "課題1: prev が None のときは new を返すこと"
    got = smooth((0.0, 0.0), (10.0, 20.0), 0.25)
    assert got is not ..., "課題1 がまだ未記入"
    assert np.allclose(got, (2.5, 5.0)), f"課題1: smooth((0, 0), (10, 20), 0.25) は (2.5, 5.0) (今は {got})"
    print("OK 課題1")

    assert update(None, None, 0.5) is None, "課題2: prev も new も None なら None"
    assert update((3.0, 4.0), None, 0.5) == (3.0, 4.0), "課題2: new が None なら prev をそのまま返す"
    assert np.allclose(update((0.0, 0.0), (10.0, 20.0), 0.5), (5.0, 10.0)), "課題2: new があれば smooth を使う"
    print("OK 課題2")


# ============================================================
# カメラで実行
# ============================================================
tb = Trackbars(
    "params",
    {
        "H_min": (0, 179),
        "H_max": (30, 179),
        "S_min": (60, 255),
        "V_min": (60, 255),
        "min_area": (300, 5000),
        "alpha_%": (30, 100),  # smooth の alpha [%]
    },
)

ball = cv2.imread(str(IMAGE_DIR / "ball.png"))
stadium_src = cv2.imread(str(IMAGE_DIR / "stadium.png"))
state = {"pos": None}  # フレームをまたいで覚えておく値は，関数の外に置く


def process(frame):
    h, w = frame.shape[:2]
    stadium = cv2.resize(stadium_src, (w, h))
    fg_h, fg_w = ball.shape[:2]

    mask = hsv_mask(frame, [tb["H_min"], tb["S_min"], tb["V_min"]], [tb["H_max"], 255, 255])
    center = largest_region_center(mask, tb["min_area"])
    state["pos"] = update(state["pos"], center, max(1, tb["alpha_%"]) / 100)

    if state["pos"] is None:
        cx, cy = w // 2, h // 2
    else:
        cx, cy = int(state["pos"][0]), int(state["pos"][1])
    cx, cy = clamp_center(cx, cy, w, h, fg_w, fg_h)

    if center is not None:  # 生の重心 (赤) と なめらかにした位置 (緑) を比べる
        cv2.circle(frame, (int(center[0]), int(center[1])), 6, (0, 0, 255), -1)
    if state["pos"] is not None:
        cv2.circle(frame, (int(state["pos"][0]), int(state["pos"][1])), 6, (0, 255, 0), -1)
    return {"output": paste_center(stadium, ball, cx, cy), "camera": frame, "mask": mask}


if __name__ == "__main__":
    run_checks()
    run(process, show_input=False)


# ============================================================
# [観察] 実際に試して，結果と原因をそれぞれ一文で書け
# ============================================================
# 観察1: alpha_% を 100 → 10 と小さくしていくと，ボールのぶれと「物体を素早く動かしたときの追従」は
#        それぞれどう変わったか．両立できない理由は何か．
#   結果:
#   原因:
#
# 観察2: 物体を一瞬手で隠してから，別の場所で再び見せると，ボールはどう動いたか．
#   結果:
#   原因:
#
# (参考) 「ぶれを抑えつつ遅れも小さくしたい」問題は，第3週の調査テーマ B3 (カルマンフィルタ) で扱う．
