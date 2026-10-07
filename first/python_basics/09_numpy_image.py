"""09 画像は numpy 配列

実行方法 (first/python_basics で):
    uv run 09_numpy_image.py

解説は first/README.md の「09 画像は numpy 配列」を参照．
OpenCV で読み込んだ画像は (高さ, 幅, チャンネル) の numpy 配列．チャンネルは B, G, R の順．
各課題の関数の `...` を書き換えて実行すると，ファイル末尾の main で各課題の結果が表示される．
画像の課題はウィンドウに表示される (何かキーを押すと閉じる)．課題文のとおりの結果になっているかを自分で確かめる．
ある課題で詰まったら，main の中のその課題の行をコメントアウトすれば，他の課題を先に進められる．
"""

from pathlib import Path

import cv2
import numpy as np

# ============================================================
# セクション1: 画像の形状と画素
# ============================================================
def task_1_1(img):
    """[課題1-1] img.shape から画像の高さと幅を取り出し，(高さ, 幅) のタプルで返せ"""
    return ...  # TODO


def task_1_2(img):
    """[課題1-2] 左上 (y=0, x=0) の画素の値を返せ．img[y, x] の順であることに注意
    (x, y の順で書く OpenCV の関数と逆なので混乱しやすい)"""
    return ...  # TODO


# ============================================================
# セクション2: 切り出し (スライス)
# ============================================================
def task_2_1(img):
    """[課題2-1] 画像の中心 (cx, cy) を中心とする 200x200 の領域を切り出して返せ
    (上端 cy-100, 下端 cy+100, 左端 cx-100, 右端 cx+100)"""
    h, w = img.shape[:2]
    cy, cx = h // 2, w // 2
    return ...  # TODO


def random_crop(image, size, rng):
    """[課題2-2] 画像からランダムな位置で size x size の領域を切り出して返せ．
    左上の座標 (x0, y0) は，切り出した領域が画像からはみ出さない範囲でランダムに選ぶ．
    rng.integers(0, n) は 0 以上 n 未満の整数を1つ返す"""
    h, w = image.shape[:2]
    y0 = ...  # TODO
    x0 = ...  # TODO
    assert y0 is not ... and x0 is not ..., "課題2-2 がまだ未記入"
    return image[y0 : y0 + size, x0 : x0 + size]


# ============================================================
# セクション3: チャンネルと反転
# ============================================================
def task_3_1(img):
    """[課題3-1] img から R チャンネルだけを取り出して返せ (結果は (高さ, 幅) の2次元配列)"""
    return ...  # TODO


def task_3_2(img):
    """[課題3-2] スライスだけを使って，img を左右反転して返せ (cv2.flip(img, 1) と同じ結果)"""
    return ...  # TODO


def task_3_3(img):
    """[課題3-3] スライスだけを使って，BGR の並びを RGB に入れ替えて返せ"""
    return ...  # TODO


# ============================================================
# セクション4: 自分でグレースケール化
# ============================================================
def task_4_1(img):
    """[課題4-1] グレースケールの値 = 0.299 R + 0.587 G + 0.114 B を numpy の計算だけで求め，
    dtype を np.uint8 にして返せ (cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) との差が 1 以下なら OK)．
    計算途中は小数になるので，最後に np.round してから astype する"""
    return ...  # TODO


# ============================================================
# セクション5: バグ修正
# ============================================================
def task_5_1(img):
    """[バグ修正5-1] 画像を明るくしたくて全画素に 100 を足したが，明るいはずの部分が暗くなってしまった．
    uint8 は 0〜255 しか表せないことがヒント．
    255 を超えた画素は 255 になるように直せ (白い部分は白のまま，暗い部分だけ明るくなる)"""
    return img + 100


if __name__ == "__main__":
    # このファイルの場所から見た画像のパス (どのフォルダから実行しても読み込めるようにする)
    image_dir = Path(__file__).resolve().parent.parent
    img = cv2.imread(str(image_dir / "keio.png"))
    assert img is not None, "画像を読み込めなかった．パスを確認すること"

    print("課題1-1:", task_1_1(img))
    print("課題1-2:", task_1_2(img))

    results = {"original": img}
    results["2-1 crop"] = task_2_1(img)
    rng = np.random.default_rng()
    results["2-2 random crop 1"] = random_crop(img, 300, rng)
    results["2-2 random crop 2"] = random_crop(img, 300, rng)
    results["3-1 R"] = task_3_1(img)
    results["3-2 flip"] = task_3_2(img)
    results["3-3 RGB"] = task_3_3(img)
    results["4-1 gray"] = task_4_1(img)
    results["5-1 bright"] = task_5_1(img)

    for name, result in results.items():
        if isinstance(result, np.ndarray):
            print(f"{name}: shape {result.shape}, dtype {result.dtype}")
            cv2.imshow(name, result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
