# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path
import sys


site_packages = Path(sys.prefix) / "Lib" / "site-packages"
datas = []
binaries = []
hiddenimports = [
    "adafruit_blinka.board.ftdi_ft232h",
    "adafruit_blinka.microcontroller.ftdi_mpsse",
    "adafruit_blinka.microcontroller.ftdi_mpsse.ft232h",
    "adafruit_blinka.microcontroller.ftdi_mpsse.mpsse",
    "adafruit_blinka.microcontroller.ftdi_mpsse.mpsse.i2c",
    "adafruit_blinka.microcontroller.ftdi_mpsse.mpsse.pin",
    "adafruit_blinka.microcontroller.ftdi_mpsse.mpsse.url",
]

for runtime_manifest in ("board_imports.json", "microcontroller_imports.json"):
    manifest = site_packages / runtime_manifest
    if manifest.exists():
        datas.append((str(manifest), "."))


a = Analysis(
    ['src/main.py'],
    pathex=['src'],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'PyQt5', 'PyQt6', 'PySide2',
        'pyqtgraph.opengl', 'pyqtgraph.console',
        'pyqtgraph.examples', 'IPython', 'matplotlib',
        'pandas', 'scipy', 'h5py', 'dask', 'numba',
        'llvmlite', 'torch', 'tensorflow', 'sklearn',
        'xarray', 'openpyxl', 'pyarrow', 'boto3',
    ],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='HelmholtzCoilMapper',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
