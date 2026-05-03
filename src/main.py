import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pipeline.api import app

__all__ = ["app"]