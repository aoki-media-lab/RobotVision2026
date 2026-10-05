"""第2週-09: オプティカルフローでボールを動かすアプリ

実行方法 (second で):
    uv run python 09_flow_app.py                  # Webカメラで実行
    uv run python 09_flow_app.py --video 動画.mp4  # 動画ファイルで実行

解説は second/README.md の「09」を参照．
画面の中の動きの向きに合わせて，スタジアムのボールを上下左右に動かす．
たくさんの点の動きから「全体としてどちらに動いたか」を1つ決める方法を3つ比べる．

キー操作: q 終了 / r 録画開始・停止 / v カメラ⇔録画の切り替え / スペース 一時停止
"""

from pathlib import Path

import cv2
import numpy as np

from common import Trackbars, run

IMAGE_DIR = Path(__file__).resolve().parent / "image_data"
METHODS = ["max", "sum", "median"]


# ============================================================
# 課題1: たくさんの点の動きを1つのベクトルにまとめる
# ============================================================
# good0, good1: 追跡に成功した点の前の位置・今の位置 (それぞれ (N, 2) の配列)
# method に応じて，全体の動き (dx, dy) を float のタプルで返せ．点が無ければ (0.0, 0.0)．
#   "max"   : 移動量 (ベクトルの長さ) が最大の点の (dx, dy)   ← 昨年度の Version1 に近い
#   "sum"   : 全点の (dx, dy) の合計                       ← 昨年度の Version2
#   "median": 全点の dx の中央値，dy の中央値
#   ヒント: d = good1 - good0 で全点の (dx, dy) が (N, 2) の配列で求まる．
#           長さは np.linalg.norm(d, axis=1)，最大の添字は np.argmax，中央値は np.median(d, axis=0)
def motion_vector(good0, good1, method):
    if len(good0) == 0:
        return 0.0, 0.0
    d = good1 - good0
    # TODO

    return ...


# ============================================================
# 課題2: 動きの向きを決める
# ============================================================
# (dx, dy) の大きいほうの成分の絶対値が threshold 以上なら，その向きを返せ．
# 向きは "left", "right", "up", "down" のどれか．threshold 未満なら None．
# 画像の y 座標は下向きが正であることに注意．
def direction(dx, dy, threshold):
    # TODO

    return None


# ============================================================
# 自動チェック (ここは編集しなくてよい)
# ============================================================
def run_checks():
    g0 = np.zeros((5, 2), np.float32)
    g1 = np.float32([[2, 0], [3, 0], [2, 1], [2, 0], [-40, 30]])  # 最後の1点だけ大きく外れている
    exp = {"max": (-40, 30), "sum": (-31, 31), "median": (2, 0)}
    for m in METHODS:
        got = motion_vector(g0, g1, m)
        assert got is not ..., "課題1 がまだ未記入"
        assert np.allclose(got, exp[m]), f'課題1: method="{m}" は {exp[m]} (今は {got})'
    assert motion_vector(np.empty((0, 2)), np.empty((0, 2)), "median") == (0.0, 0.0)
    print("OK 課題1")

    cases = [((5, 1), "right"), ((-5, 1), "left"), ((1, 5), "down"), ((1, -5), "up"), ((1, 2), None)]
    for (dx, dy), e in cases:
        got = direction(dx, dy, 3)
        assert got == e, f"課題2: direction({dx}, {dy}, 3) は {e!r} (今は {got!r})"
    print("OK 課題2")


# ============================================================
# カメラで実行 (08 の追跡部分は完成済み)
# ============================================================
tb = Trackbars(
    "params",
    {
        "method": (2, 2),  # 0: max, 1: sum, 2: median
        "threshold": (5, 100),  # 動いたとみなす移動量 [px/フレーム]
        "step": (15, 50),  # ボールを1回に動かす量 [px]
    },
)
ball = cv2.imread(str(IMAGE_DIR / "ball.png"))
stadium_src = cv2.imread(str(IMAGE_DIR / "stadium.png"))
state = {"prev_gray": None, "points": None, "frame_idx": 0, "ball": None}


def track(gray):
    """08 と同じ追跡 (10 フレームごとに点を検出し直す)"""
    good0 = good1 = np.empty((0, 2), np.float32)
    p0 = state["points"]
    if p0 is not None and len(p0) > 0:
        p1, st, _ = cv2.calcOpticalFlowPyrLK(state["prev_gray"], gray, p0, None, winSize=(15, 15), maxLevel=2)
        if p1 is not None:
            ok = st.ravel() == 1
            good0, good1 = p0.reshape(-1, 2)[ok], p1.reshape(-1, 2)[ok]
    state["frame_idx"] += 1
    if len(good1) < 10 or state["frame_idx"] % 10 == 0:
        state["points"] = cv2.goodFeaturesToTrack(gray, maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)
    else:
        state["points"] = good1.reshape(-1, 1, 2)
    state["prev_gray"] = gray
    return good0, good1


def process(frame):
    h, w = frame.shape[:2]
    stadium = cv2.resize(stadium_src, (w, h))
    bh, bw = ball.shape[:2]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if state["prev_gray"] is None or state["prev_gray"].shape != gray.shape:
        state.update(prev_gray=gray, points=None, ball=[w // 2, h // 2])

    good0, good1 = track(gray)
    method = METHODS[min(tb["method"], 2)]
    dx, dy = motion_vector(good0, good1, method)
    d = direction(dx, dy, max(1, tb["threshold"]))

    step = tb["step"]
    moves = {"left": (-step, 0), "right": (step, 0), "up": (0, -step), "down": (0, step)}
    if d is not None:
        state["ball"][0] += moves[d][0]
        state["ball"][1] += moves[d][1]
    # はみ出さないように制限
    state["ball"][0] = max(bw // 2, min(state["ball"][0], w - (bw - bw // 2)))
    state["ball"][1] = max(bh // 2, min(state["ball"][1], h - (bh - bh // 2)))

    cx, cy = state["ball"]
    out = stadium.copy()
    out[cy - bh // 2 : cy - bh // 2 + bh, cx - bw // 2 : cx - bw // 2 + bw] = ball

    for p, q in zip(good0, good1):
        cv2.line(frame, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), (0, 255, 0), 2)
    c = (w // 2, h // 2)
    cv2.arrowedLine(frame, c, (int(c[0] + 5 * dx), int(c[1] + 5 * dy)), (0, 0, 255), 3)
    cv2.putText(frame, f"{method}: ({dx:+.1f}, {dy:+.1f}) -> {d}", (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    return {"output": out, "flow": frame}


if __name__ == "__main__":
    run_checks()
    run(process, show_input=False)


# ============================================================
# [観察] 実際に試して，結果と原因をそれぞれ一文で書け
# ============================================================
# 観察1: method を max / sum / median と切り替えて同じ動作 (手を左右に振る) をすると，
#        誤ってボールが動くことが多いのはどれか．自動チェックのテストデータと関係づけて説明せよ．
#   結果:
#   原因:
#
# 観察2: sum の threshold を，画面に映る物の多い場所と少ない場所 (白い壁) で同じ値にしてよいか．
#   結果:
#   原因:
#
# 観察3: threshold の単位は [px/フレーム] である．FPS が半分になると，同じ速さの手の動きに対して
#        dx, dy はどうなるか．FPS が変わってもアプリの操作感を変えないにはどうすればよいか．
#   結果:
#   原因:
