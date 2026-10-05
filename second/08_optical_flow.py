"""第2週-08: OpenCV のオプティカルフロー (特徴点の追跡)

実行方法 (second で):
    uv run python 08_optical_flow.py                  # Webカメラで実行
    uv run python 08_optical_flow.py --video image_data/opticalflow.avi

解説は second/README.md の「08」を参照．
07 で1点だけ解いた Lucas-Kanade 法を，OpenCV で多数の点について行う．
    cv2.goodFeaturesToTrack : 追跡しやすい点 (構造テンソルの小さいほうの固有値が大きい点) を選ぶ
    cv2.calcOpticalFlowPyrLK: 各点が次のフレームでどこに移ったかを求める

昨年度のコードには「追跡に失敗した点を捨て続けるので，いずれ点が無くなる」
「点が無くなるとエラーで止まる」という問題があった．ここではそれを直す．

キー操作: q 終了 / r 録画開始・停止 / v カメラ⇔録画の切り替え / スペース 一時停止
"""

import cv2
import numpy as np

from common import Trackbars, run

COLORS = np.random.default_rng(0).integers(0, 255, (500, 3))


# ============================================================
# 課題1: 追跡に成功した点だけを取り出す
# ============================================================
# p0: 前のフレームの点 (N, 1, 2)，p1: 次のフレームでの位置 (N, 1, 2) または None，
# status: 各点の追跡に成功したら 1，失敗したら 0 の配列 (N, 1) または None．
# 追跡に成功した点だけを取り出し，(good0, good1) を返せ．それぞれ (M, 2) の配列．
# p1 が None のとき (追跡する点が1つも無かったときなど) は，
# 形が (0, 2) の空の配列を2つ返すこと (np.empty((0, 2), np.float32))．
#   ヒント: 第1週 08 の bool 配列による取り出し．status.ravel() == 1 で (N,) の bool 配列になる
def select_good(p0, p1, status):
    # TODO

    return ...


# ============================================================
# 課題2: 点を検出し直すかどうか
# ============================================================
# 次のどちらかなら True を返せ．
#   - 残っている点の数 n_points が min_points 未満
#   - フレーム番号 frame_idx が interval の倍数 (interval フレームごとに検出し直す)
def need_redetect(n_points, frame_idx, min_points, interval):
    return ...  # TODO


# ============================================================
# 課題3: バグ修正 — 動きを描く
# ============================================================
# 各点について，前の位置から今の位置へ線を引き，今の位置に円を描く．
# OpenCV 5 では cv2.line や cv2.circle に小数の座標を渡すとエラーになる．直せ．
def draw_flow(canvas, frame, good0, good1):
    for i, (p, q) in enumerate(zip(good0, good1)):
        color = COLORS[i % len(COLORS)].tolist()
        canvas = cv2.line(canvas, (p[0], p[1]), (q[0], q[1]), color, 2)
        frame = cv2.circle(frame, (q[0], q[1]), 4, color, -1)
    return canvas, frame


# ============================================================
# 自動チェック (ここは編集しなくてよい)
# ============================================================
def run_checks():
    p0 = np.float32([[[1, 2]], [[3, 4]], [[5, 6]]])
    p1 = p0 + 1
    status = np.uint8([[1], [0], [1]])
    result = select_good(p0, p1, status)
    assert result is not ..., "課題1 がまだ未記入"
    g0, g1 = result
    assert g0.shape == (2, 2) and np.allclose(g0, [[1, 2], [5, 6]]), f"課題1: good0 が違う\n{g0}"
    assert np.allclose(g1, [[2, 3], [6, 7]]), f"課題1: good1 が違う\n{g1}"
    g0, g1 = select_good(np.empty((0, 1, 2), np.float32), None, None)
    assert g0.shape == (0, 2) and g1.shape == (0, 2), "課題1: p1 が None のときは (0, 2) の空の配列を返すこと"
    print("OK 課題1")

    assert need_redetect(3, 7, 10, 30) is True, "課題2: 点が少なければ True"
    assert need_redetect(50, 60, 10, 30) is True, "課題2: interval の倍数のフレームなら True"
    assert need_redetect(50, 61, 10, 30) is False, "課題2: それ以外は False"
    print("OK 課題2")

    canvas = np.zeros((50, 50, 3), np.uint8)
    canvas, frame = draw_flow(canvas, canvas.copy(), np.float32([[10.4, 10.6]]), np.float32([[30.2, 20.7]]))
    assert canvas.max() > 0 and frame.max() > 0, "課題3: 線や円が描かれていない"
    print("OK 課題3")

    # 合成画像で，全体が (3, 2) 動いたときに正しく追跡できるか
    rng = np.random.default_rng(1)
    img = cv2.GaussianBlur(rng.integers(0, 256, (240, 320), dtype=np.uint8), (0, 0), 3)
    img1 = cv2.warpAffine(img, np.float32([[1, 0, 3], [0, 1, 2]]), (320, 240), borderMode=cv2.BORDER_REFLECT)
    pts = cv2.goodFeaturesToTrack(img, maxCorners=100, qualityLevel=0.01, minDistance=7)
    nxt, st, _ = cv2.calcOpticalFlowPyrLK(img, img1, pts, None)
    g0, g1 = select_good(pts, nxt, st)
    med = np.median(g1 - g0, axis=0)
    print(f"    合成画像: {len(g0)} 点を追跡，移動量の中央値 {np.round(med, 2)} (真値 [3, 2])")
    assert np.allclose(med, (3, 2), atol=0.3)


# ============================================================
# カメラで実行
# ============================================================
tb = Trackbars(
    "params",
    {
        "maxCorners": (100, 500),
        "quality_%": (10, 100),  # qualityLevel [%]
        "winSize": (15, 51),
        "maxLevel": (2, 5),  # 画像ピラミッドの段数
        "interval": (30, 300),  # 何フレームごとに点を検出し直すか (0 なら点が減ったときだけ)
    },
)
state = {"prev_gray": None, "points": None, "canvas": None, "frame_idx": 0}


def detect(gray):
    return cv2.goodFeaturesToTrack(
        gray,
        maxCorners=max(1, tb["maxCorners"]),
        qualityLevel=max(1, tb["quality_%"]) / 100,
        minDistance=7,
        blockSize=7,
    )


def process(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if state["prev_gray"] is None or state["prev_gray"].shape != gray.shape:
        state.update(prev_gray=gray, points=detect(gray), canvas=np.zeros_like(frame), frame_idx=0)
        return frame

    p0 = state["points"]
    if p0 is None or len(p0) == 0:
        p1, status = None, None
    else:
        win = max(3, tb["winSize"])
        p1, status, _ = cv2.calcOpticalFlowPyrLK(
            state["prev_gray"], gray, p0, None, winSize=(win, win), maxLevel=tb["maxLevel"]
        )
    good0, good1 = select_good(p0, p1, status)

    # 線は時間とともに薄くする (残像)
    state["canvas"] = (state["canvas"] * 0.9).astype(np.uint8)
    state["canvas"], frame = draw_flow(state["canvas"], frame, good0, good1)

    state["frame_idx"] += 1
    interval = tb["interval"] if tb["interval"] > 0 else 10**9
    if need_redetect(len(good1), state["frame_idx"], 10, interval):
        state["points"] = detect(gray)
    else:
        state["points"] = good1.reshape(-1, 1, 2)
    state["prev_gray"] = gray

    out = cv2.add(frame, state["canvas"])
    cv2.putText(out, f"points: {len(good1)}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    return out


if __name__ == "__main__":
    run_checks()
    run(process)


# ============================================================
# [観察] 実際に試して，結果と原因をそれぞれ一文で書け
# ============================================================
# 観察1: 白い壁や無地の机をカメラに映すと，点はどこに検出されたか．07 の固有値と関係づけて説明せよ．
#   結果:
#   原因:
#
# 観察2: maxLevel を 0 にして手を素早く動かすと，追跡はどうなったか．maxLevel を 3 にすると?
#   結果:
#   原因:
#
# 観察3: カメラ自体を揺らすと，フローはどうなったか．「物体の動き」だけを取り出すには何が必要か．
#   結果:
#   原因:
