# 第1週: Python と numpy の基礎

この週の目標は次の2つ．

- 第2週以降で使う Python と numpy の書き方に慣れる
- 「画像は numpy 配列である」ことを理解し，画像の読み込み・表示・切り出しを自分で書けるようになる

## 進め方

各ファイルの課題は関数になっていて，`...` (TODO) の穴がある．
この README の説明とコード例を読み，穴を埋めて実行する．
ファイル末尾の `if __name__ == "__main__":` の中で各課題の関数が順番に呼ばれ，結果が表示される．
課題文のとおりの結果になっているかを自分で確かめる．

```shell
cd first/python_basics
uv run 01_variables.py
```

穴を埋めていない課題は `Ellipsis` (`...` のこと) と表示される．

```
課題1-1: Ellipsis
課題2-1: Ellipsis
```

ある課題でエラーが出て先に進めなくなったら，`if __name__ == "__main__":` の中のその課題の行を
コメントアウトすると，その課題を飛ばして他の課題を先に進められる．

```python
if __name__ == "__main__":
    print("課題1-1:", task_1_1())
    # print("課題2-1:", task_2_1())    ← 後回しにする
    print("課題2-2:", task_2_2())
```

- `[バグ修正]` の課題は，最初はわざとエラーになる．エラーメッセージを **一番下の行から** 読み，
  「何が (〜Error)」「どこで (line ◯)」起きたかを確認してから直す
- 第1週の内容は基礎なので，生成AI (ChatGPT, Gemini など) は基本的に使わず，
  この README とエラーメッセージを手がかりに自分で書くこと

| ファイル | 内容 |
| --- | --- |
| `python_basics/01_variables.py` | 変数・型・f文字列 |
| `python_basics/02_operators.py` | 演算子 |
| `python_basics/03_containers.py` | リスト・スライス・タプル・辞書 |
| `python_basics/04_control_flow.py` | if / for / while |
| `python_basics/05_functions.py` | 関数，関数を引数として渡す |
| `python_basics/06_modules/` | 別ファイルの関数を import する |
| `python_basics/07_numpy_basics.py` | numpy 配列の作成・取り出し・計算 |
| `python_basics/08_numpy_mask.py` | 比較・bool 配列・np.where |
| `python_basics/09_numpy_image.py` | 画像を numpy 配列として扱う |

以下のコード例では，`print` の出力を `# → ` の後ろに書いている．

---

## 01 変数と型

### 変数

Python では，値を代入したときに変数が作られる．C 言語のような型の宣言 (`int x;`) は要らない．

```python
x = 3
y = x * 2 + 1
print(x, y)            # → 3 7

x = x + 10             # 右辺を計算してから x に入れ直す
print(x)               # → 13
```

### 型

値にはそれぞれ型がある．`type(値)` で確認できる．

| 型 | 意味 | 例 |
| --- | --- | --- |
| `int` | 整数 | `3`, `-10` |
| `float` | 小数 | `2.5`, `1.0` |
| `str` | 文字列 | `"abc"`, `'カメラ'` |
| `bool` | 真偽値 | `True`, `False` |

```python
print(type(3))         # → <class 'int'>
print(type(2.5))       # → <class 'float'>
print(type("abc"))     # → <class 'str'>
print(type(True))      # → <class 'bool'>
```

型は `int()`, `float()`, `str()` で変換できる．

```python
s = "42"
print(s + s)           # → 4242      (文字列どうしの + は連結)
n = int(s)
print(n + n)           # → 84        (整数どうしの + は足し算)

print(float(3))        # → 3.0
print(str(100) + "円")  # → 100円
print(int(9.99))       # → 9         (小数を int にすると切り捨て)
print(int(-2.5))       # → -2        (0 に近い方へ切り捨て)
```

**よくあるエラー**: 文字列と数値は `+` でつなげない．

```python
age = 20
print("年齢は" + age)
# → TypeError: can only concatenate str (not "int") to str
#   「文字列には文字列しか連結できない (int が来た)」という意味
```

### f文字列

文字列の前に `f` を付けると，`{}` の中に変数や式を書いて値を埋め込める．

```python
name = "cup"
x, y = 120, 85
print(f"{name} is at ({x}, {y})")    # → cup is at (120, 85)
print(f"x + y = {x + y}")            # → x + y = 205

ratio = 0.123456
print(f"{ratio:.3f}")                # → 0.123     (小数点以下3桁)
print(f"{ratio:.1f}")                # → 0.1       (小数点以下1桁)
```

## 02 演算子

### 算術演算子

| 演算子 | 意味 | 例 | 結果 |
| --- | --- | --- | --- |
| `+` `-` `*` | 足し算・引き算・掛け算 | `7 * 2` | `14` |
| `/` | 割り算 (結果は必ず float) | `7 / 2` | `3.5` |
| `//` | 切り捨て除算 | `7 // 2` | `3` |
| `%` | 余り | `7 % 2` | `1` |
| `**` | べき乗 | `2 ** 10` | `1024` |

```python
print(9 / 3)           # → 3.0       (割り切れても / の結果は float)
print(9 // 4)          # → 2
print(9 % 4)           # → 1
print(type(9 // 4))    # → <class 'int'>
```

`%` は「◯回に1回だけ処理する」ときによく使う．

```python
for i in range(7):
    if i % 3 == 0:     # 3 で割った余りが 0 → 0, 3, 6 のときだけ
        print(i)
# → 0
# → 3
# → 6
```

### 代入演算子

`a += b` は `a = a + b` と同じ．`-=`, `*=`, `/=`, `//=` も同様．

```python
count = 0
count += 1
count += 1
print(count)           # → 2

size = 100
size -= 30
print(size)            # → 70
```

### 文字列の演算

```python
print("Robot" + "Vision")   # → RobotVision    (連結)
print("ab" * 3)             # → ababab         (繰り返し)
print("=" * 5)              # → =====
```

## 03 リスト・タプル・辞書

### リストとインデックス

`[]` の中に値を `,` で区切って並べる．**先頭は 0 番目**．負の数を使うと末尾から数える．

```python
fruits = ["apple", "banana", "cherry", "durian"]
print(fruits[0])       # → apple
print(fruits[2])       # → cherry
print(fruits[-1])      # → durian    (末尾)
print(fruits[-2])      # → cherry    (末尾から2番目)
print(len(fruits))     # → 4         (要素数)
```

要素が4個なら，使える添字は `0` 〜 `3` (または `-1` 〜 `-4`)．範囲外を指定するとエラーになる．

```python
print(fruits[4])
# → IndexError: list index out of range
```

添字は **整数でなければならない**．`/` の結果は割り切れても float になるので，
真ん中の位置や半分の大きさを添字に使うときは `//` を使う (画像の座標でも同じ)．

```python
print(len(fruits) / 2)         # → 2.0
print(fruits[len(fruits) / 2])
# → TypeError: list indices must be integers or slices, not float
print(fruits[len(fruits) // 2])  # → cherry
```

### スライス

`リスト[開始:終了:ステップ]` で複数の要素をまとめて取り出す．**終了の位置は含まない**．

```python
nums = [0, 1, 2, 3, 4, 5, 6, 7]
print(nums[2:5])       # → [2, 3, 4]       (2番目から，5番目の手前まで)
print(nums[:3])        # → [0, 1, 2]       (開始を省略すると先頭から)
print(nums[5:])        # → [5, 6, 7]       (終了を省略すると末尾まで)
print(nums[::2])       # → [0, 2, 4, 6]    (1つおき)
print(nums[1::3])      # → [1, 4, 7]       (1番目から2つおき)
print(nums[::-1])      # → [7, 6, 5, 4, 3, 2, 1, 0]   (ステップが負だと逆順)
print(nums[::-3])      # → [7, 4, 1]       (末尾から2つおき)
```

### リストへの追加と2次元リスト

```python
names = ["ken"]
names.append("yui")    # 末尾に追加 (names そのものが変わる)
names.append("rio")
print(names)           # → ['ken', 'yui', 'rio']
```

リストの中にリストを入れると2次元になる．`リスト[行][列]` で取り出す．

```python
table = [
    [10, 11, 12],      # 0 行目
    [20, 21, 22],      # 1 行目
]
print(table[0])        # → [10, 11, 12]
print(table[1][0])     # → 20        (1 行目の 0 列目)
print(table[0][2])     # → 12        (0 行目の 2 列目)
```

### タプル

`()` で作る．リストと似ているが，**作った後で中身を変更できない**．
OpenCV では座標 `(x, y)` や色 `(B, G, R)` をタプルで渡す．

```python
size = (640, 480)
print(size[0])         # → 640

w, h = size            # アンパック: 要素を複数の変数に一度に取り出す
print(w, h)            # → 640 480

pair = (h, w)          # 新しいタプルを作る
print(pair)            # → (480, 640)

size[0] = 1280
# → TypeError: 'tuple' object does not support item assignment
```

### 辞書

`{キー: 値}` の組を格納する．`辞書[キー]` で値を取り出す．

```python
scores = {"math": 80, "english": 65}
print(scores["math"])          # → 80

scores["science"] = 90         # 新しいキーを追加
scores["english"] = 70         # 既存のキーの値を上書き
print(scores)                  # → {'math': 80, 'english': 70, 'science': 90}
print(list(scores.keys()))     # → ['math', 'english', 'science']
```

値に辞書やリストを入れることもできる．`[]` を続けて書いて奥まで取り出す．

```python
camera = {
    "front": {"size": [640, 480], "fps": 30},
    "side": {"size": [320, 240], "fps": 15},
}
print(camera["side"])              # → {'size': [320, 240], 'fps': 15}
print(camera["side"]["size"])      # → [320, 240]
print(camera["front"]["size"][0])  # → 640
```

無いキーを `[]` で指定するとエラーになる．`.get(キー, 既定値)` を使うと，無いときに既定値が返る．

```python
print(scores["art"])               # → KeyError: 'art'
print(scores.get("art"))           # → None
print(scores.get("art", 0))        # → 0
print(scores.get("math", 0))       # → 80     (あれば普通に取り出せる)
```

## 04 制御構文

Python は **インデント (字下げ) でブロックを表す**．`:` の次の行は必ずスペース4つで字下げする．
字下げが終わったところでブロックも終わる．

### if 文

```python
temp = 18
if temp >= 25:
    print("暑い")
elif temp >= 15:       # 上の条件が偽で，この条件が真のとき
    print("ちょうどよい")
else:                  # どの条件も偽のとき
    print("寒い")
# → ちょうどよい
```

条件には比較演算子と論理演算子を使う．

| 演算子 | 意味 | 例 |
| --- | --- | --- |
| `==` `!=` | 等しい・等しくない | `x == 3` |
| `<` `<=` `>` `>=` | 大小 | `x >= 10` |
| `in` | 含まれる | `"a" in ["a", "b"]` |
| `and` `or` `not` | かつ・または・否定 | `x > 0 and x < 10` |

```python
x = 7
print(0 < x and x < 10)    # → True
print(0 < x < 10)          # → True     (まとめて書ける)
print(x % 2 == 0)          # → False
print(3 in [1, 2, 3])      # → True
```

### for 文

`for 変数 in リストなど:` で，要素を1つずつ取り出してくり返す．

```python
for name in ["ken", "yui"]:
    print("hello", name)
# → hello ken
# → hello yui
```

`range` で整数の並びを作れる．**終わりの値は含まない** (スライスと同じ)．

```python
print(list(range(4)))          # → [0, 1, 2, 3]
print(list(range(2, 6)))       # → [2, 3, 4, 5]
print(list(range(0, 10, 3)))   # → [0, 3, 6, 9]
```

くり返しながら値を足し込むときは，ループの前に変数を用意しておく．

```python
total = 0
for i in range(1, 4):          # i = 1, 2, 3
    total += i * 10
print(total)                   # → 60   (10 + 20 + 30)
```

条件に合うものだけを集めるときは，空のリストを用意して `append` する．

```python
evens = []
for n in [3, 8, 5, 12, 7]:
    if n % 2 == 0:
        evens.append(n)
print(evens)                   # → [8, 12]
```

辞書の `.items()` を回すと，キーと値を同時に取り出せる．

```python
prices = {"apple": 120, "melon": 800, "lemon": 90}
for fruit, price in prices.items():
    if price < 100:
        print(fruit)
# → lemon
```

### while 文と break

`while 条件:` は条件が真の間くり返す．`break` でループを途中で抜ける．

```python
x = 1
while x < 50:
    x = x * 3
print(x)                       # → 81   (1 → 3 → 9 → 27 → 81 で 50 以上になり終了)

n = 0
while True:                    # 条件が常に真 = break するまでくり返す
    n += 1
    if n * n > 30:
        break
print(n)                       # → 6
```

カメラの処理も「`q` が押されるまで `while True:` でくり返す」形で書かれている．

### 条件の順番

`if` / `elif` は **上から順に調べ，最初に真になったところだけ** 実行する．
「2 の倍数」と「6 の倍数」のように片方がもう片方を含む条件では，順番によって結果が変わる．

```python
n = 12
if n % 2 == 0:
    print("2の倍数")
elif n % 6 == 0:
    print("6の倍数")           # n = 12 でもここには来ない
# → 2の倍数
```

### print を使ったデバッグ

エラーは出ないのに結果が合わないときは，ループの中で変数を `print` して，何が起きているかを確かめる．

```python
total = 0
for i in range(5):
    print("i =", i, "total =", total)   # 途中経過を表示
    total += i
```

## 05 関数

### 定義と return

`def 関数名(引数):` で定義し，`return` で結果を返す．

```python
def triple(x):
    return 3 * x

print(triple(5))               # → 15
y = triple(2) + 1
print(y)                       # → 7
```

引数は複数とれる．

```python
def rect_area(w, h):
    return w * h

print(rect_area(4, 5))         # → 20
```

`return` の中で `if` を使ったり，組み込み関数 `max`, `min`, `abs` を使ったりできる．

```python
def larger(a, b):
    if a > b:
        return a
    return b                   # a > b でなければここに来る

print(larger(3, 8))            # → 8
print(max(3, 8), min(3, 8))    # → 8 3
print(abs(-4))                 # → 4
```

### print と return の違い

**`print` は画面に表示するだけで，値を返さない**．`return` を書かない関数は `None` を返す．

```python
def show_sum(a, b):
    print(a + b)               # 表示するだけ

result = show_sum(1, 2)        # → 3      (関数の中の print が表示)
print(result)                  # → None   (値は返ってきていない)
```

### 複数の値を返す

`return a, b` と書くとタプルで返る．受け取るときはアンパックできる．

```python
def min_max(values):
    return min(values), max(values)

print(min_max([4, 9, 1]))      # → (1, 9)
lo, hi = min_max([4, 9, 1])
print(lo, hi)                  # → 1 9
```

### 関数を引数として渡す

Python では関数も値として扱える．**関数名の後に `()` を付けると「呼ぶ」，付けないと「関数そのもの」**．

```python
def add_one(x):
    return x + 1

def apply_twice(func, x):
    return func(func(x))       # 受け取った関数を2回呼ぶ

print(apply_twice(add_one, 5))     # → 7
print(apply_twice(triple, 2))      # → 18
```

第2週からは，**自分で書いた `process` 関数をカメラのループに渡す** 形で処理を書く．

```python
from common import run

def process(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

run(process)     # process() ではない．関数そのものを渡す
```

(`common` を import するための準備は 06 で説明する)

## 06 モジュール

`06_modules/` で実行する．

```shell
cd first/python_basics/06_modules
uv run use_module.py
uv run exercise.py
```

### import

別のファイルに書いた関数は `from ファイル名 import 関数名` で読み込める (`.py` は付けない)．

```
06_modules/
├── A.py              def a(): ...
├── use_module.py     ← ここから A.py と modules/B.py の関数を使う
└── modules/
    └── B.py          def b(): ...
```

```python
# use_module.py
from A import a              # 同じフォルダの A.py から関数 a を読み込む
from modules.B import b      # modules フォルダの中の B.py から関数 b を読み込む

a()                          # → Hello A.py
b()                          # → Wow! B.py!?
```

`import numpy as np` のように，モジュール全体を別名で読み込むこともできる．このときは `np.関数名` で使う．

### `if __name__ == "__main__":`

この `if` の中は **そのファイルを直接実行したときだけ** 動く．import されたときは動かない．
関数の動作確認 (試し打ち) を書いておく場所として使う．

```python
# calc.py
def square(x):
    return x * x

if __name__ == "__main__":
    print(square(3))         # uv run calc.py のときだけ表示される
```

```python
# main.py
from calc import square      # ここでは calc.py の print(square(3)) は実行されない
print(square(5))             # → 25
```

### 別のフォルダにあるファイルを import する

`from A import a` が動くのは，**実行したファイルがあるフォルダ** が，Python がモジュールを探す場所の一覧
`sys.path` に自動で入るから．別のフォルダにあるファイルは，そのままでは見つからない．

第2週以降で使う `common/` (授業で共通して使う部品) はリポジトリのトップにあるので，
`sys.path` にリポジトリのトップを自分で加えてから import する．

```python
# second/02_camera_basics.py の先頭
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))   # リポジトリのトップを探索先に加える
from common import Trackbars, run
```

`Path(__file__).resolve()` はこのファイルの絶対パス．`.parents[n]` でそこから上のフォルダをたどる．

```python
p = Path("/home/me/RobotVision2026/second/02_camera_basics.py")
print(p.parents[0])    # → /home/me/RobotVision2026/second
print(p.parents[1])    # → /home/me/RobotVision2026         ← common/ があるフォルダ
```

`second/advanced/` のように1段深いフォルダのファイルなら `parents[2]` になる．
ファイルの場所に合わせて数字を変える．

<details>
<summary>もっと詳しく: import がどこからファイルを探すか (読まなくても演習はできる)</summary>

同じフォルダのファイルを読む書き方は2つある．

```python
import util          # ① 絶対 import: sys.path に並んだフォルダを順に探す
from . import util   # ② 相対 import: 自分が属しているパッケージの中を探す
```

①は相対パスのように見えるが，実際は `sys.path` から探しているだけ．
「同じフォルダを暗黙に探す」機能は Python 3 で廃止されている．
②は，そのファイルが **パッケージの一部として読み込まれたとき** だけ動く．

どちらが動くかは実行の仕方で決まる (`pkg/` の中に `main.py` と `util.py` がある場合)．

| 実行の仕方 | `sys.path` に入るもの | `import util` | `from . import util` |
| --- | --- | --- | --- |
| `uv run pkg/main.py` (どこから実行しても) | `pkg/` (実行したファイルのフォルダ) | 動く | 動かない |
| `uv run -m pkg.main` | カレントディレクトリ (`pkg/` の親) | 動かない | 動く |
| 別のファイルから `import pkg.main` | そのファイルのフォルダ | 動かない | 動く |

**ファイルとして実行する** (`uv run pkg/main.py`) と，`sys.path` に入るのは実行したファイルのフォルダで，
カレントディレクトリではない．また，そのファイルは単独の `__main__` として扱われ，親のパッケージを持たない．
そのため②は `ImportError: attempted relative import with no known parent package` になる．

**モジュールとして実行する** (`uv run -m pkg.main`，`python -m pkg.main` と同じ) と，
ファイルのパスではなくモジュール名 (フォルダを `.` でつなぎ，`.py` は付けない) で指定する．
このとき `sys.path` に入るのはカレントディレクトリで，`main.py` は `pkg` パッケージの一員として読み込まれる．
そのため②の相対 import や，`from pkg import util` のようにパッケージ名から書く import が使える．
パッケージのあるフォルダ (この例では `project/`) から実行する必要がある．

```
project/
├── pyproject.toml    uv はこのファイルがあるフォルダをプロジェクトのトップとみなす
└── pkg/
    ├── __init__.py
    ├── main.py       from . import util
    └── util.py
```

`uv run` は，カレントディレクトリから上にたどって最初に見つかった `pyproject.toml` のプロジェクトの環境で実行する．
`-m` で実行するときは，`pyproject.toml` と同じフォルダ (パッケージ `pkg/` の親) に移動してから実行する．
この授業のリポジトリでは，`RobotVision2026/pyproject.toml` がそれにあたる．

```shell
cd project
uv run -m pkg.main      # 動く
uv run pkg/main.py      # ImportError: attempted relative import with no known parent package
```

</details>

## 07 numpy の基本

numpy は数値の配列を高速に計算するためのライブラリ．`import numpy as np` で使う．

### 配列の作成と形状

```python
import numpy as np

a = np.array([1, 2, 3])                  # リストから作る
m = np.array([[1, 2], [3, 4], [5, 6]])   # 2次元 (3行2列)
print(m)
# → [[1 2]
#    [3 4]
#    [5 6]]
print(a.shape)                 # → (3,)
print(m.shape)                 # → (3, 2)     (行数, 列数)

print(np.arange(5))            # → [0 1 2 3 4]
print(np.arange(1, 10, 4))     # → [1 5 9]    (range と同じ要領)
print(np.zeros((2, 3)))        # → 0 で埋めた 2行3列
print(np.full((2, 2), 7))      # → 7 で埋めた 2行2列
print(np.arange(6).reshape(2, 3))
# → [[0 1 2]
#    [3 4 5]]                  (並べ替えて 2行3列 にする)
```

### 要素の取り出し

2次元配列は `配列[行, 列]` で取り出す．`:` は「その軸のすべて」を表し，スライスも使える．

```python
m = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]])
print(m[0, 2])         # → 3           (0 行 2 列目)
print(m[1])            # → [4 5 6]     (1 行目)
print(m[:, 0])         # → [1 4 7]     (全行の 0 列目 = 0 列目全体)
print(m[0:2, 1:3])     # → [[2 3]
                       #    [5 6]]     (0〜1 行目，1〜2 列目)
```

最後の `m[0:2, 1:3]` は **画像の一部を切り出す操作と同じ**．

### 配列の計算

`+ - * /` は **要素ごと** に計算される．

```python
a = np.array([1, 2, 3])
b = np.array([10, 20, 30])
print(a + b)           # → [11 22 33]
print(b - a)           # → [ 9 18 27]
print(a * b)           # → [10 40 90]
print(np.dot(a, b))    # → 140         (内積 1*10 + 2*20 + 3*30)

m = np.array([[1, 2], [3, 4]])
print(np.sum(m), np.mean(m), np.max(m), np.min(m))   # → 10 2.5 4 1
print(np.sort(np.array([3, 1, 2])))                  # → [1 2 3]
```

行列の積 `np.dot(A, B)` (または `A @ B`) は，**A の列数と B の行数が一致** していなければならない．
`.T` で転置 (行と列の入れ替え) できる．

```python
A = np.array([[1, 2, 3], [4, 5, 6]])     # (2, 3)
B = np.array([[1, 0, 0], [0, 1, 0]])     # (2, 3)
print(A.T.shape)                         # → (3, 2)
print(np.dot(A, B.T))                    # (2, 3) と (3, 2) の積 → (2, 2)
# → [[1 2]
#    [4 5]]
np.dot(A, B)
# → ValueError: shapes (2,3) and (2,3) not aligned: 3 (dim 1) != 2 (dim 0)
```

### ブロードキャスト

形の違う配列どうしでも，サイズ1の軸 (や足りない軸) を自動で引き伸ばして計算してくれる．

```python
a = np.array([1, 2, 3])
print(a * 10)          # → [10 20 30]   (10 が [10, 10, 10] に引き伸ばされる)

m = np.zeros((2, 3))
print(m + np.array([1, 2, 3]))
# → [[1. 2. 3.]
#    [1. 2. 3.]]       (各行に [1, 2, 3] が足される)
```

最後の軸の長さが一致していれば，3次元の配列にも使える．

```python
img = np.zeros((2, 2, 3))              # (高さ, 幅, 3) の小さな「画像」
print(img + np.array([5, 6, 7]))      # 全画素の3つの値にそれぞれ 5, 6, 7 を足す
```

### 乱数とソート

```python
rng = np.random.default_rng(0)    # 乱数生成器 (0 は種．同じ種なら毎回同じ乱数)
r = rng.random(5)                 # 0〜1 の乱数を 5 個
print(np.sort(r))                 # 小さい順
print(np.sort(r)[::-1])           # 大きい順 (小さい順を逆にする)
```

## 08 numpy の比較とマスク

### 比較すると bool 配列になる

numpy 配列を比較すると，**要素ごとの** `True` / `False` の配列 (bool 配列) ができる．

```python
a = np.array([5, 12, 3, 20])
mask = a > 10
print(mask)            # → [False  True False  True]
print(mask.sum())      # → 2           (True は 1, False は 0 として数えられる)
print(a[mask])         # → [12 20]     (True の位置の要素だけ取り出す)
print(a[a < 10])       # → [5 3]       (まとめて書ける)
```

### 範囲の条件 (`&` と `|`)

numpy 配列の条件の組み合わせには，`and` / `or` ではなく `&` (かつ) / `|` (または) を使い，
**各条件を `()` で囲む**．

```python
v = np.array([2, 15, 30, 45, 60])
print((v >= 10) & (v <= 40))   # → [False  True  True False False]   (10 以上 かつ 40 以下)
print((v < 10) | (v > 50))     # → [ True False False False  True]   (10 未満 または 50 より大きい)
```

### np.where で値を置き換える

`np.where(条件, 真のときの値, 偽のときの値)` で，条件に応じて値を選んだ配列を作る．

