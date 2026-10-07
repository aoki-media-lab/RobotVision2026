"""トラックバー(スライダー)でパラメータを動かす

    from common import Trackbars

    tb = Trackbars("params", {
        "H_min": (0, 179),     # 名前: (初期値, 最大値)
        "H_max": (30, 179),
    })

    def process(frame):
        h_min = tb["H_min"]   # 現在のスライダーの値(int)を取得
        ...

トラックバーの最小値は常に 0．負の値や小数が欲しいときは，取得した値を自分で変換する
(例: sigma = tb["sigma_x10"] / 10)．
"""

import cv2


class Trackbars:
    def __init__(self, window, params):
        """
        Args:
            window: トラックバーを置くウィンドウ名
            params: {"名前": (初期値, 最大値), ...}
        """
        self.window = window
        self.names = list(params)
        cv2.namedWindow(window)
        for name, (init, maximum) in params.items():
            cv2.createTrackbar(name, window, int(init), int(maximum), lambda _v: None)

    def __getitem__(self, name):
        return cv2.getTrackbarPos(name, self.window)

    def values(self):
        """全パラメータを {"名前": 値} の辞書で返す"""
        return {name: self[name] for name in self.names}
