"""授業で共通して使う部品

    from common import run, Trackbars
"""

from .camera import run
from .trackbar import Trackbars

__all__ = ["run", "Trackbars"]
