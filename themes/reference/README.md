# 参考資料

第3・4週のテーマと関係が深い参考資料．解答例ではなく，テーマの出発点として使う．

| フォルダ | 内容 | 関係するテーマ |
| --- | --- | --- |
| `A3/grabcut.py` | GrabCut による前景の切り出し | A3 |
| `C1/haar_face_detect.py`, `C1/face_data/` | Haar-like 特徴のカスケード分類器による顔・目の検出 | C1 |
| `hog_knn/` | 背景差分で物体を切り出し，HOG 特徴 + 最近傍法で分類する | C2, C3 |

## hog_knn の使い方

`themes/reference/hog_knn` で次の順に実行する．画像は `data/` の下に保存される．

```shell
uv run 1_collect_background.py     # 物体の無い画像を撮る (s で保存, q で終了) → data/background/
uv run 2_collect_data.py A         # 物体Aを撮る (s で背景を撮る → 物体を置いて c で保存) → data/A/
uv run 2_collect_data.py B         # 物体Bも同様 → data/B/
uv run 3_calc_hog.py               # HOG 特徴を計算して data/features.npy に保存
uv run 4_nearest_neighbor_search.py  # カメラの映像を最近傍法で分類 (s で背景を撮ってから)
```
