# 第1週: Python と OpenCV の基礎

この週の目標は次の2つ．

- 第2週以降で使う Python と numpy の書き方に慣れる
- 「画像は numpy 配列である」ことを理解したうえで，色の抽出・二値化・ノイズ除去を自分で動かし，
  **どんなときに失敗するか** を観察する

## 進め方

各ファイルには `...` (TODO) の穴があり，課題ごとに **期待する出力** が書いてある．
穴を埋めて実行し，`OK 課題◯` がすべて表示されれば完了．

```shell
cd first/python_basics
uv run python 01_variables.py
```

- 上から順に進める．途中で `AssertionError` が出たら，メッセージに書かれた課題を直す
- `[バグ修正]` の課題は，最初はわざとエラーになる．エラーメッセージを **一番下の行から** 読み，
  「何が (〜Error)」「どこで (line ◯)」起きたかを確認してから直す
- 生成AI (ChatGPT, Gemini など) を使ってよい．ただし `[観察]` の問いは，
  自分のカメラで実際に試した結果を書くこと．AI はあなたの部屋の照明を知らない

| ファイル | 内容 | 目安 |
| --- | --- | --- |
| `python_basics/01_variables.py` | 変数・型・f文字列 | 経験者は飛ばしてよい |
| `python_basics/02_operators.py` | 演算子，`//` と `/` の違い | 経験者は飛ばしてよい |
| `python_basics/03_containers.py` | リスト・スライス・タプル・辞書 | |
| `python_basics/04_control_flow.py` | if / for / while, FizzBuzz | |
| `python_basics/05_functions.py` | 関数，関数を引数として渡す | **必須** |
| `python_basics/06_modules/` | 別ファイルの関数を import する | **必須** |
| `python_basics/07_numpy_basics.py` | numpy 配列の作成・取り出し・計算 | **必須** |
| `python_basics/08_numpy_mask.py` | 比較・bool 配列・np.where | **必須** |
| `python_basics/09_numpy_image.py` | 画像を numpy 配列として扱う | **必須** |
| `opencv/01_hsv_color.py` | HSV による色の抽出 (カメラ) | **必須** |
| `opencv/02_threshold_noise.py` | 二値化とノイズ除去 (カメラ) | **必須** |
| `advanced/erode_numpy.py` | 発展: numpy だけで収縮・膨張・メディアン | 早く終わった人向け |

---

## 01 変数と型

- Python では値を代入したときに変数が作られる．C 言語のような型の宣言は要らない
- 主な型は `int` (整数), `float` (小数), `str` (文字列), `bool` (`True` / `False`)．`type(x)` で確認できる
- 型の変換: `int("123")`, `str(640)`, `float(3)`．`int(3.7)` は **切り捨て** で `3` になる
- f文字列: `f"x = {x}"` で文字列に値を埋め込める．`{fps:.2f}` で小数点以下2桁

**よくあるエラー**: `"幅は" + 640` → `TypeError: can only concatenate str (not "int") to str`．
文字列と数値は `+` でつなげない．`str(640)` で文字列にするか，f文字列を使う．

## 02 演算子

| 演算子 | 意味 | 例 |
| --- | --- | --- |
| `/` | 割り算 (結果は必ず float) | `7 / 2` → `3.5` |
| `//` | 切り捨て除算 | `7 // 2` → `3` |
| `%` | 余り | `7 % 2` → `1` |
| `**` | べき乗 | `2 ** 10` → `1024` |
| `+=` など | `a += b` は `a = a + b` | |

画像の座標や配列の添字は整数でなければならない．中心座標や半分の大きさを求めるときは `//` を使う．

## 03 リスト・タプル・辞書

- **リスト** `[10, 20, 30]`: 先頭が 0 番目．`xs[-1]` で末尾．`len(xs)` で要素数．`xs.append(v)` で追加
- **スライス** `xs[開始:終了:ステップ]`: 終了の位置は **含まない**．省略すると先頭/末尾．`xs[::-1]` で逆順
- **タプル** `(120, 80)`: 作った後で変更できないリスト．`x, y = point` で取り出せる (アンパック)．
  OpenCV では座標 `(x, y)` や色 `(B, G, R)` をタプルで渡す
- **辞書** `{"blue": 110}`: キーで値を取り出す．`d["key"]` はキーが無いと `KeyError`，
  `d.get("key", 既定値)` はキーが無いと既定値を返す

**よくあるエラー**: `xs[len(xs)]` → `IndexError: list index out of range`．
要素が5個なら添字は 0〜4．

## 04 制御構文

Python は **インデント (字下げ) でブロックを表す**．`:` の次の行は必ずスペース4つで字下げする．

```python
if area >= 1000:
    size = "large"
elif area >= 300:
    size = "medium"
else:
    size = "small"

for i in range(1, 11):      # 1, 2, ..., 10 (11 は含まない)
    total += i ** 2

for name, value in d.items():   # 辞書のキーと値を同時に取り出す
    ...

while True:                 # カメラの処理はこの形でくり返す
    ...
    if key == ord("q"):
        break               # ループを抜ける
```

- 条件は `and` / `or` / `not` で組み合わせる．`10 <= x < 50` のようにまとめて書ける
- `0`, `""`, `[]`, `None` は条件式の中では偽として扱われる
- `range(9)` は 0〜8．**終わりの値は含まない** (スライスと同じ)

## 05 関数

```python
def clamp(v, lo, hi):
    return max(lo, min(v, hi))
```

- `return` で値を返す．`return` を書かないと `None` が返る．
  **`print` は画面に表示するだけで，値を返さない** (バグ修正5-1)
- `return x, y` と書くとタプルで返る
- 関数は値として他の関数に渡せる．第2週からは次のように **自分で書いた `process` 関数をカメラのループに渡す**

```python
from common import run

def process(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

run(process)     # process() ではない．関数そのものを渡す
```

## 06 モジュール

`06_modules/` で実行する．

```shell
cd first/python_basics/06_modules
uv run python use_module.py
uv run python exercise.py
```

- `from A import a` で，同じフォルダの `A.py` に書かれた関数 `a` を使える
- `from modules.B import b` で，`modules` フォルダの中の `B.py` の関数 `b` を使える
- `if __name__ == "__main__":` の中は **そのファイルを直接実行したときだけ** 動く．
  他のファイルから import されたときは動かない．関数の「試し打ち」を書いておく場所として使う
- 第2週以降の `from common import run` も同じ仕組み．`common/` は授業用に用意した共通部品で，
  `uv sync` を実行するとどのフォルダからでも import できるようになっている

## 07 numpy の基本

numpy は数値の配列を高速に計算するためのライブラリ．`import numpy as np` で使う．

- 作成: `np.array([[1, 2], [3, 4]])`, `np.arange(0, 20, 5)`, `np.zeros((h, w))`, `np.full(shape, 値)`
- 形状: `arr.shape` → `(行数, 列数)`．画像なら `(高さ, 幅, チャンネル数)`
- 取り出し: `arr[行, 列]`．`arr[:, 1]` は全行の1列目．`arr[1:3, 0:2]` は部分配列 (**画像の切り出しと同じ**)
- 計算: `+ - * /` は要素ごと．行列の積は `np.dot(a, b)` または `a @ b`．
  `np.mean`, `np.max`, `np.sort` なども使える
- **ブロードキャスト**: 形の違う配列どうしの計算で，サイズ1の軸を自動で引き伸ばす．
  `img + np.array([50, 0, -50])` は全画素の B, G, R にそれぞれ足し算する

**よくあるエラー**: `ValueError: shapes (2,3) and (2,3) not aligned`．
行列の積は (前の列数) = (後ろの行数) でなければならない．`.T` で転置する．

## 08 numpy の比較とマスク