```python
g = np.array([[30, 180], [220, 90]], dtype=np.uint8)
print(np.where(g > 100, 1, 0))
# → [[0 1]
#    [1 0]]
print(np.where(g > 100, g, 0))     # 100 以下だけ 0 にし，他は元の値のまま
# → [[  0 180]
#    [220   0]]
```

結果の型を指定し直すには `.astype(型)` を使う．画像として扱うときは `np.uint8`．

```python
out = np.where(g > 100, 9, 0).astype(np.uint8)
print(out.dtype)       # → uint8
```

### np.where で座標を取り出す

`np.where(条件)` と引数を1つだけにすると，条件を満たす要素の **添字** が
`(行の添字の配列, 列の添字の配列)` の形で返る．

```python
b = np.zeros((4, 5), dtype=np.uint8)
b[1, 3] = 255
b[2, 1] = 255
rows, cols = np.where(b == 255)
print(rows)            # → [1 2]
print(cols)            # → [3 1]
print(rows.min(), rows.max(), cols.min(), cols.max())   # → 1 2 1 3
```

### if と配列

bool 配列をそのまま `if` に使うとエラーになる．「1つでも真」なら `.any()`，「すべて真」なら `.all()` を使う．

```python
a = np.array([5, 12, 3])
if a > 10:
    pass
# → ValueError: The truth value of an array with more than one element is ambiguous.
#               Use a.any() or a.all()

print((a > 10).any())  # → True
print((a > 10).all())  # → False
```

## 09 画像は numpy 配列

### 読み込みと形状

```python
import cv2

img = cv2.imread("color.jpg")   # 読み込みに失敗すると None が返る (パスの間違いが多い)
print(type(img))                # → <class 'numpy.ndarray'>
print(img.shape)                # → (400, 800, 3)    (高さ, 幅, チャンネル数)
print(img.dtype)                # → uint8            (0〜255 の整数)

h, w = img.shape[:2]            # 高さと幅だけ取り出す
```

### 画素の値と座標の順番

カラー画像の各画素は **B, G, R** の3つの値を持つ．
**numpy の添字は `img[y, x]` (行, 列) の順，OpenCV の関数に渡す座標は `(x, y)` の順** なので注意．

```python
print(img[10, 50])              # → [B G R]   (y=10, x=50 の画素)
print(img[10, 50, 2])           # → R の値

cv2.circle(img, (50, 10), 5, (0, 0, 255), -1)   # (x=50, y=10) に赤い円
```

### 切り出し・反転・チャンネル

スライスで画像を加工できる．

```python
top_left = img[0:100, 0:200]    # 上から 100 行，左から 200 列
print(top_left.shape)           # → (100, 200, 3)

upside_down = img[::-1, :]      # 上下反転 (行の順番を逆にする)
blue = img[:, :, 0]             # B チャンネルだけ (高さ, 幅) の2次元配列
print(blue.shape)               # → (400, 800)
```

ランダムな位置を選ぶときは，選んだ範囲が画像からはみ出さないよう上限を決める．

```python
rng = np.random.default_rng()
print(rng.integers(0, 10))      # 0 以上 10 未満の整数を1つ
```

### チャンネルの計算

チャンネルごとに取り出して計算できる．計算の途中は小数になるので，最後に整数に戻す．

```python
b, g, r = img[:, :, 0], img[:, :, 1], img[:, :, 2]
avg = (b.astype(float) + g + r) / 3            # 3つの平均
avg = np.round(avg).astype(np.uint8)
```

### uint8 のオーバーフロー

`uint8` は 0〜255 しか表せない．範囲を超えると **256 で割った余り** に回り込む．

```python
x = np.array([250], dtype=np.uint8)
print(x + 10)                   # → [4]      (260 は 256 を引いて 4 になる)
print(np.array([5], dtype=np.uint8) - 10)    # → [251]    (-5 は 256 を足して 251 になる)
```

回り込ませたくないときは，一度 `int` などの大きな型にしてから計算し，`np.clip` で範囲に収める．

```python
y = x.astype(int) + 10          # int なら 260 のまま
y = np.clip(y, 0, 255)          # 0〜255 に収める → [255]
y = y.astype(np.uint8)
```

### 表示

```python
cv2.imshow("window name", img)  # ウィンドウに表示
cv2.waitKey(0)                  # キーが押されるまで待つ (これが無いとウィンドウが描画されない)
cv2.destroyAllWindows()
```
