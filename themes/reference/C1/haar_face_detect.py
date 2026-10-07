"""Haar-like 特徴によるカスケード分類器で顔と目を検出する

実行方法 (themes/reference/C1 で):
    uv run haar_face_detect.py
    uv run haar_face_detect.py --video 動画.mp4

学習済みの分類器のデータ (face_data/*.xml) を使う．OpenCV にも同じものが入っており，
cv2.data.haarcascades のフォルダにある．以下のリンクからも取得できる．
https://github.com/opencv/opencv/tree/master/data/haarcascades
笑顔 (haarcascade_smile.xml) と上半身 (haarcascade_upperbody.xml) のデータも置いてある．
"""

import sys
from pathlib import Path

import cv2

sys.path.append(str(Path(__file__).resolve().parents[3]))
from common import run


def process(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 顔の x座標, y座標, 幅, 高さ を取得
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    for x, y, w, h in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        face = img[y : y + h, x : x + w]
        face_gray = gray[y : y + h, x : x + w]

        # 顔の中で目を検出
        eyes = eye_cascade.detectMultiScale(face_gray)
        for ex, ey, ew, eh in eyes:
            cv2.rectangle(face, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
    return img


if __name__ == "__main__":
    data_dir = Path(__file__).resolve().parent / "face_data"
    face_cascade = cv2.CascadeClassifier(str(data_dir / "haarcascade_frontalface_default.xml"))
    eye_cascade = cv2.CascadeClassifier(str(data_dir / "haarcascade_eye.xml"))
    run(process)
