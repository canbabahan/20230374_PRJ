"""pytest konfigürasyonu: kutuphane dizinini sys.path'e ekler."""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
