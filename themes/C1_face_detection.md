# C1 顔検出

キーワード: Viola-Jones，AdaBoost，YuNet

## 問い

- Viola-Jones 法は，どんな特徴 (Haar-like 特徴) を，どうやって高速に計算し (積分画像)，どう組み合わせて (AdaBoost，カスケード) 顔を見つけているか
- 深層学習ベースの検出器 (YuNet) と比べて，何が強く，何が弱いか
- 横顔・マスク・暗い部屋・遠くの顔など，どんな条件で見逃しや誤検出が起きるか

## 最初の一歩

- 関数: `cv2.CascadeClassifier`, `detectMultiScale`, `cv2.FaceDetectorYN.create`, `detect`
- 最初の実験: `reference/C1/haar_face_detect.py` を動かし，`scaleFactor` と `minNeighbors` を
  トラックバーで動かして，見逃し・誤検出・FPS がどう変わるかを記録する
- 次の実験: 同じ録画動画に対して YuNet (OpenCV の `FaceDetectorYN`．モデルは opencv_zoo の `face_detection_yunet`) を
  適用し，顔の向き・距離・明るさを変えた場面で Haar と比べる

## 他テーマとの境界

- 複数の検出枠の重なりを1つにまとめる NMS の自前実装は C2 が担当．C1 は OpenCV の出力をそのまま使ってよい
- 検出した顔の追跡・ぶれの抑制は B2, B3 の範囲

## CPUでの注意点

- `detectMultiScale` は探す大きさの範囲 (`minSize`, `maxSize`) と `scaleFactor` で速度が大きく変わる
- YuNet は入力サイズ (`setInputSize`) を小さくすると速くなるが，小さい顔を見逃しやすくなる

## 参考資料

- `reference/C1/haar_face_detect.py`, `reference/C1/face_data/`: Haar-like 特徴による顔・目の検出
