"""06 モジュールの演習

実行方法 (first/python_basics/06_modules で):
    uv run exercise.py

やること:
    [課題1] my_geometry.py に clamp と center を書く
    [課題2] my_geometry.py の if __name__ == "__main__": の中に試し打ちを書く
            (このファイルを実行したときには，その試し打ちの print が表示されないことを確かめる)
    [課題3] modules/C.py を新しく作り，"Hello C" という文字列を返す関数 c() を書く
            (print ではなく return すること)
    [課題4] task_4 の中で modules/C.py の c を import し，c() の戻り値を返す

ある課題で詰まったら，main の中のその課題の行をコメントアウトすれば，他の課題を先に進められる．
"""

from my_geometry import center, clamp


def task_4():
    """[課題4] modules/C.py から c を import し (use_module.py を参考に)，c() の戻り値を返せ"""
    from modules.C import c
    # TODO: import の行を書く
    return c()


if __name__ == "__main__":
    print("課題1 clamp:", clamp(-5, 0, 100), clamp(50, 0, 100), clamp(200, 0, 100))
    print("課題1 center:", center(640, 480))
    print("課題3・4:", task_4())
