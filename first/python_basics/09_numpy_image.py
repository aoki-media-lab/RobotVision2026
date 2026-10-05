"""09 画像は numpy 配列

実行方法 (first/python_basics で):
    uv run python 09_numpy_image.py

解説は first/README.md の「09 画像は numpy 配列」を参照．
OpenCV で読み込んだ画像は (高さ, 幅, チャンネル) の numpy 配列．チャンネルは B, G, R の順．
`...` の部分を書き換えて，各セクション末尾の自動チェックがすべて OK になれば完了．
最後まで OK になると，作った画像がウィンドウに表示される (何かキーを押すと閉じる)．
"""

from pathlib import Path

import cv2
import numpy as np

# このファイルの場所から見た画像のパス (どのフォルダから実行しても読み込めるようにする)
IMAGE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# 自動チェック用の関数 (ここは編集しなくてよい)
# ============================================================
def check(name, actual, expected, atol=0):
    assert actual is not ..., f"課題{name} がまだ未記入"
    if isinstance(expected, np.ndarray):
        assert isinstance(actual, np.ndarray), f"課題{name} は numpy 配列にすること"
        assert actual.shape == expected.shape, (
            f"課題{name} の形状が違う: 期待 {expected.shape} / 実際 {actual.shape}"
        )
        diff = np.abs(actual.astype(int) - expected.astype(int)).max()
        assert diff <= atol, f"課題{name} が不正解 (最大の差: {diff})"
    else:
        assert actual == expected, f"課題{name} が不正解: 期待 {expected!r} / 実際 {actual!r}"
    print(f"OK 課題{name}")


# ============================================================
# セクション1: 画像の読み込みと形状
# ============================================================
img = cv2.imread(str(IMAGE_DIR / "keio.png"))
# 読み込みに失敗すると None が返る (パスの間違いが多い)
assert img is not None, "画像を読み込めなかった．パスを確認すること"
print("shape:", img.shape, "dtype:", img.dtype)

# [課題1-1] img.shape から画像の高さと幅を取り出し，(高さ, 幅) のタプルにせよ
# 期待する出力: (630, 1200)
ans_1_1 = ...  # TODO
print(ans_1_1)
check("1-1", ans_1_1, (630, 1200))

# [課題1-2] 左上 (y=0, x=0) の画素の値を取り出せ．img[y, x] の順であることに注意
#   (x, y の順で書く OpenCV の関数と逆なので混乱しやすい)
ans_1_2 = ...  # TODO
print("左上の画素 (B, G, R):", ans_1_2)
check("1-2", ans_1_2, img[0, 0].copy())


# ============================================================
# セクション2: 切り出し (スライス)
# ============================================================
h, w = img.shape[:2]
cy, cx = h // 2, w // 2

# [課題2-1] 画像の中心 (cx, cy) を中心とする 200x200 の領域を切り出せ
#   (上端 cy-100, 下端 cy+100, 左端 cx-100, 右端 cx+100)
ans_2_1 = ...  # TODO
print("切り出した画像の shape:", None if ans_2_1 is ... else ans_2_1.shape)
check("2-1", ans_2_1, img[cy - 100 : cy + 100, cx - 100 : cx + 100])


# [課題2-2] 画像からランダムな位置で size x size の領域を切り出す関数を完成させよ
#   左上の座標 (x0, y0) は，切り出した領域が画像からはみ出さない範囲でランダムに選ぶ
#   ヒント: rng.integers(0, n) は 0 以上 n 未満の整数を1つ返す
def random_crop(image, size, rng):
    h, w = image.shape[:2]
    y0 = ...  # TODO
    x0 = ...  # TODO
    assert y0 is not ... and x0 is not ..., "課題2-2 がまだ未記入"  # この行は消さない
    return image[y0 : y0 + size, x0 : x0 + size]


rng = np.random.default_rng(0)
crops = [random_crop(img, 300, rng) for _ in range(20)]
for c in crops:
    check("2-2 (大きさ)", c.shape, (300, 300, 3))
print("ランダムに切り出した画像は", len({c.tobytes() for c in crops}), "種類")
assert len({c.tobytes() for c in crops}) > 1, "課題2-2: 毎回同じ場所が切り出されている"


# ============================================================
# セクション3: チャンネルと反転
# ============================================================
# [課題3-1] img から R チャンネルだけを取り出せ (結果は (高さ, 幅) の2次元配列)
ans_3_1 = ...  # TODO
check("3-1", ans_3_1, cv2.split(img)[2])

# [課題3-2] スライスだけを使って，img を左右反転せよ (cv2.flip(img, 1) と同じ結果)
ans_3_2 = ...  # TODO
check("3-2", ans_3_2, cv2.flip(img, 1))

# [課題3-3] スライスだけを使って，BGR の並びを RGB に入れ替えよ
ans_3_3 = ...  # TODO
check("3-3", ans_3_3, cv2.cvtColor(img, cv2.COLOR_BGR2RGB))


# ============================================================
# セクション4: 自分でグレースケール化
# ============================================================
# グレースケールの値 = 0.299 R + 0.587 G + 0.114 B
# [課題4-1] numpy の計算だけでグレースケール画像を作り，dtype を np.uint8 にせよ
#   (cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) との差が 1 以下なら OK)
#   ヒント: img[:, :, 0] が B．計算途中は小数になるので，最後に np.round してから astype する
ans_4_1 = ...  # TODO
check("4-1", ans_4_1, cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), atol=1)


# ============================================================
# セクション5: バグ修正
# ============================================================
# [バグ修正5-1] 画像を明るくしたくて全画素に 100 を足したが，明るいはずの部分が暗くなってしまった．
#   uint8 は 0〜255 しか表せないことがヒント．
#   255 を超えた画素は 255 になるように直せ (cv2.add(img, 100) と同じ結果になればよい)
# 期待する結果: 白い部分は白のまま，暗い部分だけ明るくなる
ans_5_1 = img + 100
check("5-1", ans_5_1, cv2.add(img, np.full_like(img, 100)))

print("\nすべて OK!")

# 結果を表示 (何かキーを押すと閉じる)
cv2.imshow("original", img)
cv2.imshow("crop", ans_2_1)
cv2.imshow("flip", ans_3_2)
cv2.imshow("gray", ans_4_1)
cv2.imshow("bright", ans_5_1)
cv2.waitKey(0)
cv2.destroyAllWindows()
