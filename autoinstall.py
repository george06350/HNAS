# autoinstall.py
import importlib
import subprocess
import sys
import os

REQ_FILE = "requirements.txt"

def import_or_install(package, import_name=None):
    """嘗試匯入套件，若不存在則自動安裝，並寫入 requirements.txt"""
    try:
        return importlib.import_module(import_name or package)
    except ImportError:
        print(f"[AutoInstall] 缺少套件 {package}，正在安裝...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

        # 更新 requirements.txt
        _update_requirements(package)
        return importlib.import_module(import_name or package)

def _update_requirements(package):
    """將套件名稱加入 requirements.txt（如果尚未存在）"""
    if not os.path.exists(REQ_FILE):
        open(REQ_FILE, "w", encoding="utf-8").close()

    with open(REQ_FILE, "r+", encoding="utf-8") as f:
        lines = f.read().splitlines()
        if package not in lines:
            f.write(package + "\n")
            print(f"[AutoInstall] 已將 {package} 加入 requirements.txt")
