"""第2週-03: 色で抽出した領域にラベルを付ける

実行方法 (second で):
    uv run python 03_color_labeling.py                  # Webカメラで実行
    uv run python 03_color_labeling.py --video 動画.mp4  # 動画ファイルで実行

解説は second/README.md の「03」を参照．
第1週の HSV マスクは「どの画素が対象の色か」しか分からない．
ラベリング (連結成分分析) で「つながった白い領域」ごとに番号を振ると，
領域ごとの位置・大きさ・重心が分かり，「物体がどこにあるか」が求まる．

キー操作: q 終了 / r 録画開始・停止 / v カメラ⇔録画の切り替え / スペース 一時停止
"""

import cv2
import numpy as np

from common import Trackbars, run


def hsv_mask(frame, lower, upper):
    """第1週で作ったもの (完成済み)"""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
    return cv2.medianBlur(mask, 5)


# ============================================================
# 課題1: バグ修正 — 面積の大きい領域を取り出す
# ============================================================
# 昨年度の教材のコードをほぼそのまま関数にしたもの．
# 「面積の大きい順に n 個の領域を返す」つもりだが，状況によっては背景を物体として返してしまう．
#
#   cv2.connectedComponentsWithStats(mask) の戻り値:
#     n_labels  : ラベルの数 (背景も含む)
#     labels    : 各画素のラベル番号の画像
#     stats     : 各ラベルの [左上x, 左上y, 幅, 高さ, 面積] (n_labels 行 5 列)
#     centroids : 各ラベルの重心 [x, y] (n_labels 行 2 列)
#   ラベル 0 は常に背景 (マスクが 0 の画素)．
#
# どんな状況でおかしくなるかを考え (自動チェックのテスト画像がヒント)，正しく直せ．
# さらに min_area より小さい領域は返さないようにせよ．
# 戻り値: [(x, y, w, h, area, cx, cy), ...] を面積の大きい順に並べたリスト (最大 n 個)
def largest_regions(mask, n, min_area):
    n_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask)
    regions = []
    if n_labels >= n + 1:
        # 面積でソートし，最大のもの(=背景のはず)を除いた上位 n 個を使う
        top_idx = stats[:, 4].argsort()[-(n + 1) : -1][::-1]
        for i in top_idx:
            x, y, w, h, area = stats[i]
            cx, cy = centroids[i]
            regions.append((int(x), int(y), int(w), int(h), int(area), float(cx), float(cy)))
    return regions


# ============================================================
# 課題2: 領域を描く
# ============================================================
# regions の各領域について，外接矩形 (赤 (0, 0, 255)，太さ 2) と
# 重心の位置に塗りつぶした円 (黄 (0, 255, 255)，半径 5) を描いた画像を返せ．
#   使う関数: cv2.rectangle(画像, 左上(x, y), 右下(x, y), 色, 太さ)
#            cv2.circle(画像, 中心(x, y), 半径, 色, -1)   ← 太さ -1 で塗りつぶし
#   重心は float なので int にしてから渡すこと
def draw_regions(frame, regions):
    for x, y, w, h, area, cx, cy in regions:
        pass  # TODO
    return frame


# ============================================================
# 自動チェック (ここは編集しなくてよい)
# ============================================================
def run_checks():
    # テスト1: 小さな物体が2つと，ごく小さなノイズ
    mask = np.zeros((100, 100), np.uint8)
    mask[10:30, 10:40] = 255  # 面積 600
    mask[60:70, 60:70] = 255  # 面積 100
    mask[90, 90] = 255  # 面積 1 (ノイズ)
    r = largest_regions(mask, 2, min_area=10)
    assert [reg[4] for reg in r] == [600, 100], f"課題1: テスト1 で面積 [600, 100] の2つを返すこと (今は {[reg[4] for reg in r]})"

    # テスト2: 物体が画面の大部分を占める (カメラに物体を近づけたとき)
    mask = np.full((100, 100), 255, np.uint8)
    mask[:10, :] = 0  # 背景は上の 1000 画素だけ
    r = largest_regions(mask, 1, min_area=10)
    assert len(r) == 1 and r[0][4] == 9000, (
        f"課題1: テスト2 で面積 9000 の物体を返すこと (今は {[reg[4] for reg in r]})．背景を返していないか?"
    )

    # テスト3: 物体が1つしかないのに n = 2 を指定
    mask = np.zeros((100, 100), np.uint8)
    mask[10:30, 10:40] = 255
    r = largest_regions(mask, 2, min_area=10)
    assert [reg[4] for reg in r] == [600], f"課題1: テスト3 で物体が1つだけのときもそれを返すこと (今は {r})"

    # テスト4: min_area
    mask = np.zeros((100, 100), np.uint8)
    mask[10:30, 10:40] = 255
    mask[90:92, 90:92] = 255  # 面積 4
    r = largest_regions(mask, 3, min_area=10)
    assert [reg[4] for reg in r] == [600], f"課題1: テスト4 で min_area 未満の領域は返さないこと (今は {[reg[4] for reg in r]})"
    print("OK 課題1")

    frame = np.zeros((100, 100, 3), np.uint8)
    out = draw_regions(frame, [(10, 10, 30, 20, 600, 24.6, 19.5)])
    assert (out[10, 20] == (0, 0, 255)).all(), "課題2: 外接矩形が描かれていない"
    assert (out[19, 24] == (0, 255, 255)).all(), "課題2: 重心に円が描かれていない"
    print("OK 課題2")


# ============================================================
# カメラで実行
# ============================================================
tb = Trackbars(
    "params",
    {
        "H_min": (0, 179),
        "H_max": (30, 179),
        "S_min": (60, 255),
        "V_min": (60, 255),
        "n": (2, 10),  # 取り出す領域の数
        "min_area": (300, 5000),
    },
)


def process(frame):
    mask = hsv_mask(frame, [tb["H_min"], tb["S_min"], tb["V_min"]], [tb["H_max"], 255, 255])
    regions = largest_regions(mask, max(1, tb["n"]), tb["min_area"])
    for x, y, w, h, area, cx, cy in regions:
        cv2.putText(frame, f"area {area}", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
    return {"result": draw_regions(frame, regions), "mask": mask}


if __name__ == "__main__":
    run_checks()
    run(process)


# ============================================================
# [観察] 実際に試して，結果と原因をそれぞれ一文で書け
# ============================================================
# 観察1: 物体をゆっくり動かしたとき，重心の位置 (黄色の点) はフレームごとにどの程度ぶれたか．
#        物体が止まっていてもぶれるなら，その原因は何か．
#   結果:
#   原因:
#
# 観察2: 物体を手で半分隠すと，外接矩形と重心はどうなったか．物体が2つに分かれて見えたときは?
#   結果:
#   原因:
#
# 観察3: 同じ色の物体を2つ画面に入れ，交差させるように動かすと，
#        「どちらの物体がどちらか」を区別し続けられるか．
#   結果:
#   原因:
