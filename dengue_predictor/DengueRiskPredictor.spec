# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = [('F:\\gihtub\\Dengue_Prefict\\dengue_predictor\\frontend', 'frontend'), ('F:\\gihtub\\Dengue_Prefict\\dengue_predictor\\core\\models', 'core/models'), ('F:\\gihtub\\Dengue_Prefict\\dengue_predictor\\datasets', 'datasets')]
binaries = []
hiddenimports = ['uvicorn', 'uvicorn.loops', 'uvicorn.loops.auto', 'uvicorn.protocols', 'uvicorn.protocols.http', 'uvicorn.protocols.http.auto', 'uvicorn.protocols.websockets', 'uvicorn.protocols.websockets.auto', 'uvicorn.lifespan', 'uvicorn.lifespan.on', 'fastapi', 'pydantic', 'google.generativeai', 'pinecone', 'joblib', 'sklearn', 'sklearn.linear_model', 'sklearn.linear_model._logistic', 'numpy', 'pandas', 'pydantic.fields', 'pydantic.main', 'api', 'api.BaseAPI', 'db', 'db.PineconeDB', 'agents', 'agents.AI_Agent', 'core']
tmp_ret = collect_all('uvicorn')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('fastapi')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('pydantic')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['F:\\gihtub\\Dengue_Prefict\\dengue_predictor\\start_full_system_exe.py'],
    pathex=['F:\\gihtub\\Dengue_Prefict\\dengue_predictor', 'F:\\gihtub\\Dengue_Prefict\\dengue_predictor\\api', 'F:\\gihtub\\Dengue_Prefict\\dengue_predictor\\db', 'F:\\gihtub\\Dengue_Prefict\\dengue_predictor\\agents'],
    binaries=binaries,
    datas=datas,
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
    name='DengueRiskPredictor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
