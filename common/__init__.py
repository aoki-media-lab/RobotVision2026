"""授業で共通して使う部品

    from common import run, tile, Trackbars
"""

from .camera import run, tile
from .trackbar import Trackbars

__all__ = ["run", "tile", "Trackbars"]
