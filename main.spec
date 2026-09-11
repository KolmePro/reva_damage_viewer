# -*- mode: python ; coding: utf-8 -*-

import re
from pathlib import Path

from PyInstaller.utils.win32.versioninfo import (
    FixedFileInfo,
    StringFileInfo,
    StringStruct,
    StringTable,
    VarFileInfo,
    VarStruct,
    VSVersionInfo,
)


version = Path('src/VERSION').read_text(encoding='utf-8').strip()
version_match = re.fullmatch(r'(\d+)\.(\d+)\.(\d+)(?:[-+][0-9A-Za-z.-]+)?', version)
if version_match is None:
    raise ValueError(f'Некорректная версия в src/VERSION: {version!r}')

version_tuple = tuple(map(int, version_match.groups())) + (0,)
version_info = VSVersionInfo(
    ffi=FixedFileInfo(
        filevers=version_tuple,
        prodvers=version_tuple,
        mask=0x3F,
        flags=0x0,
        OS=0x40004,
        fileType=0x1,
        subtype=0x0,
        date=(0, 0),
    ),
    kids=[
        StringFileInfo([
            StringTable('041904B0', [
                StringStruct('CompanyName', 'KolmePRO'),
                StringStruct('FileDescription', 'DamageViewer — Калькулятор урона'),
                StringStruct('FileVersion', version),
                StringStruct('InternalName', 'DamageViewer'),
                StringStruct('OriginalFilename', 'DamageViewer.exe'),
                StringStruct('ProductName', 'DamageViewer'),
                StringStruct('ProductVersion', version),
            ]),
        ]),
        VarFileInfo([VarStruct('Translation', [1049, 1200])]),
    ],
)


a = Analysis(
    ['src/main.pyw'],
    pathex=['src'],
    binaries=[],
    datas=[
        ('src/resources', 'resources'),
        ('src/filter_plugins', 'filter_plugins'),
        ('src/VERSION', '.'),
    ],
    hiddenimports=[],
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
    name='DamageViewer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon='src/resources/DamageViewer.ico',
    version=version_info,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
