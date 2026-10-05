"""トラックバー(スライダー)でパラメータを動かすための共通部品

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

import os

import cv2


class Trackbars:
    def __init__(self, window, params):
        """
        Args:
            window: トラックバーを置くウィンドウ名
            params: {"名前": (初期値, 最大値), ...}
        """
        self.window = window
        self._defaults = {}
        # RV_HEADLESS=1 のときは画面を作らない(動作確認用)
        self._enabled = not os.environ.get("RV_HEADLESS")
        if not self._enabled:
            self._defaults = {name: int(init) for name, (init, _m) in params.items()}
            return
        try:
            cv2.namedWindow(window)
            for name, (init, maximum) in params.items():
                cv2.createTrackbar(name, window, int(init), int(maximum), lambda _v: None)
                self._defaults[name] = int(init)
        except cv2.error:
            # 画面のない環境(動作確認用)では初期値をそのまま返す
            self._enabled = False
            self._defaults = {name: int(init) for name, (init, _m) in params.items()}

    def __getitem__(self, name):
        if not self._enabled:
            return self._defaults[name]
        return cv2.getTrackbarPos(name, self.window)

    def values(self):
        """全パラメータを {"名前": 値} の辞書で返す"""
        return {name: self[name] for name in self._defaults}
