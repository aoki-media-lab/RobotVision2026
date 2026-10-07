"""第2週-01 [課題]: キーボードでボールを動かす (カメラは使わない)

実行方法 (second で):
    uv run 01_keyboard_ball.py

解説は second/README.md の「01」を参照．
スタジアムの画像の上にボールの画像を貼り付けて表示する．
課題1・2 を完成させると，w/a/s/d でボールが上下左右に動き，画面の端で止まるようになる．
q キーで終了する．
"""

from pathlib import Path

import cv2


def paste_center(bg, fg, cx, cy):
    """背景 bg のコピーに，fg の中心が (cx, cy) に来るように貼り付けた画像を返す"""
    out = bg.copy()
    h, w = fg.shape[:2]
    x0, y0 = cx - w // 2, cy - h // 2
    out[y0 : y0 + h, x0 : x0 + w] = fg
    return out


# ============================================================
# 課題1: キーに応じて中心座標を動かす
# ============================================================
def move(cx, cy, key, step):
    """key が "w" なら上，"s" なら下，"a" なら左，"d" なら右に step ピクセル動かした (cx, cy) を返せ．
    それ以外のキーなら動かさない．画像の y 座標は「下向きが正」であることに注意"""
    # TODO

    return cx, cy


# ============================================================
# 課題2: はみ出さないように中心座標を制限する
# ============================================================
def clamp_center(cx, cy, bg_w, bg_h, fg_w, fg_h):
    """大きさ (fg_w, fg_h) の画像を，大きさ (bg_w, bg_h) の背景の中に完全に収めたい．
    中心座標 (cx, cy) を収まる範囲に制限して返せ．
    制限しないと，ボールを画面の端まで動かしたときにエラーで止まる"""
    # TODO

    return cx, cy


if __name__ == "__main__":
    image_dir = Path(__file__).resolve().parent / "image_data"
    ball = cv2.imread(str(image_dir / "ball.png"))
    stadium = cv2.resize(cv2.imread(str(image_dir / "stadium.png")), (1200, 700))
    bg_h, bg_w = stadium.shape[:2]
    fg_h, fg_w = ball.shape[:2]
    cx, cy = bg_w // 2, bg_h // 2  # ボールの中心 (最初はスタジアムの中央)
    step = 20  # 1回のキー入力で動かす距離 [px]

    print("w/a/s/d で移動，q で終了")
    while True:
        cv2.imshow("output", paste_center(stadium, ball, cx, cy))
        k = cv2.waitKey(30) & 0xFF
        if k == ord("q"):
            break
        if k != 255:  # 何かキーが押された
            cx, cy = move(cx, cy, chr(k), step)
            cx, cy = clamp_center(cx, cy, bg_w, bg_h, fg_w, fg_h)
    cv2.destroyAllWindows()
