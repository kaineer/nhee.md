#!/usr/bin/env python3
import shutil
import sys
from pathlib import Path

script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from processors.builder import Builder

src = Path("src").absolute()
dist = Path("dist").absolute()

if dist.exists():
    shutil.rmtree(dist)
dist.mkdir(parents=True)

assets = src / "assets"
if assets.is_dir():
    shutil.copytree(assets, dist / "assets")

Builder(str(src), outdir=str(dist)).build()
