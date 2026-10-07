# 第2週: カメラの映像を処理する

この週の目標は次の3つ．

- `process(frame) -> frame` の形で，カメラの映像を1フレームずつ処理するプログラムを書けるようになる
- 色・差分・動き (オプティカルフロー) で「対象がどこにあるか」を求め，簡単なアプリにする
- 照明・似た色・カメラの揺れなどで **何が壊れるか** を観察し，原因を説明できるようになる

第3週からの調査テーマ・第5週からのアプリ制作は，この週の内容を土台にする．

## 進め方

```shell
cd second
uv run 02_camera_basics.py                       # Webカメラ
uv run 02_camera_basics.py --video 動画.mp4       # 動画ファイル
uv run 02_camera_basics.py --camera 1            # 別のカメラ (外付けなど)
```

`q` キーで終了する．

- **[課題]** と付いたファイル (01, 02, 03, 04, 07) は，`# TODO` の部分を自分で書いて完成させる．
  この README の説明とコード例を参考にする
- それ以外のファイルは完成している．README の説明と照らし合わせてコードを読み，実行し，
  トラックバーを動かしたり，コードを書き換えたりして動きを確かめる
- 各節の末尾の **[観察]** は，実際に試して「結果」と「原因」をそれぞれ一文で書く
- 第2週の内容は基礎なので，生成AI (ChatGPT, Gemini など) は基本的に使わず，
  この README とエラーメッセージを手がかりに自分で書くこと

**同じ動画で比べる習慣をつけること**．パラメータや手法を変えて「良くなった」と言うには，
同じ入力で比べなければならない．うまくいかない場面を見つけたら動画に撮っておき
(スマートフォンや PC のカメラアプリで撮ったものでよい)，`--video` でくり返し再生しながら確かめるとよい．

| ファイル | 内容 |
| --- | --- |
| `01_keyboard_ball.py` | **[課題]** キー操作でボールを動かす (カメラなし) |
| `02_camera_basics.py` | **[課題]** `process` の書き方，キーで反転を切り替える |
| `03_hsv_color.py` | **[課題]** HSV による色の抽出 |
| `04_threshold_noise.py` | **[課題]** 二値化とノイズ除去 |
| `05_color_labeling.py` | ラベリングで領域ごとの位置・大きさを求める |
| `06_labeling_app.py` | 色の物体でボールを動かす |
| `07_multi_color.py` | **[課題]** 複数の色を同時に追跡する |
| `08_background_subtraction.py` | 背景差分: 自前の3手法と MOG の比較 |
| `09_optical_flow.py` | オプティカルフロー (特徴点の追跡) |
| `10_flow_app.py` | 動きの向きでボールを動かす |
| `11_overlay.py` | マスクを使った画像の合成 |
| `advanced/erode_numpy.py` | **[発展課題]** numpy だけで収縮・膨張・メディアン |
| `advanced/harris_numpy.py` | **[発展課題]** numpy だけで Harris コーナー検出 |

以下のコード例では，`print` の出力を `# → ` の後ろに書いている．

---

## 共通部品 `common`

ファイル: `common/camera.py` (`run`)，`common/trackbar.py` (`Trackbars`)

カメラを開き，1フレームずつ読み込み，表示し，`q` で終了する……という部分は毎回同じなので，
`common.run` にまとめてある．自分で書くのは **1枚の画像を受け取って，処理した画像を返す関数** だけ．

```python
import sys
from pathlib import Path

import cv2

sys.path.append(str(Path(__file__).resolve().parents[1]))
from common import Trackbars, run

def process(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, tb["threshold"], 255, cv2.THRESH_BINARY)
    return binary                                     # 画像を1枚返す

if __name__ == "__main__":
    tb = Trackbars("params", {"threshold": (120, 255)})   # 名前: (初期値, 最大値)
    run(process)
```

トラックバーの作成や画像の読み込みなどの準備は `if __name__ == "__main__":` の中に書く．
そこで作った変数 (この例の `tb`) は，`process` の中からも使える．

`common/` はリポジトリのトップにあるので，`sys.path.append(...)` でリポジトリのトップを
import の探索先に加えてから `from common import ...` する (第1週 06 を参照)．
`second/` のファイルから見るとリポジトリのトップは1つ上のフォルダなので `parents[1]` を使う．

`common.run` の中では，おおよそ次のことが行われている．