- `arr > 4` は要素ごとの比較になり，`True` / `False` の配列 (bool 配列) ができる
- `arr[mask]` で `True` の要素だけ取り出せる．`mask.sum()` で `True` の個数
- 条件の組み合わせは `&` (かつ), `|` (または)．各条件を `()` で囲む:
  `(hue >= 10) & (hue <= 40)` ← これが `cv2.inRange` の中身
- `np.where(条件, 真の値, 偽の値)` で値を置き換える ← これが二値化
- `np.where(条件)` と引数1つだと，条件を満たす要素の添字 `(行の配列, 列の配列)` が返る
- `if arr > 4:` はエラー．「1つでも」なら `.any()`，「すべて」なら `.all()` を使う

## 09 画像は numpy 配列

```python
img = cv2.imread("keio.png")   # 失敗すると None が返る (パスの間違いが多い)
img.shape                      # (高さ, 幅, 3)
img[y, x]                      # 画素 (B, G, R)．添字は y が先
cv2.circle(img, (x, y), ...)   # OpenCV の関数に座標を渡すときは x が先
```

- 画像の値は `uint8` (0〜255 の整数)．**255 を超えると 0 に戻る (オーバーフロー)**．
  明るさを足すときは `cv2.add` を使うか，一度 `int` にして `np.clip` する (バグ修正5-1)
- チャンネルの並びは **B, G, R**．`img[:, :, ::-1]` で RGB になる
- `img[:, ::-1]` で左右反転，`img[y0:y1, x0:x1]` で切り出し

---

## OpenCV-1 HSV による色の抽出 (`opencv/01_hsv_color.py`)

```shell
cd first/opencv
uv run python 01_hsv_color.py
```

BGR のままだと「明るいオレンジ」と「暗いオレンジ」は全く違う値になる．
HSV は色を **H (色相: 何色か), S (彩度: 鮮やかさ), V (明度: 明るさ)** に分けるので，
H の範囲で「何色か」を指定しやすい．

- OpenCV の H は 0〜179 (角度 0〜360° の半分)．S, V は 0〜255
- 赤は H が 0 付近と 179 付近の **両端にまたがる** ので，範囲を2つに分けてマスクを OR する (課題2)
- `cv2.inRange(hsv, lower, upper)` で範囲内を 255 にしたマスクができる
- `cv2.bitwise_and(frame, frame, mask=mask)` でマスクの部分だけ元の色を残せる

トラックバーで範囲を調整し，手元の物体だけが白くなるようにしたら，ファイル末尾の **[観察]** に答える．
暗くしたとき・似た色の物が入ったとき・反射したときに **何が壊れるか** を確かめるのがこの演習の目的．

## OpenCV-2 二値化とノイズ除去 (`opencv/02_threshold_noise.py`)

- **二値化**: 閾値より明るい画素を 255，暗い画素を 0 にする．`np.where` で書ける (課題1)
- **ノイズ**: 二値化の結果には小さな点 (ノイズ) が残る．わざとノイズを加えて (課題3) 除去の効果を比べる
- **メディアンフィルタ** `cv2.medianBlur`: 周りの画素の中央値に置き換える．カーネルの大きさは3以上の奇数 (課題4)
- **収縮** `cv2.erode`: 周りに1つでも黒があれば黒にする → 白い領域がやせる
- **膨張** `cv2.dilate`: 周りに1つでも白があれば白にする → 白い領域が太る
- **オープニング** = 収縮 → 膨張: 小さな白い点が消え，大きな領域はほぼ元の形に戻る (課題2)．
  逆の順 (膨張 → 収縮) は **クロージング** で，白い領域に開いた小さな穴が埋まる

トラックバーで閾値・ノイズ量・カーネルの大きさを動かし，**[観察]** に答える．

## 発展課題 (`advanced/erode_numpy.py`)

収縮・膨張・メディアンフィルタを numpy だけで書き，OpenCV と結果と速度を比べる．
1画素ずつ for 文で回すのではなく，「画像を少しずつずらしたもの」を重ねて最小値・最大値・中央値をとる．
