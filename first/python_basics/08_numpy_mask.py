"""08 numpy の比較とマスク

実行方法 (first/python_basics で):
    uv run python 08_numpy_mask.py

解説は first/README.md の「08 numpy の比較とマスク」を参照．
画像処理の「マスク(どの画素を使うかを表す白黒画像)」は，ここで扱う bool 配列そのもの．
`...` の部分を書き換えて，各セクション末尾の自動チェックがすべて OK になれば完了．
"""

import numpy as np


# ============================================================
# 自動チェック用の関数 (ここは編集しなくてよい)
# ============================================================
def check(name, actual, expected):
    assert actual is not ..., f"課題{name} がまだ未記入"
    if isinstance(expected, np.ndarray):
        assert isinstance(actual, np.ndarray), f"課題{name} は numpy 配列にすること"
        assert actual.shape == expected.shape, (
            f"課題{name} の形状が違う: 期待 {expected.shape} / 実際 {actual.shape}"
        )
        assert actual.dtype == expected.dtype, (
            f"課題{name} の dtype が違う: 期待 {expected.dtype} / 実際 {actual.dtype}"
        )
        assert np.array_equal(actual, expected), (
            f"課題{name} が不正解:\n期待\n{expected}\n実際\n{actual}"
        )
    else:
        assert actual == expected, f"課題{name} が不正解: 期待 {expected!r} / 実際 {actual!r}"
    print(f"OK 課題{name}")


# ============================================================
# セクション1: 比較すると bool 配列になる
# ============================================================
arr = np.array([3, 8, 1, 9, 5])
print(arr > 4)  # 要素ごとに比較される
print(arr == 8)

# [課題1-1] arr の要素が 4 より大きいかどうかを表す bool 配列を作れ
# 期待する出力: [False  True False  True  True]
mask = ...  # TODO
print(mask)
check("1-1", mask, np.array([False, True, False, True, True]))

# [課題1-2] mask の True の個数を数えよ (True は 1，False は 0 として足し算できる)
# 期待する出力: 3
ans_1_2 = ...  # TODO
print(ans_1_2)
check("1-2", ans_1_2, 3)

# [課題1-3] mask を添字に使って，arr から 4 より大きい要素だけを取り出せ
# 期待する出力: [8 9 5]
ans_1_3 = ...  # TODO
print(ans_1_3)
check("1-3", ans_1_3, np.array([8, 9, 5]))


# ============================================================
# セクション2: 範囲の条件 (& と |)
# ============================================================
# 条件を組み合わせるときは and / or ではなく & / | を使い，各条件を () で囲む
#   (lower <= arr) & (arr <= upper)  ← cv2.inRange がやっていることと同じ
hue = np.array([5, 20, 35, 90, 110, 175])

# [課題2-1] hue が 10 以上 40 以下の要素を True とする bool 配列を作れ
# 期待する出力: [False  True  True False False False]
ans_2_1 = ...  # TODO
print(ans_2_1)
check("2-1", ans_2_1, np.array([False, True, True, False, False, False]))

# [課題2-2] 赤色の Hue は 0 付近と 179 付近の両端にまたがる．
#   hue が 10 未満 または 170 より大きい要素を True とする bool 配列を作れ
# 期待する出力: [ True False False False False  True]
ans_2_2 = ...  # TODO
print(ans_2_2)
check("2-2", ans_2_2, np.array([True, False, False, False, False, True]))


# ============================================================
# セクション3: np.where で値を置き換える (二値化)
# ============================================================
# np.where(条件, 真のときの値, 偽のときの値)
gray = np.array([[10, 200, 130], [90, 250, 40]], dtype=np.uint8)
print(np.where(gray > 100, 1, 0))

# [課題3-1] gray を「128 以上なら 255，それ以外は 0」に二値化せよ．
#   画像として扱えるよう，dtype は np.uint8 にすること (.astype(np.uint8))
# 期待する出力:
#   [[  0 255 255]
#    [  0 255   0]]
ans_3_1 = ...  # TODO
print(ans_3_1)
check("3-1", ans_3_1, np.array([[0, 255, 255], [0, 255, 0]], dtype=np.uint8))


# ============================================================
# セクション4: 白い領域を囲む四角形 (np.where で座標を取り出す)
# ============================================================
# np.where(条件) と引数を1つだけにすると，条件を満たす要素の「添字」が返る
# 2次元配列なら (行の添字の配列, 列の添字の配列) のタプル
binary = np.zeros((6, 8), dtype=np.uint8)
binary[2:5, 3:7] = 255  # 2〜4 行目，3〜6 列目 が白
print(binary)
ys, xs = np.where(binary == 255)
print("ys:", ys)
print("xs:", xs)

# [課題4-1] ys, xs から，白い領域を囲む四角形の (左, 上, 右, 下) を求めよ
# 期待する出力: (3, 2, 6, 4)
ans_4_1 = ...  # TODO
print(ans_4_1)
check("4-1", tuple(int(v) for v in ans_4_1) if ans_4_1 is not ... else ..., (3, 2, 6, 4))


# ============================================================
# セクション5: バグ修正
# ============================================================
# [バグ修正5-1] 「arr に 4 より大きい要素が1つでもあれば」と書きたいが，エラーになる．
#   エラーメッセージが勧めている方法のどちらを使えばよいか考えて直せ
# 期待する出力: 大きい値がある
if arr > 4:
    ans_5_1 = "大きい値がある"
else:
    ans_5_1 = "ない"
print(ans_5_1)
check("5-1", ans_5_1, "大きい値がある")

print("\nすべて OK!")
