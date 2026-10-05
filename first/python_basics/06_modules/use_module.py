"""06 モジュール: 別のファイルに書いた関数を使う

実行方法 (first/python_basics/06_modules で):
    uv run use_module.py

同じフォルダの A.py と，modules フォルダの中の B.py から関数を読み込んで使う．
解説は first/README.md の「06 モジュール」を参照．
"""

from A import a  # A.py の関数 a を読み込む
from modules.B import b  # modules/B.py の関数 b を読み込む


def main():
    a()
    b()


if __name__ == "__main__":
    main()
