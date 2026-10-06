"""第2週 発展課題: numpy だけで Harris コーナー検出を作る

実行方法 (second/advanced で):
    uv run harris_numpy.py

各画素の周りの窓で，画像の x 方向・y 方向の微分 Ix, Iy から次の行列 (構造テンソル) を作り，
    M = [[Σ Ix*Ix, Σ Ix*Iy],
         [Σ Ix*Iy, Σ Iy*Iy]]
Harris の応答
    R = det(M) - k * trace(M)^2
を全画素について求める．R が大きい点がコーナー．
cv2 の関数は画像の読み込み・表示と，答え合わせの cv2.cornerHarris 以外は使わないこと．

手順:
    1. Sobel フィルタ (3x3) を numpy で実装し，Ix, Iy を求める
         x方向: [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]，y方向はその転置
         (erode_numpy.py と同じく「画像をずらしたもの」の重み付き和で書ける)
    2. Ixx = Ix*Ix, Iyy = Iy*Iy, Ixy = Ix*Iy を block x block の窓で足し合わせる (箱フィルタ)
    3. R = (Sxx * Syy - Sxy^2) - k * (Sxx + Syy)^2
実行すると cv2.cornerHarris との相関係数を表示する (1 に近ければ同じ形．定数倍や端の扱いの違いは気にしなくてよい)．
"""

import cv2
import numpy as np


def shift_sum(img, kernel):
    """img に 3x3 などの kernel を畳み込んだ結果を返す (端は edge で延長)"""
    ...  # TODO


def sobel(img):
    """(Ix, Iy) を返す"""
    ...  # TODO


def box_sum(img, block):
    """block x block の窓の中の和を返す"""
    ...  # TODO


def harris(img, block=3, k=0.04):
    ...  # TODO


def make_test_image():
    img = np.zeros((200, 260), np.float32)
    img[40:100, 40:120] = 1.0  # 四角
    pts = np.array([[160, 40], [230, 70], [200, 160]], np.int32)
    cv2.fillPoly(img, [pts], 0.7)  # 三角形
    for y in range(120, 180, 20):  # 市松模様
        for x in range(30, 130, 20):
            if (x // 20 + y // 20) % 2 == 0:
                img[y : y + 20, x : x + 20] = 0.5
    return img


if __name__ == "__main__":
    img = make_test_image()
    mine = harris(img)
    assert mine is not None, "まだ未記入"
    ref = cv2.cornerHarris(img, 3, 3, 0.04)
    inner = (slice(5, -5), slice(5, -5))
    corr = np.corrcoef(mine[inner].ravel(), ref[inner].ravel())[0, 1]
    print(f"cv2.cornerHarris との相関係数: {corr:.4f}")

    vis = cv2.cvtColor((img * 255).astype(np.uint8), cv2.COLOR_GRAY2BGR)
    vis[mine > 0.01 * mine.max()] = (0, 0, 255)
    cv2.imshow("harris (red: R > 1% of max)", cv2.resize(vis, None, fx=2, fy=2, interpolation=cv2.INTER_NEAREST))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 考察1: R の値は「辺」の上で正・負・0 のどれになったか．det と trace の式から説明せよ．
# 考察2: Shi-Tomasi (M の小さいほうの固有値) と Harris (R) は，どちらも M から計算する．
#        固有値を直接計算しない Harris の式には，どんな利点があったと考えられるか．
# 考察3: 画像を 45 度回転させても同じ点がコーナーとして検出されるか試せ．画像を2倍に拡大したら?
#        (拡大・縮小への強さは調査テーマ A4 で扱う)