```python
cap = cv2.VideoCapture(0)              # カメラを開く
while True:
    ret, frame = cap.read()            # 1フレーム読み込む (ret は成功したかどうか)
    if not ret:
        break
    result = process(frame)            # 自分で書いた関数を呼ぶ
    cv2.imshow("output", result)       # 結果を表示
    if cv2.waitKey(1) == ord("q"):     # 1ms キー入力を待ち，q なら終了
        break
cap.release()
cv2.destroyAllWindows()
```

### 複数のウィンドウに表示する

`process` が辞書を返すと，キーをウィンドウ名として複数のウィンドウに表示する．

```python
def process(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    return {"camera": frame, "edges": edges}
```

### トラックバー

`Trackbars(ウィンドウ名, {名前: (初期値, 最大値), ...})` でスライダーを作り，`tb["名前"]` で現在の値 (整数) を取る．
最小値は 0 なので，小数や負の値が欲しいときは自分で変換する．

```python
def process(frame):
    size = tb["size"]                  # 0〜50 の整数
    ratio = tb["ratio_%"] / 100        # 0.0〜1.0 の小数に変換
    ...

if __name__ == "__main__":
    tb = Trackbars("params", {"size": (5, 50), "ratio_%": (30, 100)})
    run(process)
```

### フレームをまたいで値を覚えておく

`process` は毎フレーム呼ばれ，関数の中の変数はそのたびに作り直される．
前のフレームの画像や物体の位置などを覚えておきたいときは，`if __name__ == "__main__":` の中で辞書を作っておき，
`process` の中で読み書きする．

```python
def process(frame):
    state["count"] += 1                # 呼ばれた回数
    if state["prev"] is not None:
        diff = cv2.absdiff(frame, state["prev"])   # 前のフレームとの差
    state["prev"] = frame              # 次のフレームのために保存
    ...

if __name__ == "__main__":
    state = {"count": 0, "prev": None}
    run(process)
```

### キー入力を受け取る

`run(process, on_key=関数)` とすると，`q` 以外のキーが押されるたびに，その関数が押されたキーの文字を受け取って呼ばれる．

```python
def on_key(key):
    print(key, "が押された")         # 例: a が押された

if __name__ == "__main__":
    run(process, on_key=on_key)
```

### カメラの確認

`process` を渡さずに `run()` とすると，カメラの映像をそのまま表示する．
リポジトリのトップで `uv run common/camera.py` を実行しても同じことができるので，カメラが動くかの確認に使える．

## 01 [課題] キーボードでボールを動かす

ファイル: `second/01_keyboard_ball.py`

スタジアムの画像の上にボールの画像を貼り付けて表示するところまではできている．
**課題1** (`move`) でキー入力に応じてボールの中心座標を動かし，
**課題2** (`clamp_center`) で画面からはみ出さないように制限する．

### 画像の貼り付け (`paste_center`)

画像の貼り付けは numpy のスライスへの代入．貼り付ける範囲と貼る画像の大きさが一致していなければならない．

```python
bg = np.zeros((300, 400, 3), np.uint8)        # 背景 (高さ 300, 幅 400)
fg = np.full((50, 80, 3), 255, np.uint8)       # 貼る画像 (高さ 50, 幅 80)

out = bg.copy()                                # bg そのものは書き換えない
out[100:150, 20:100] = fg                      # 左上 (x=20, y=100) に貼る
out[100:150, 20:90] = fg
# → ValueError: could not broadcast input array from shape (50,80,3) into shape (50,70,3)
```

`paste_center` は，中心 `(cx, cy)` から左上 `(cx - w // 2, cy - h // 2)` を計算して貼り付けている．
ボールの中心が画面の端に近すぎると，貼り付ける範囲が画面の外にはみ出して上のようなエラーになる．

### キー入力

`cv2.waitKey(ミリ秒)` は，その時間キー入力を待ち，押されたキーの番号を返す
(押されなければ -1．`& 0xFF` をとると 255 になる)．
`chr(番号)` で文字に，`ord(文字)` で番号に変換できる．

```python
k = cv2.waitKey(30) & 0xFF     # 下位 8 ビットだけ使う (OS による違いを吸収する)
print(chr(k))                  # → 例えば "j" が押されたら j

key = "j"
x, y = 100, 100
if key == "j":                 # 押されたキーで処理を分ける
    x -= 5
elif key == "l":
    x += 5
print(x, y)                    # → 95 100
```

画像の座標は **右向きが x の正，下向きが y の正**．「上に動かす」は y を減らすこと．

### 範囲に収める

第1週 05 の `clamp` と同じく，`max` と `min` で値を範囲に収める．

```python
x = 450
x = max(0, min(x, 320))        # 0 以上 320 以下に収める
print(x)                       # → 320
```

ボールの中心が動ける範囲を考えるときは，ボールの幅の半分だけ内側に入る必要がある．
幅が奇数でもずれないよう，左側は `w // 2`，右側は `w - w // 2` を使う．

```python
w = 7
print(w // 2)          # → 3   (中心から左端までの距離)
print(w - w // 2)      # → 4   (中心から右端の外側までの距離)
```

## 02 [課題] カメラの処理を `process(frame)` で書く

ファイル: `second/02_camera_basics.py`

左右反転 → ぼかし を順に行っている．左右反転は `state["flip"]` が `True` のときだけ行う．
**課題** では，キーが押されたときに呼ばれる関数 `on_key` を書き，`f` キーを押すたびに
`state["flip"]` の `True` / `False` を切り替えて，反転のオン・オフを切り替えられるようにする．
完成したら，このファイルを書き換えて，いろいろな処理を試してみるとよい．

### キーで状態を切り替える

`on_key` で `state` の値を書き換えると，次のフレームから `process` の動きが変わる．
`True` / `False` を切り替えるには `not` を使う．

```python
state = {"gray": False}

def on_key(key):
    if key == "g":
        state["gray"] = not state["gray"]    # True なら False に，False なら True にする

def process(frame):
    if state["gray"]:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return frame
```

### 反転

`cv2.flip(画像, 方向)` で反転する．Webカメラの映像は左右が逆なので，左右反転すると鏡のように見える．

| 方向 | 結果 |
| --- | --- |
| `0` | 上下反転 |
| `1` | 左右反転 |
| `-1` | 上下左右とも反転 |

### ぼかし

`cv2.GaussianBlur(画像, (幅, 高さ), 0)` でぼかす．カーネルの大きさは **奇数** で，大きいほど強くぼける．
トラックバーの値 `v` から `2v+1` を作れば必ず奇数になる．

### 描画

03 以降では，結果を画像に描き込んで表示する．OpenCV の描画関数は，**座標を `(x, y)` の順で，必ず int で** 渡す (OpenCV 5 では float を渡すとエラー)．
色は `(B, G, R)` のタプル．描画関数は渡した画像そのものを書き換える．

```python
img = np.zeros((200, 300, 3), np.uint8)
cv2.line(img, (10, 20), (200, 20), (255, 0, 0), 2)          # 始点, 終点, 色, 太さ
cv2.rectangle(img, (50, 50), (120, 150), (0, 255, 0), 3)    # 左上, 右下, 色, 太さ
cv2.circle(img, (200, 100), 30, (0, 0, 255), -1)            # 中心, 半径, 色, 太さ (-1 で塗りつぶし)
cv2.putText(img, "hello", (10, 190), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

cv2.circle(img, (200.5, 100.0), 30, (0, 0, 255), -1)
# → cv2.error: ... Can't parse 'center'. Sequence item with index 0 has a wrong type
cv2.circle(img, (int(200.5), int(100.0)), 30, (0, 0, 255), -1)   # int にすれば OK
```

### [観察]

1. blur を 0 → 30 と大きくしていくと，映像の動き (なめらかさ・遅れ) はどう変わったか．

## 03 [課題] HSV による色の抽出

ファイル: `second/03_hsv_color.py`

カメラの映像から，特定の色の物体だけを取り出す．
**課題1** (`hsv_mask`) で HSV の範囲のマスクを作り，**課題2** (`red_mask`) で赤のマスクを作り，
**課題3** (`apply_mask`) でマスクの部分だけ元の色を残す．

### HSV

BGR のままだと「明るいオレンジ」と「暗いオレンジ」は全く違う値になる．
HSV は色を **H (色相: 何色か)，S (彩度: 鮮やかさ)，V (明度: 明るさ)** に分けるので，
H の範囲で「何色か」を指定しやすい．OpenCV の H は 0〜179 (角度 0〜360° の半分)，S と V は 0〜255．

| 色 | H のおよその値 |
| --- | --- |
| 赤 | 0 付近 と 179 付近 |
| 黄 | 30 付近 |
| 緑 | 60 付近 |
| 青 | 120 付近 |

```python
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)     # BGR → HSV
print(hsv[10, 50])                             # → [H S V]
```

### cv2.inRange でマスクを作る

`cv2.inRange(画像, 下限, 上限)` は，3つの値がすべて下限以上・上限以下の画素を 255，それ以外を 0 にした
マスク (白黒画像) を返す．中身は第1週 08 の `(lower <= x) & (x <= upper)` と同じ．

```python
lower = np.array([40, 80, 80])       # [H, S, V] の下限
upper = np.array([80, 255, 255])     # [H, S, V] の上限
mask = cv2.inRange(hsv, lower, upper)   # 緑っぽい画素だけ 255
print(mask.shape, mask.dtype)        # → (高さ, 幅) uint8
```

### マスクの組み合わせと適用

2つのマスクの「または」「かつ」は `cv2.bitwise_or` / `cv2.bitwise_and` でとれる (第1週 08 の `|` / `&` でもよい)．

```python
mask_a = cv2.inRange(hsv, np.array([20, 80, 80]), np.array([35, 255, 255]))   # 黄
mask_b = cv2.inRange(hsv, np.array([40, 80, 80]), np.array([80, 255, 255]))   # 緑
mask_ab = cv2.bitwise_or(mask_a, mask_b)       # 黄 または 緑
```

`cv2.bitwise_and(img, img, mask=mask)` で，マスクが 255 の画素だけ元の色を残し，他を黒にできる．

```python
only_green = cv2.bitwise_and(img, img, mask=mask_b)
```

トラックバーで範囲を調整し，手元の物体だけが白くなるようにしたら，次の **[観察]** に答える．
暗くしたとき・似た色の物が入ったとき・反射したときに **何が壊れるか** を確かめるのがこの演習の目的．

### [観察]

1. 部屋の照明を暗くする (またはカメラを手で覆って暗くする) と，マスクはどう変わったか．
   H・S・V のどの範囲を広げると耐えられるようになったか．それはなぜか．
2. 抽出したい物体と同じような色の物体 (服，背景など) を画面に入れると何が起きたか．
   HSV の範囲の調整だけで解決できるか．できないなら何の情報が足りないか．
3. 物体をカメラに近づけたり傾けたりして，光の反射 (テカリ) が入ると何が起きたか．

## 04 [課題] 二値化とノイズ除去

ファイル: `second/04_threshold_noise.py`

**課題1** (`threshold_numpy`) で二値化を numpy で書き，**課題2** (`opening`) で収縮と膨張を組み合わせ，
**課題3** (`add_noise`) でノイズを加え，**課題4** (`to_odd_ksize`) のバグを直す．

### 二値化

閾値より明るい画素を 255，暗い画素を 0 にする．OpenCV では `cv2.threshold` を使う．

```python
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)   # 100 より大きい画素を 255 に
```

`cv2.threshold` は2つの値を返す (1つ目は使った閾値)．使わない値は `_` で受け取る習慣がある．

### ノイズを加える

一部の画素をランダムに選ぶには，乱数と比較して bool 配列を作る．

```python
rng = np.random.default_rng()
selected = rng.random(gray.shape) < 0.05     # 約 5% の画素が True
gray2 = gray.copy()
gray2[selected] = 0                          # 選ばれた画素を黒にする
```

### メディアンフィルタ

周りの画素の **中央値** に置き換える．孤立した点 (ノイズ) を消せる．
カーネルの大きさ (周りの何画素を見るか) は **3 以上の奇数** でなければならない．

```python
smooth = cv2.medianBlur(binary, 5)           # 5x5 の範囲の中央値
cv2.medianBlur(binary, 4)
# → cv2.error: ... (ksize % 2 == 1) ...      (偶数はエラー)
```

### 収縮と膨張

| 処理 | 関数 | 働き |
| --- | --- | --- |
| 収縮 | `cv2.erode` | 周りに1つでも黒があれば黒にする → 白い領域がやせる |
| 膨張 | `cv2.dilate` | 周りに1つでも白があれば白にする → 白い領域が太る |

```python
kernel = np.ones((5, 5), np.uint8)           # 「周り」の範囲 (5x5 の正方形)
thin = cv2.erode(binary, kernel)
thick = cv2.dilate(binary, kernel)
```

収縮 → 膨張 の順に行うと **オープニング**，膨張 → 収縮 の順だと **クロージング** と呼ぶ．
OpenCV ではまとめて `cv2.morphologyEx` でも書ける．

```python
opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)    # 小さな白い点が消える
closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)   # 白い領域の小さな穴が埋まる
```

トラックバーで閾値・ノイズ量・カーネルの大きさを動かし，次の **[観察]** に答える．

### [観察]

1. 白い紙の上に黒いペンを置いて二値化し，threshold を調整した．
   そのあと手で紙に影を落とすと何が起きたか．1つの閾値で画面全体をうまく分けられるか．
2. noise_% を大きくしていったとき，median と opening のどちらがノイズに強かったか．
   「白い点」と「黒い点 (白い物体に開いた穴)」で違いはあったか．
3. open_k を大きくしていくと，ノイズ以外に何が消えたか．

## 05 ラベリング

ファイル: `second/05_color_labeling.py`

03 の HSV マスクで対象の色の画素を取り出し，**つながった白い領域ごとに番号 (ラベル) を振って**，
領域ごとの位置・大きさ・重心を求める．面積の大きい順に `n` 個の領域を枠で囲む．

### connectedComponentsWithStats

```python
mask = np.zeros((6, 8), np.uint8)
mask[1:3, 1:3] = 255          # 2x2 の白い領域
mask[3:6, 5:8] = 255          # 3x3 の白い領域

n_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask)
print(n_labels)               # → 3      (背景 + 2つの領域)
print(labels)
# → [[0 0 0 0 0 0 0 0]
#    [0 1 1 0 0 0 0 0]
#    [0 1 1 0 0 0 0 0]
#    [0 0 0 0 0 2 2 2]
#    [0 0 0 0 0 2 2 2]
#    [0 0 0 0 0 2 2 2]]
print(stats)
# → [[ 0  0  8  6 35]         ラベル 0 (背景): 左上x, 左上y, 幅, 高さ, 面積
#    [ 1  1  2  2  4]         ラベル 1
#    [ 5  3  3  3  9]]        ラベル 2
print(centroids[2])           # → [6. 4.]  ラベル 2 の重心 (x, y)
```

| 戻り値 | 内容 |
| --- | --- |
| `n_labels` | ラベルの数 (背景を含む) |
| `labels` | 各画素のラベル番号の画像 |
| `stats` | 各ラベルの `[左上x, 左上y, 幅, 高さ, 面積]` (面積は `stats[:, cv2.CC_STAT_AREA]` でも取れる) |
| `centroids` | 各ラベルの重心 `[x, y]` (小数) |

### 面積の大きい順に並べる (`largest_regions`)

**ラベル 0 は常に背景** (マスクが 0 の画素) で，面積の大きさとは関係ない．
「面積が最大のラベルが背景」と仮定してしまうと，物体をカメラに近づけて画面の大部分を占めたときに，
背景を物体として扱ってしまう．そこで `stats[1:]` でラベル 0 を除いてから並べている．

```python
areas = np.array([35, 4, 9])      # ラベル 0, 1, 2 の面積
print(np.argsort(areas))          # → [1 2 0]    (小さい順に並べたときの添字)
print(np.argsort(-areas))         # → [0 2 1]    (大きい順)
print(1 + np.argsort(-areas[1:])) # → [2 1]      (ラベル 0 を除いて大きい順．添字がずれるので 1 を足す)
```

### [観察]

1. 物体をゆっくり動かしたとき，重心の位置 (黄色の点) はフレームごとにどの程度ぶれたか．
   物体が止まっていてもぶれるなら，その原因は何か．
2. 物体を手で半分隠すと，外接矩形と重心はどうなったか．物体が2つに分かれて見えたときは?
3. 同じ色の物体を2つ画面に入れ，交差させるように動かすと，「どちらの物体がどちらか」を区別し続けられるか．

## 06 色の物体でボールを動かす

ファイル: `second/06_labeling_app.py`

05 の最も大きい領域の重心 (`largest_region_center`) にボールを置く．
物体が見つからないフレームでは，ボールを画面の中央に置く．
ボールが画面からはみ出さないよう，01 と同じ `clamp_center` で位置を制限している．

### [観察]

1. 物体を止めたまま持っていても，ボールは震えたか．震えるなら，その原因は何か．
2. 物体を一瞬手で隠してから，別の場所で再び見せると，ボールはどう動いたか．

## 07 [課題] 複数の色を同時に追跡する

ファイル: `second/07_multi_color.py`

色ごとの HSV の範囲を辞書 `hsv_ranges` (main の中にある) で持ち，それぞれの色の最も大きい領域の重心に，その色の円を描く．
**課題1** (`detect_colors`) で色ごとの重心を求め，**課題2** (`draw_centers`) で円を描く．
最も大きい領域の重心を求める関数 `largest_region_center` は 06 と同じものを用意してある．

### 辞書を for で回して結果を辞書にまとめる

`.items()` で色の名前と範囲を同時に取り出し，結果も色の名前をキーにした辞書に入れる．
HSV への変換は色ごとにやり直さず，ループの前に1回だけ行う．

```python
RANGES = {
    "yellow": {"lower": [20, 80, 80], "upper": [35, 255, 255]},
    "green": {"lower": [40, 80, 80], "upper": [80, 255, 255]},
}

hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)          # 変換は1回だけ
areas = {}
for name, r in RANGES.items():
    mask = cv2.inRange(hsv, np.array(r["lower"]), np.array(r["upper"]))
    areas[name] = int(np.count_nonzero(mask))         # 白い画素の数
print(areas)                   # → {'yellow': 1234, 'green': 56} など
```

### 値が無いとき (None)

見つからなかった色は `None` になる．描く前に `is None` / `is not None` で確かめる．

```python
found = {"red": (120.5, 80.2), "blue": None}
for name, pos in found.items():
    if pos is None:
        continue                               # 次の色へ
    print(name, int(pos[0]), int(pos[1]))      # → red 120 80
```

### [観察]

1. 3色の物体を用意し，すべてを同時に検出できる HSV の範囲を探せ．
   ある色の範囲を広げると別の色を誤検出する，ということは起きたか．
2. 背景 (服，机，壁) の中に，誤検出されやすい色はあったか．

## 08 背景差分

ファイル: `second/08_background_subtraction.py`

色を使わずに「動いているもの」を取り出す方法を4つ並べて比べる．(a)〜(c) は簡単な計算で自分で書いたもの，
(d) は OpenCV の背景差分．

| 方法 | 背景の作り方 | 得意 | 苦手 |
| --- | --- | --- | --- |
| (a) 静的背景差分 | 最初のフレーム (撮り直すときは起動し直す) | 止まっている物も検出できる | 照明の変化，カメラの移動 |
| (b) フレーム間差分 | 1つ前のフレーム | 照明のゆっくりした変化 | 物の内側が抜ける，止まると消える |
| (c) 移動平均背景 | `(1-α)·背景 + α·現在` で少しずつ更新 | ゆっくりした変化に追従 | α の選び方，止まった物が背景になる |
| (d) MOG | 画素ごとに色の分布 (混合ガウス分布) を学習 | 揺れる木の葉など背景が複数の色をとる場合 | 計算が重い，学習に時間がかかる |

### 差の絶対値 (`diff_mask`)

`uint8` どうしの引き算は，負になると 256 を足した値に回り込む (第1週 09)．そのため `cv2.absdiff` を使っている．

```python
a = np.array([[100, 50]], np.uint8)
b = np.array([[120, 40]], np.uint8)
print(a - b)                   # → [[236  10]]   (-20 が回り込んだ)
print(np.abs(a - b))           # → [[236  10]]   (回り込んだ後に abs をとっても戻らない)
print(cv2.absdiff(a, b))       # → [[20 10]]
```

### 小数のまま更新する (`update_background`)

少しずつ更新する値を `uint8` で持つと，小さな変化が切り捨てられて変わらなくなる．そのため背景は `float32` で持っている．

```python
v = np.array([100], np.uint8)
v = (0.99 * v + 0.01 * 150).astype(np.uint8)    # 100.5 → 100 に切り捨て
print(v)                       # → [100]   (何回くり返しても 100 のまま)

w = np.array([100], np.float32)
w = (0.99 * w + 0.01 * 150).astype(np.float32)
print(w)                       # → [100.5]
```

### OpenCV の背景差分器

```python
subtractor = cv2.bgsegm.createBackgroundSubtractorMOG()   # 背景差分器を作る
fg_mask = subtractor.apply(frame)                          # 1フレーム入れると前景のマスクが返る
```

背景差分器は，`apply` を呼ぶたびにそれまでに見たフレームから背景を学習していく．
そのため `process` の外で1回だけ作り，毎フレーム同じものに `apply` する．
`process` の中で毎回作り直すと，学習した背景が毎回捨てられて何も検出できなくなる．

### [観察]

1. カメラの前で手をゆっくり動かしたときと，素早く動かしたとき，(b) フレーム間差分では手のどの部分が検出されたか．
   手の内側が抜けるのはなぜか．
2. 画面に入ってきた人 (物) がしばらく静止すると，(a)(c)(d) はそれぞれどうなったか．
   `alpha_%` を変えると (c) はどう変わったか．
3. 部屋の照明を点けたり消したりすると，4つの方法はそれぞれどうなったか．
4. カメラを手で持って揺らすと，4つの方法はそれぞれどうなったか．
   背景差分を「動いているもの」の検出に使えるのは，どういう条件のときか．

## 09 オプティカルフロー

ファイル: `second/09_optical_flow.py`

画像の中の点が，次のフレームでどこに動いたかを求める．

### しくみ

`cv2.calcOpticalFlowPyrLK` は **Lucas-Kanade 法** で点を追跡する．
「点が少し動いても明るさは変わらない」と仮定し，点の周りの小さな窓 (`winSize`) の中の明るさの変化から動きを求める．

- **追跡しやすい点** は角のような点．白い壁のように模様の無い場所や，まっすぐな辺の上の点は，
  どちらに動いたかが見た目から決まらない．`cv2.goodFeaturesToTrack` はそのような点を避けて，角のような点を選ぶ
- 動きが大きいと仮定が成り立たなくなるので，画像を縮小した **ピラミッド** で大まかな動きから求める
  (`maxLevel` がピラミッドの段数)

### 関数と配列の形

```python
pts = cv2.goodFeaturesToTrack(gray, maxCorners=100, qualityLevel=0.3, minDistance=7)
print(pts.shape)               # → (N, 1, 2)    N 個の点の (x, y)．見つからなければ None

nxt, status, err = cv2.calcOpticalFlowPyrLK(prev_gray, gray, pts, None,
                                            winSize=(15, 15), maxLevel=2)
print(nxt.shape)               # → (N, 1, 2)    各点の移動先
print(status.shape)            # → (N, 1)       追跡に成功したら 1，失敗したら 0
```

`(N, 1, 2)` の配列は `reshape(-1, 2)` で `(N, 2)` にしてから使い，
`status.ravel() == 1` の bool 配列で追跡に成功した点だけを取り出している (`track`)．

```python
p = np.array([[[1, 2]], [[3, 4]], [[5, 6]]], np.float32)   # (3, 1, 2)
st = np.array([[0], [1], [1]], np.uint8)                    # (3, 1)
print(p.reshape(-1, 2))              # → [[1. 2.] [3. 4.] [5. 6.]]   (-1 は「残りから自動で決める」)
print(st.ravel() == 1)               # → [False  True  True]
print(p.reshape(-1, 2)[st.ravel() == 1])   # → [[3. 4.] [5. 6.]]
```

追跡に失敗した点を捨て続けると点は減る一方なので，点が少なくなったとき，または一定フレームごとに点を選び直している．
点を選び直すときは，それまでに描いた線も消している．

### [観察]

1. 白い壁や無地の机をカメラに映すと，点はどこに選ばれたか．
2. `maxLevel` を 0 にして手を素早く動かすと，追跡はどうなったか．`maxLevel` を 3 にすると?
3. カメラ自体を揺らすと，フローはどうなったか．「物体の動き」だけを取り出すには何が必要か．

## 10 動きの向きでボールを動かす

ファイル: `second/10_flow_app.py`

たくさんの点の動きを1つのベクトルにまとめ (`motion_vector`)，その向きにボールを動かす．
まとめ方を2つ用意してあり，トラックバーの `method` で切り替えられる．

```python
d = np.array([[3, 0], [4, 1], [-30, 20]], np.float32)   # 3点の (dx, dy)．最後の点だけ外れている
print(np.linalg.norm(d, axis=1))     # → [ 3.  4.12  36.06]   各点の動きの大きさ
print(np.argmax(np.linalg.norm(d, axis=1)))      # → 2        最も大きく動いた点の添字
print(d[np.argmax(np.linalg.norm(d, axis=1))])   # → [-30. 20.]
print(d.sum(axis=0))                 # → [-23.  21.]          (dx の合計, dy の合計)
```

`axis=0` は「縦方向 (点の方向) にまとめる」，`axis=1` は「横方向 (1点の x, y) にまとめる」．

| method | まとめ方 | 特徴 |
| --- | --- | --- |
| 0 | 最も大きく動いた1点の動き | 追跡を間違えた1点に引きずられる |
| 1 | 全点の動きの合計 | 点の数によって大きさが変わる |

まとめた動きの大きいほうの成分が `threshold` 以上なら，その向きにボールを `step` だけ動かす (`direction`)．

### [観察]

1. `method` を 0 と 1 で切り替えて同じ動作 (手を左右に振る) をすると，誤ってボールが動くことが多いのはどちらか．
   上の例と関係づけて説明せよ．
2. `method` が 1 のとき，`threshold` を画面に映る物の多い場所と少ない場所 (白い壁) で同じ値にしてよいか．

## 11 マスクを使った合成

ファイル: `second/11_overlay.py`

四角い画像をそのまま貼ると，背景の黒い部分まで貼られてしまう．
「黒でない部分」を白にしたマスクを作り，その部分だけをカメラの映像と置き換える．
アプリ制作でキャラクターやエフェクトを重ねるときに使える．

### ビット演算による合成

`cv2.bitwise_and(画像, 画像, mask=マスク)` は，マスクが白の画素だけ元の値を残し，それ以外を黒 (0) にする．
`cv2.bitwise_not` はマスクの白黒を反転する．これらを組み合わせて，次の手順で合成している．

1. 合成したい画像をグレースケールにして二値化し，「黒でない部分」が白のマスク `mask` を作る
2. `bitwise_and(fg, fg, mask=mask)` で，合成したい画像の前景だけを取り出す (背景は黒になる)
3. カメラの映像の左上の領域 `roi` を，反転したマスク `mask_inv` で `bitwise_and` し，前景が来る部分を黒にする
4. 2 と 3 を `cv2.add` で足す．黒 (0) の部分にもう一方の値が入るので，2枚が重なる

```python
a = np.array([[10, 20]], np.uint8)
m = np.array([[255, 0]], np.uint8)
print(cv2.bitwise_and(a, a, mask=m))       # → [[10  0]]   マスクが 0 の画素は 0 になる
print(cv2.bitwise_not(m))                  # → [[  0 255]]
print(cv2.add(np.array([[10, 0]], np.uint8), np.array([[0, 99]], np.uint8)))   # → [[10 99]]
```

合成する画像の大きさだけ，カメラの映像の左上を切り出している (`frame[0:h, 0:w]`)．
カメラの映像より大きい画像は合成できない．

## 発展課題: numpy だけで収縮・膨張・メディアン

ファイル: `second/advanced/erode_numpy.py`

収縮・膨張・メディアンフィルタを numpy だけで書き，OpenCV と結果と速度を比べる．
1画素ずつ for 文で回すのではなく，「画像を少しずつずらしたもの」を重ねて最小値・最大値・中央値をとる．

```python
p = np.pad(img, 1, mode="edge")     # 周りに1画素ずつ，端の値をコピーして広げる
print(img.shape, p.shape)           # → (H, W) (H+2, W+2)
above = p[0:H, 1:W+1]               # 各画素の位置に「1つ上の画素」が来る画像
stack = np.stack([a, b, c])         # 同じ形の配列を重ねて (3, H, W) にする
print(stack.min(axis=0).shape)      # → (H, W)   (重ねた方向に最小値をとる)
```

## 発展課題: numpy だけで Harris コーナー検出

ファイル: `second/advanced/harris_numpy.py`

各画素の周りの窓で，x 方向・y 方向の微分 $I_x, I_y$ から行列 (構造テンソル)

$$ M = \begin{pmatrix} \sum I_x^2 & \sum I_x I_y \\ \sum I_x I_y & \sum I_y^2 \end{pmatrix} $$

を作り，Harris の応答 $R = \det M - k\,(\mathrm{tr}\,M)^2$ を全画素について numpy だけで求める．
$R$ が大きい点がコーナー．`cv2.cornerHarris` と結果を比べ，ファイル末尾の考察に答える．
