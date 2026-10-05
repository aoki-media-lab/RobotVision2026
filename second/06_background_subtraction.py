"""第2週-06: 背景差分 — 自分で作る方法と OpenCV の方法を比べる

実行方法 (second で):
    uv run python 06_background_subtraction.py                  # Webカメラで実行
    uv run python 06_background_subtraction.py --video 動画.mp4  # 動画ファイルで実行
    uv run python 06_background_subtraction.py --video image_data/opticalflow.avi

解説は second/README.md の「06」を参照．
色を使わずに「動いているもの」を取り出す方法を4つ並べて比べる．
    (a) 静的背景差分 : 最初に撮った背景画像との差 (b キーで背景を撮り直す)
    (b) フレーム間差分: 1つ前のフレームとの差
    (c) 移動平均背景 : 背景を少しずつ更新しながら，その背景との差
    (d) MOG          : OpenCV の背景差分 (画素ごとに背景の色の分布を学習する)

キー操作: q 終了 / r 録画開始・停止 / v カメラ⇔録画の切り替え / スペース 一時停止 / b 背景を撮り直す
"""

import cv2
import numpy as np

from common import Trackbars, run, tile


# ============================================================
# 課題1: バグ修正 — 2枚の画像の差
# ============================================================
# グレースケール画像 a と b の差の絶対値が th より大きい画素を 255，それ以外を 0 にしたマスクを返したい．
# しかし，少し明るくなった画素は正しく無視されるのに，少し暗くなっただけの画素
# (照明のちらつき程度の変化) は前景として検出されてしまう．
# a, b の dtype が uint8 であることがヒント (第1週 09 のバグ修正5-1 を思い出す)．直せ．
def diff_mask(a, b, th):
    diff = np.abs(a - b)
    return np.where(diff > th, 255, 0).astype(np.uint8)


# ============================================================
# 課題2: 移動平均で背景を更新する
# ============================================================
# 背景 bg (float32 の配列) を，現在のフレーム gray を使って次のように更新した配列を返せ．
#     新しい背景 = (1 - alpha) * bg + alpha * gray
# alpha が大きいほど背景がすぐに新しいフレームに置き換わる．
# 戻り値の dtype は float32 にすること (uint8 にすると小さな変化が切り捨てられて更新されない)．
def update_background(bg, gray, alpha):
    return ...  # TODO


# ============================================================
# 課題3: バグ修正 — MOG が何も検出しない
# ============================================================
# MOG は「これまでに見たフレーム」から背景を学習する．
# 次の関数は毎フレーム呼ばれるが，何が動いても前景が検出されない．原因を考えて直せ．
#   ヒント: 背景差分器 (BackgroundSubtractor) は，いつ作られて，いつ捨てられているか．
def mog_mask(frame):
    subtractor = cv2.bgsegm.createBackgroundSubtractorMOG()
    return subtractor.apply(frame)


# ============================================================
# 自動チェック (ここは編集しなくてよい)
# ============================================================
def run_checks():
    bg = np.full((10, 10), 200, np.uint8)
    cur = bg.copy()
    cur[0, 0] = 50  # 暗い物体 (差 150)
    cur[0, 1] = 250  # 明るい物体 (差 50)
    cur[0, 2] = 190  # 少し暗くなっただけ (差 10)
    cur[0, 3] = 210  # 少し明るくなっただけ (差 10)
    m = diff_mask(cur, bg, 30)
    assert m[0, 0] == 255 and m[0, 1] == 255, "課題1: 物体が検出されていない"
    assert m[0, 3] == 0 and m[5, 5] == 0, "課題1: 変化の小さい画素まで検出されている"
    assert m[0, 2] == 0, "課題1: 少し暗くなっただけの画素が検出されている (190 - 200 は uint8 でいくつになる?)"
    print("OK 課題1")

    bg = np.zeros((4, 4), np.float32)
    gray = np.full((4, 4), 100, np.uint8)
    new = update_background(bg, gray, 0.1)
    assert new is not ..., "課題2 がまだ未記入"
    assert new.dtype == np.float32, f"課題2: dtype は float32 にすること (今は {new.dtype})"
    assert np.allclose(new, 10.0), f"課題2: (1 - 0.1) * 0 + 0.1 * 100 = 10 になるはず (今は {new[0, 0]})"
    print("OK 課題2")

    rng = np.random.default_rng(0)
    still = rng.integers(60, 120, (60, 80, 3), dtype=np.uint8)
    for t in range(10):
        f = still.copy()
        f[20:40, 5 + 3 * t : 25 + 3 * t] = (0, 0, 255)  # 動く赤い四角
        m = mog_mask(f)
    assert (m > 0).sum() > 100, "課題3: 動いている四角が前景として検出されていない"
    assert m[:15].max() == 0, "課題3: 動いていない部分まで前景になっている"
    print("OK 課題3")


# ============================================================
# カメラで実行
# ============================================================
tb = Trackbars(
    "params",
    {
        "threshold": (30, 255),  # (a)(b)(c) の差の閾値
        "alpha_%": (5, 100),  # (c) の更新の速さ [%]
    },
)
state = {"static_bg": None, "prev": None, "avg_bg": None}


def on_key(key):
    if key == "b":
        state["static_bg"] = None  # 次のフレームを背景として撮り直す
        print("背景を撮り直した")


def process(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    th = tb["threshold"]

    if state["static_bg"] is None:
        state["static_bg"] = gray
    if state["prev"] is None:
        state["prev"] = gray
    if state["avg_bg"] is None:
        state["avg_bg"] = gray.astype(np.float32)

    m_static = diff_mask(gray, state["static_bg"], th)
    m_frame = diff_mask(gray, state["prev"], th)
    m_avg = diff_mask(gray, state["avg_bg"].astype(np.uint8), th)
    m_mog = mog_mask(frame)

    state["prev"] = gray
    state["avg_bg"] = update_background(state["avg_bg"], gray, tb["alpha_%"] / 100)

    return tile(
        [frame, m_static, m_frame, m_avg, m_mog, state["avg_bg"]],
        cols=3,
        labels=["input", "(a) static", "(b) frame diff", "(c) running avg", "(d) MOG", "(c) background"],
        width=320,
    )


if __name__ == "__main__":
    run_checks()
    run(process, on_key=on_key)


# ============================================================
# [観察] 実際に試して，結果と原因をそれぞれ一文で書け
# ============================================================
# 観察1: カメラの前で手をゆっくり動かしたときと，素早く動かしたとき，
#        (b) フレーム間差分では手のどの部分が検出されたか．手の内側が抜けるのはなぜか．
#   結果:
#   原因:
#
# 観察2: 画面に入ってきた人(物)がしばらく静止すると，(a)(c)(d) はそれぞれどうなったか．
#        alpha_% を変えると (c) はどう変わったか．
#   結果:
#   原因:
#
# 観察3: 部屋の照明を点けたり消したりすると，4つの方法はそれぞれどうなったか．
#   結果:
#   原因:
#
# 観察4: カメラを手で持って揺らすと，4つの方法はそれぞれどうなったか．
#        背景差分を「動いているもの」の検出に使えるのは，どういう条件のときか．
#   結果:
#   原因:
