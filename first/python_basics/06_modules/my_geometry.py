"""exercise.py から import して使う関数をここに書く

[課題1] 05_functions.py で書いた clamp と center をここに書き写せ．
"""

def clamp(v, lo, hi):
    if v <= lo:
        return lo
    if v >= hi:
        return hi
    return v  # TODO


def center(w, h):
    return w // 2, h // 2  # TODO


# [課題2] 下の if 文の中に，このファイルを直接実行したときだけ動く「試し打ち」を書け．
#   例: print(center(640, 480))
#   exercise.py から import したときには，この print が出ないことを確かめよう．
if __name__ == "__main__":
    print(center(640,480))
    print("これは試し打ち")
