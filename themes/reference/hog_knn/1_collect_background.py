"""背景の画像を集める (s で保存, q で終了)．保存先: data/background/"""

from pathlib import Path

import cv2

SAVE_DIR = Path(__file__).resolve().parent / "data" / "background"

cap = cv2.VideoCapture(0)

# スクショしたかどうかを保存する変数 (まだ撮っていないのでFalse)
screenshot = False
# スクショを保存する変数
photo = None

# フォルダにある画像の枚数を取得
n_data = len(list(SAVE_DIR.glob("*.jpg")))

# 実行
while True:
    # Webカメラのフレーム取得
    ret, frame = cap.read()
    cv2.imshow("camera", frame)

    # キーボードの入力の受付
    k = cv2.waitKey(1)

    # 終了
    if k == ord("q"):
        break
    # 写真を保存
    elif k == ord("s"):
        cv2.imwrite(str(SAVE_DIR / f"{n_data}.jpg"), frame)
        n_data += 1

cap.release()
cv2.destroyAllWindows()
