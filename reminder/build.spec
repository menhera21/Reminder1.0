# -*- mode: python -*-

block_cipher = None

a = Analysis(
    ['reminder_app.py'],
    pathex=[os.getcwd()],  # 添加当前工作目录路径
    binaries=[],
    # 修改第7行确保包含图标路径
    datas=[('icon.ico', '.')],
    hiddenimports=['PIL'],  # 显式声明Pillow依赖
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher
)

# 在Analysis后添加PYZ配置
pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

# 修改EXE配置为：
exe = EXE(
    pyz,
    a.scripts,
    exclude_binaries=True,
    name='ReminderApp',
    debug=False,
    icon=['icon.ico'],
    console=False  # 隐藏控制台窗口
)

# 添加COLLECT配置确保完整打包
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='ReminderApp'
)