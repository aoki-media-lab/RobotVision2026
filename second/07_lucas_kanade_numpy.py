"""第2週-07: Lucas-Kanade 法を1点だけ numpy で解く (カメラは使わない)

実行方法 (second で):
    uv run python 07_lucas_kanade_numpy.py

解説は second/README.md の「07」を参照．
08 で使う cv2.calcOpticalFlowPyrLK と cv2.goodFeaturesToTrack の中身を，1点だけ自分で計算する．

    明るさは動いても変わらない  I(x + u, y + v, t + 1) = I(x, y, t)
    1次の近似 (テイラー展開)      Ix * u + Iy * v + It = 0
    窓の中の全画素で連立し最小二乗法で解く:

        M = [[Σ Ix*Ix, Σ Ix*Iy],      b = -[Σ Ix*It,
             [Σ Ix*Iy, Σ Iy*Iy]]             Σ Iy*It]      M [u, v]^T = b

この M を「構造テンソル」と呼ぶ．M の固有値を見ると，その点で動きが求まるかどうかが分かる．
"""

import cv2
import numpy as np

# 真の移動量 (課題が終わったら [観察] のために変えてみる)
TRUE_SHIFT = (1.3, -0.7)


def make_images(shift):
    """白い四角を (shift) だけ動かした2枚の画像 (float32) を作る"""
    img = np.full((120, 160), 60, np.float32)
    img[40:90, 50:120] = 200
    img = cv2.GaussianBlur(img, (0, 0), 2.0)
    m = np.float32([[1, 0, shift[0]], [0, 1, shift[1]]])
    img1 = cv2.warpAffine(img, m, (160, 120), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    return img, img1


def gradients(img):
    """x方向・y方向の微分 (Sobel フィルタを 1/8 して「1画素あたりの変化」にそろえる)"""
    ix = cv2.Sobel(img, cv2.CV_32F, 1, 0, ksize=3) / 8
    iy = cv2.Sobel(img, cv2.CV_32F, 0, 1, ksize=3) / 8
    return ix, iy


def window(arr, x, y, r):
    """(x, y) を中心とする (2r+1) x (2r+1) の窓を1次元に並べて返す"""
    return arr[y - r : y + r + 1, x - r : x + r + 1].ravel()


# ============================================================
# 課題1: 構造テンソル M を作る
# ============================================================
# 点 (x, y) の周りの窓の Ix, Iy から，2x2 の行列 M を作って返せ．
#   M = [[Σ Ix*Ix, Σ Ix*Iy],
#        [Σ Ix*Iy, Σ Iy*Iy]]
#   ヒント: ix, iy は1次元配列なので，Σ Ix*Iy は np.sum(ix * iy) (または ix @ iy) で計算できる
def structure_tensor(Ix, Iy, x, y, r):
    ix = window(Ix, x, y, r)
    iy = window(Iy, x, y, r)
    return ...  # TODO: np.array([[..., ...], [..., ...]])


# ============================================================
# 課題2: 1点の動き (u, v) を求める
# ============================================================
# It = I1 - I0 として b = -[Σ Ix*It, Σ Iy*It] を作り，M [u, v]^T = b を解いて (u, v) を返せ．
#   使う関数: np.linalg.solve(M, b)   ← 連立1次方程式を解く
#   M が特異 (逆行列が無い) とき np.linalg.solve はエラーになる．
#   そのときは np.linalg.lstsq(M, b, rcond=None)[0] を使うと「最も小さい解」が得られる．
#   (try: ... except np.linalg.LinAlgError: ... で書くとよい)
def lucas_kanade_point(I0, I1, x, y, r=7):
    Ix, Iy = gradients(I0)
    It = I1 - I0
    M = structure_tensor(Ix, Iy, x, y, r)
    b = ...  # TODO
    # TODO: (u, v) を求めて返す
    return ...


# ============================================================
# 課題3: 固有値で点の種類を判定する (Shi-Tomasi の考え方)
# ============================================================
# M の2つの固有値 λ1 <= λ2 を np.linalg.eigvalsh(M) で求め，次の規則で文字列を返せ．
#     λ1 > th          → "corner" (どの方向に動いても見た目が変わる → 動きが求まる)
#     λ1 <= th < λ2    → "edge"   (辺に沿った方向の動きは見えない)
#     λ2 <= th         → "flat"   (どの方向に動いても見た目が変わらない)
# cv2.goodFeaturesToTrack は，この λ1 (小さいほうの固有値) が大きい点を「追跡しやすい点」として選ぶ．
def classify_point(M, th):
    lam1, lam2 = ...  # TODO
    # TODO: if / elif / else で書く
    return ...


# ============================================================
# 自動チェック (ここは編集しなくてよい)
# ============================================================
POINTS = {"corner": (50, 40), "edge": (85, 40), "flat": (20, 20), "inside": (85, 65)}


def run_checks():
    I0, I1 = make_images((1.3, -0.7))
    Ix, Iy = gradients(I0)

    M = structure_tensor(Ix, Iy, 50, 40, 7)
    assert M is not ..., "課題1 がまだ未記入"
    M = np.asarray(M)
    assert M.shape == (2, 2), f"課題1: M は 2x2 の行列にすること (今は {M.shape})"
    assert np.allclose(M, M.T), "課題1: M は対称行列になるはず"
    ix, iy = window(Ix, 50, 40, 7), window(Iy, 50, 40, 7)
    assert np.isclose(M[0, 0], np.sum(ix * ix)) and np.isclose(M[0, 1], np.sum(ix * iy)), "課題1: M の成分が違う"
    print("OK 課題1")

    uv = lucas_kanade_point(I0, I1, *POINTS["corner"])
    assert uv is not ..., "課題2 がまだ未記入"
    assert np.allclose(uv, (1.3, -0.7), atol=0.2), f"課題2: 角の点で (1.3, -0.7) に近い値が出るはず (今は {uv})"
    uv_edge = lucas_kanade_point(I0, I1, *POINTS["edge"])
    uv_flat = lucas_kanade_point(I0, I1, *POINTS["flat"])
    print("OK 課題2")
    print(f"    角   (corner) の推定: {np.round(uv, 3)}  ← 真値 (1.3, -0.7)")
    print(f"    辺   (edge)   の推定: {np.round(uv_edge, 3)}")
    print(f"    平坦 (flat)   の推定: {np.round(uv_flat, 3)}")

    th = 100.0
    for name, (x, y) in POINTS.items():
        M = structure_tensor(Ix, Iy, x, y, 7)
        got = classify_point(M, th)
        exp = {"corner": "corner", "edge": "edge", "flat": "flat", "inside": "flat"}[name]
        assert got == exp, f"課題3: 点 {name} は {exp} と判定されるはず (今は {got})"
        lam = np.linalg.eigvalsh(M)
        print(f"    {name:7s} λ1 = {lam[0]:9.2f}, λ2 = {lam[1]:9.2f} → {got}")
    print("OK 課題3")

    # OpenCV の cv2.cornerMinEigenVal (goodFeaturesToTrack の中で使われている) と比べる
    cv_min = cv2.cornerMinEigenVal(I0, 15, 3)
    ratios = []
    for x, y in [(50, 40), (119, 40), (50, 89), (119, 89)]:
        mine = np.linalg.eigvalsh(structure_tensor(Ix, Iy, x, y, 7))[0]
        ratios.append(mine / cv_min[y, x])
    print(f"    自分の λ1 / cv2.cornerMinEigenVal = {np.round(ratios, 3)}  (4つの角で同じ比 → 定数倍の違いだけ)")
    assert np.allclose(ratios, ratios[0], rtol=0.02), "λ1 が cv2.cornerMinEigenVal と比例していない"


if __name__ == "__main__":
    run_checks()

    print(f"\n----- TRUE_SHIFT = {TRUE_SHIFT} で試す -----")
    I0, I1 = make_images(TRUE_SHIFT)
    for name, (x, y) in POINTS.items():
        print(f"{name:7s}: 推定 {np.round(lucas_kanade_point(I0, I1, x, y), 3)}")


# ============================================================
# [観察] 結果と原因をそれぞれ一文で書け
# ============================================================
# 観察1: 辺 (edge) の点では，(u, v) のどちらの成分が正しく求まり，どちらが 0 になったか．
#        これを「開口問題」という．なぜ辺の上の点だけを見ても動きが決まらないのか．
#   結果:
#   原因:
#
# 観察2: ファイル先頭の TRUE_SHIFT を (3, -2), (6, -4) と大きくしていくと，角の点の推定はどうなったか．
#        1次の近似 (テイラー展開) が成り立つのはどんなときか．
#        (cv2.calcOpticalFlowPyrLK の maxLevel (画像ピラミッド) はこの問題への対策である)
#   結果:
#   原因:
