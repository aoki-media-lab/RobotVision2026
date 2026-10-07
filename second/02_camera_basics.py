"""第2週-02 [課題]: カメラの処理を process(frame) で書く

実行方法 (second で):
    uv run 02_camera_basics.py                  # Webカメラで実行
    uv run 02_camera_basics.py --video 動画.mp4  # 動画ファイルで実行

解説は second/README.md の「02」を参照．
カメラから画像を読み込んで表示するループは common.run が受け持つ．
自分で書くのは「1枚の画像を受け取って，処理した画像を返す」関数 process と，
キーが押されたときに呼ばれる関数 on_key．
課題を完成させると，f キーを押すたびに左右反転のオン・オフが切り替わる．
q キーで終了する．
"""

import sys
from pathlib import Path

import cv2

sys.path.append(str(Path(__file__).resolve().parents[1]))
from common import Trackbars, run


# ============================================================
# 課題: キーで左右反転のオン・オフを切り替える
# ============================================================
def on_key(key):
    """q 以外のキーが押されるたびに呼ばれる．key は押されたキーの文字 (例: "f")．
    "f" が押されたら，state["flip"] の True / False を切り替えよ"""
    # TODO

    return


def process(frame):
    # 反転がオンなら，鏡のように左右反転する
    if state["flip"]:
        frame = cv2.flip(frame, 1)
    # カーネルの大きさ 2v+1 のガウシアンぼかし (v = 0 ならそのまま)
    v = tb["blur"]
    if v > 0:
        frame = cv2.GaussianBlur(frame, (2 * v + 1, 2 * v + 1), 0)
    return frame


if __name__ == "__main__":
    tb = Trackbars("params", {"blur": (0, 30)})
    # フレームをまたいで覚えておく値 (反転するかどうか)
    state = {"flip": False}
    run(process, on_key=on_key)
