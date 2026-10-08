def a():
    print("Hello A.py")


# このファイルを直接実行したとき (uv run A.py) だけ実行される．
# 他のファイルから import されたときは実行されない．
if __name__ == "__main__":
    a()
