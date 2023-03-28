# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# generovani exe
# py -3.9 -m PyInstaller --clean --log-level DEBUG  --distpath ./ server.spec
# ! primo do slozky dist vyhazovalo vyjimky, nekdy stacilo opakovat build? !
# spolu s exe souborem nutne kopriovat web, configs, mainConfig.json + dalsi povinne soubory
a = Analysis(['server.py'],
             pathex=[
                 'C:\\Program Files (x86)\\Windows Kits\\10\\Redist\\ucrt\\DLLs\\x86'
             ],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[".git"],
             win_no_prefer_redirects=False,
            win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='cameraProcessing',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )

#volano obracene z deploy.py
#import deploy
#deploy.deploy()