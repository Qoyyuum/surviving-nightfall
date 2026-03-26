# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = ['ursina', 'panda3d', 'panda3d.core', 'screeninfo', 'panda3d_gltf', 'panda3d_simplepbr']
hiddenimports += collect_submodules('panda3d')
hiddenimports += collect_submodules('direct')


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('assets', 'assets'), ('game', 'game'), ('.venv\\Lib\\site-packages\\ursina', 'ursina'), ('.venv\\Lib\\site-packages\\panda3d', 'panda3d'), ('.venv\\Lib\\site-packages\\direct', 'direct'), ('.venv\\Lib\\site-packages\\screeninfo', 'screeninfo'), ('.venv\\Lib\\site-packages\\panda3d_gltf', 'panda3d_gltf'), ('.venv\\Lib\\site-packages\\panda3d_simplepbr', 'panda3d_simplepbr')],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='SurvivingNightfall',
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
