# -*- mode: python -*-

block_cipher = None


a = Analysis(['pyling/PyLing.py'],
             pathex=['/Users/dominiquedanco/Documents/College/U3/LING550/project/PyLing'],
             binaries=None,
             datas=None,
             hiddenimports=['setuptools'],
             hookspath=['freezing/hooks'],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='PyLing',
          debug=True,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='PyLing')
app = BUNDLE(coll,
             name='PyLing.app',
             icon=None,
             bundle_identifier=None)
