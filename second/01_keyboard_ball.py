"""第2週-01: キーボードでボールを動かす (カメラは使わない)

実行方法 (second で):
    uv run python 01_keyboard_ball.py

解説は second/README.md の「01」を参照．
第2週のアプリは「背景画像の上に，ボール画像を好きな位置に貼り付ける」ことの繰り返しなので，
ここでその部品を作っておく．課題1〜3 が OK になるとウィンドウが開き，w/a/s/d でボールが動く．
"""

from pathlib import Path

import cv2
import numpy as np

IMAGE_DIR = Path(__file__).resolve().parent / "image_data"


# ============================================================
# 課題1: 画像を中心座標を指定して貼り付ける
# ============================================================
# 背景 bg のコピーを作り，fg の中心が (cx, cy) に来るように貼り付けた画像を返せ．
#   - fg の幅・高さが奇数でも動くこと (fg の左上 = (cx - w // 2, cy - h // 2) とすればよい)
#   - 貼り付ける位置ははみ出さないものとしてよい (はみ出さないようにするのは課題2)
#   - bg そのものを書き換えないこと (bg.copy() を使う)
def paste_center(bg, fg, cx, cy):
    out = bg.copy()
    h, w = fg.shape[:2]
    x0 = ...  # TODO
    y0 = ...  # TODO
    assert x0 is not ... and y0 is not ..., "課題1 がまだ未記入"  # この行は消さない
    # TODO: out の (y0, x0) から高さ h，幅 w の範囲に fg を代入する (1行)

    return out


# ============================================================
# 課題2: はみ出さないように中心座標を制限する
# ============================================================
# 大きさ (fg_w, fg_h) の画像を，大きさ (bg_w, bg_h) の背景の中に完全に収めたい．
# 中心座標 (cx, cy) を収まる範囲に制限して返せ．
#   ヒント: 05_functions の clamp．左端に寄せたときの中心は fg_w // 2，
#           右端に寄せたときの中心は bg_w - (fg_w - fg_w // 2)
def clamp_center(cx, cy, bg_w, bg_h, fg_w, fg_h):
    cx = ...  # TODO
    cy = ...  # TODO
    assert cx is not ... and cy is not ..., "課題2 がまだ未記入"  # この行は消さない
    return cx, cy


# ============================================================
# 課題3: キーに応じて中心座標を動かす
# ============================================================
# key が "w" なら上，"s" なら下，"a" なら左，"d" なら右に step ピクセル動かした (cx, cy) を返せ．
# それ以外のキーなら動かさない．画像の y 座標は「下向きが正」であることに注意．
def move(cx, cy, key, step):
    # TODO: if / elif で書く
    return cx, cy


# ============================================================
# 自動チェック (ここは編集しなくてよい)
# ============================================================
def run_checks():
    bg = np.zeros((10, 12), np.uint8)
    fg = np.full((3, 5), 9, np.uint8)  # 奇数の大きさ
    out = paste_center(bg, fg, 6, 4)
    expected = bg.copy()
    expected[3:6, 4:9] = 9
    assert np.array_equal(out, expected), f"課題1: 貼り付ける位置が違う\n{out}"
    assert bg.max() == 0, "課題1: bg そのものを書き換えている"
    print("OK 課題1")

    for (cx, cy), exp in [((-100, 4), (2, 4)), ((100, 100), (9, 8)), ((6, 4), (6, 4))]:
        got = clamp_center(cx, cy, 12, 10, 5, 3)
        assert got == exp, f"課題2: clamp_center({cx}, {cy}, 12, 10, 5, 3) は {exp} (今は {got})"
        paste_center(bg, fg, *got)  # はみ出さなければエラーにならない
    print("OK 課題2")

    for key, exp in [("w", (50, 40)), ("s", (50, 60)), ("a", (40, 50)), ("d", (60, 50)), ("x", (50, 50))]:
        got = move(50, 50, key, 10)
        assert got == exp, f'課題3: move(50, 50, "{key}", 10) は {exp} (今は {got})'
    print("OK 課題3")


def main():
    ball = cv2.imread(str(IMAGE_DIR / "ball.png"))
    stadium = cv2.resize(cv2.imread(str(IMAGE_DIR / "stadium.png")), (1200, 700))
    bg_h, bg_w = stadium.shape[:2]
    fg_h, fg_w = ball.shape[:2]
    cx, cy = bg_w // 2, bg_h // 2

    print("w/a/s/d で移動，q で終了")
    while True:
        cv2.imshow("output", paste_center(stadium, ball, cx, cy))
        k = cv2.waitKey(30) & 0xFF
        if k == ord("q"):
            break
        if k != 255:
            cx, cy = move(cx, cy, chr(k), 20)
            cx, cy = clamp_center(cx, cy, bg_w, bg_h, fg_w, fg_h)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run_checks()
    main()
