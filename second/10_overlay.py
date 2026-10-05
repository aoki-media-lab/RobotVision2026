"""第2週-10: マスクを使って画像を合成する (任意課題)

実行方法 (second で):
    uv run python 10_overlay.py                  # Webカメラで実行
    uv run python 10_overlay.py --video 動画.mp4  # 動画ファイルで実行

解説は second/README.md の「10」を参照．
四角い画像をそのまま貼ると背景の黒い部分まで貼られてしまう．
マスク (貼りたい部分だけ白い画像) を作り，その部分だけを置き換えると自然に合成できる．
アプリ制作でキャラクターやエフェクトを重ねるときに使う．

キー操作: q 終了 / r 録画開始・停止 / v カメラ⇔録画の切り替え / スペース 一時停止
"""

from pathlib import Path

import cv2
import numpy as np

from common import Trackbars, run

IMAGE_DIR = Path(__file__).resolve().parent / "image_data"


# ============================================================
# 課題1: 貼りたい部分のマスクを作る
# ============================================================
# 黒い背景の上に描かれた画像 fg (BGR) から，「黒でない部分」を 255 にしたマスクを返せ．
# グレースケールに変換し，値が th より大きい画素を 255 とする (cv2.threshold か np.where)．
def make_mask(fg, th):
    return ...  # TODO


# ============================================================
# 課題2: マスクの部分だけ置き換える
# ============================================================
# frame の左上 (x, y) の位置に fg を合成した画像を返せ．mask が 255 の画素だけ fg に置き換える．
# fg の一部が frame からはみ出すときは，はみ出した部分を切り捨てて合成すること (エラーにしない)．
# fg が完全に画面外なら frame をそのまま返す．
#   ヒント: 合成する範囲は frame 上で x0 = max(x, 0) 〜 x1 = min(x + fw, W)．
#           fg 側では x0 - x 〜 x1 - x の範囲が対応する (y も同様)．
#           置き換えは np.where(mask[..., None] > 0, fg_part, roi) か cv2.bitwise_and / cv2.add
def overlay(frame, fg, mask, x, y):
    out = frame.copy()
    H, W = frame.shape[:2]
    fh, fw = fg.shape[:2]
    # TODO

    return out


# ============================================================
# 自動チェック (ここは編集しなくてよい)
# ============================================================
def run_checks():
    fg = np.zeros((4, 4, 3), np.uint8)
    fg[1:3, 1:3] = (0, 0, 255)  # 中央 2x2 が赤，周りは黒
    mask = make_mask(fg, 10)
    assert mask is not ..., "課題1 がまだ未記入"
    assert mask.shape == (4, 4) and mask[1, 1] == 255 and mask[0, 0] == 0, "課題1: マスクが違う"
    print("OK 課題1")

    frame = np.full((10, 10, 3), 100, np.uint8)
    out = overlay(frame, fg, mask, 3, 2)
    assert (out[3, 4] == (0, 0, 255)).all(), "課題2: 赤い部分が合成されていない"
    assert (out[2, 3] == 100).all(), "課題2: 黒い部分 (マスクの外) まで貼られている"
    assert (frame == 100).all(), "課題2: frame そのものを書き換えている"
    out = overlay(frame, fg, mask, -2, 8)  # 左下にはみ出す
    assert (out[9, 0] == (0, 0, 255)).all(), "課題2: はみ出したときの合成位置が違う"
    out = overlay(frame, fg, mask, 50, 50)  # 完全に画面外
    assert (out == frame).all(), "課題2: 画面外なら frame のまま"
    print("OK 課題2")


tb = Trackbars("params", {"x": (0, 1280), "y": (0, 720), "threshold": (10, 255)})
shizuku = cv2.imread(str(IMAGE_DIR / "shizuku.png"))


def process(frame):
    mask = make_mask(shizuku, tb["threshold"])
    return {"result": overlay(frame, shizuku, mask, tb["x"], tb["y"]), "mask": mask}


if __name__ == "__main__":
    run_checks()
    run(process)
