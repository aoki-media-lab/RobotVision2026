# requirement: opencv-contrib-python
# if 'bgsegm' was not found, run `uv sync` in the repository root

"""物体の画像を集める．

    uv run python 2_collect_data.py A     # data/A/ に保存
    uv run python 2_collect_data.py B     # data/B/ に保存

s: 物体の無い背景を撮る → 物体を置いて c: 背景との差分で物体の部分を切り出して保存 / q: 終了
"""

import sys
from pathlib import Path

import cv2
import numpy as np

HERE = Path(__file__).resolve().parent
CLASS_NAME = sys.argv[1] if len(sys.argv) > 1 else "A"
SAVE_DIR = HERE / "data" / CLASS_NAME
MASK_DIR = HERE / "mask_results"
SAVE_DIR.mkdir(parents=True, exist_ok=True)

cap = cv2.VideoCapture(0)

# スクショしたかどうかを保存する変数 (まだ撮っていないのでFalse)
screenshot = False
# スクショを保存する変数
photo = None

# フォルダにある画像の枚数を取得
n_data = len(list(SAVE_DIR.glob("*.jpg")))

# ノイズ除去のためのカーネルの定義
kernel = np.ones((5, 5), np.uint8)

# 実行
while True:
    # Webカメラのフレーム取得
    ret, frame = cap.read()
    cv2.imshow("camera", frame)

    # キーボードの入力の受付
    k = cv2.waitKey(1)

    # スクショがあるなら差分を出力
    if screenshot:
        fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
        fgmask = fgbg.apply(frame)
        fgmask = fgbg.apply(photo)
        cv2.imshow("flow", fgmask)

        if k == ord("c"):
            cv2.imwrite(str(MASK_DIR / "initial_mask.jpg"), fgmask)

            # 白色領域のノイズを除去する
            fgmask = cv2.erode(fgmask, kernel)  # 収縮処理
            cv2.imwrite(str(MASK_DIR / "eroded_mask.jpg"), fgmask)

            fgmask = cv2.dilate(fgmask, kernel)  # 膨張処理
            cv2.imwrite(str(MASK_DIR / "denoised_mask.jpg"), fgmask)

            # マスクのかかっていない部分のみ切り取る
            # np.where(条件式) で，条件を満たすインデックスを取り出すことができる
            H_arr, W_arr = np.where(fgmask == 255)
            if len(H_arr) == 0:
                print("差分が見つからなかった")
                continue

            left = min(W_arr)
            right = max(W_arr)
            top = min(H_arr)
            bottom = max(H_arr)

            # 不要な部分は無視して画像の保存
            cv2.imwrite(str(SAVE_DIR / f"{n_data}.jpg"), frame[top : bottom + 1, left : right + 1])

            n_data += 1

    # 終了
    if k == ord("q"):
        break
    # フレームを保存 (スクショ)
    elif k == ord("s"):
        photo = frame
        screenshot = True

cap.release()
cv2.destroyAllWindows()
