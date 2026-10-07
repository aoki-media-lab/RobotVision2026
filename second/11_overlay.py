"""第2週-11: マスクを使って画像を合成する

実行方法 (second で):
    uv run 11_overlay.py                  # Webカメラで実行
    uv run 11_overlay.py --video 動画.mp4  # 動画ファイルで実行

解説は second/README.md の「11」を参照．
四角い画像をそのまま貼ると背景の黒い部分まで貼られてしまう．
マスク (貼りたい部分だけ白い画像) を作り，その部分だけを置き換えると自然に合成できる．
カメラの映像の左上に画像を合成する．
q キーで終了する．
"""

import sys
from pathlib import Path

import cv2

sys.path.append(str(Path(__file__).resolve().parents[1]))
from common import Trackbars, run


def process(frame):
    h, w = fg.shape[:2]

    # 合成したい画像の「黒でない部分」を白にしたマスクと，その反転
    gray = cv2.cvtColor(fg, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, tb["threshold"], 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)

    # 合成したい画像の前景だけを取り出す (背景は黒になる)
    fg_only = cv2.bitwise_and(fg, fg, mask=mask)

    # カメラの映像の左上 (注目領域) のうち，前景が来る部分を黒にする
    roi = frame[0:h, 0:w]
    bg_only = cv2.bitwise_and(roi, roi, mask=mask_inv)

    # 黒にした部分に前景を足し合わせて，左上に戻す
    frame[0:h, 0:w] = cv2.add(bg_only, fg_only)
    return {"result": frame, "mask": mask}


if __name__ == "__main__":
    fg = cv2.imread(str(Path(__file__).resolve().parent / "image_data" / "shizuku.png"))
    tb = Trackbars("params", {"threshold": (10, 255)})
    run(process)
