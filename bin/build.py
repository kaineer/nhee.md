#!/usr/bin/env python3
import sys
from pathlib import Path

script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from processors.builder import Builder

root = str((Path(".") / "src").absolute())

Builder(root).build()
