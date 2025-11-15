# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for the PyArmor-protected build."""

from pathlib import Path

block_cipher = None

project_root = Path(__file__).parent
obf_dir = project_root / "dist" / "obf"
entry_script = obf_dir / "white_click.py"

if not entry_script.exists():
    raise SystemExit(
        "dist/obf/white_click.py is missing. Run 'pyarmor gen -O dist/obf white_click.py' first."
    )

runtime_datas = [
    (str(path), path.name) for path in obf_dir.glob("pyarmor_runtime_*") if path.is_dir()
]

hidden_imports = ["numpy", "mss", "pynput"]


a = Analysis(
    [str(entry_script)],
    pathex=[],
    binaries=[],
    datas=runtime_datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="white_click_obf",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="white_click_obf",
)
