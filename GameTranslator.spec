# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file para Game Translator

import os
import sys

block_cipher = None

# Diretório base do projeto
BASE_DIR = os.path.dirname(os.path.abspath(SPEC))
SRC_DIR = os.path.join(BASE_DIR, 'src')

# Coleta todos os arquivos Python do src
datas = []
hiddenimports = [
    'PySide6.QtCore',
    'PySide6.QtGui', 
    'PySide6.QtWidgets',
    'sqlite3',
    'psutil',
    'requests',
    'json',
    'xml.etree.ElementTree',
    're',
    'os',
    'sys',
    'pathlib',
    'datetime',
    'time',
    'threading',
    'collections',
    'functools',
    'gc',
    'database',
    'regex_profiles',
    'file_processor',
    'smart_translator',
    'translation_api',
    'logger',
    'security',
]

# Adiciona os módulos src como dados
datas.append((os.path.join(SRC_DIR, '*.py'), '.'))
datas.append((os.path.join(SRC_DIR, 'gui', '*.py'), 'gui'))

# Adiciona pasta profiles se existir
profiles_dir = os.path.join(BASE_DIR, 'profiles')
if os.path.exists(profiles_dir):
    datas.append((profiles_dir, 'profiles'))

a = Analysis(
    [os.path.join(SRC_DIR, 'main.py')],
    pathex=[SRC_DIR, BASE_DIR],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='GameTranslator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Sem janela de console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
