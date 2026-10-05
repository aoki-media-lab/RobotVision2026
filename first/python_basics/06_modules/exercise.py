"""06 モジュールの演習

実行方法 (first/python_basics/06_modules で):
    uv run python exercise.py

やること:
    [課題1] my_geometry.py に clamp と center を書く
    [課題2] my_geometry.py の if __name__ == "__main__": の中に試し打ちを書く
    [課題3] modules/C.py を新しく作り，"Hello C" という文字列を返す関数 c() を書く
            (print ではなく return すること)
    [課題4] 下の TODO の行で，modules/C.py の c を import する

期待する出力:
    OK 課題1
    OK 課題3
    すべて OK!
(my_geometry.py の試し打ちの print はここでは表示されないはず)
"""

from my_geometry import center, clamp

# [課題4] TODO: modules/C.py から c を import する (use_module.py を参考に)


assert clamp(-5, 0, 100) == 0 and clamp(50, 0, 100) == 50 and clamp(200, 0, 100) == 100, (
    "課題1: clamp が正しくない"
)
assert center(640, 480) == (320, 240), "課題1: center が正しくない"
print("OK 課題1")

assert "c" in globals(), "課題3・4: modules/C.py の c がまだ import されていない"
assert c() == "Hello C", f'課題3: c() は "Hello C" を返すこと (実際: {c()!r})'
print("OK 課題3")

print("すべて OK!")
