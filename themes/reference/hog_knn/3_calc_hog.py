from pathlib import Path

import cv2
import numpy as np
from skimage.feature import hog


def main():
    data_dir = Path(__file__).resolve().parent / "data"

    classes = ["background", "A", "B"]
    cls2label = {"background": 0, "A": 1, "B": 2}

    # 特徴量とラベルを保持するリスト
    features = []
    labels = []

    for c in classes:
        label = cls2label[c]

        # 画像のパスの一覧(リスト)を取得
        image_paths = sorted((data_dir / c).glob("*.jpg"))
        num_images = len(image_paths)

        for path in image_paths:
            # 画像の読み込み
            img = cv2.imread(str(path))

            # grayscaleに変換
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # リサイズ (H, W) = (56, 56) ※要調整
            gray = cv2.resize(gray, (56, 56))

            # HOGによって特徴抽出
            feat = hog(gray)

            # リストに追加
            features.append(feat)
            labels.append(label)

        print(f"{num_images} images found in {c}")

    # numpy配列に変換
    features = np.array(features, dtype=np.float32)
    labels = np.array(labels, dtype=np.uint8)

    # 配列を保存
    np.save(data_dir / "features.npy", features)
    np.save(data_dir / "labels.npy", labels)


if __name__ == "__main__":
    main()
