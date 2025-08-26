import importlib
import subprocess
import sys
import os

REQ_FILE = "requirements.txt"

def import_or_install(package, import_name=None, version=None):
    """嘗試匯入套件，若不存在則自動安裝，並寫入 requirements.txt"""
    module_name = import_name or package
    try:
        return importlib.import_module(module_name)
    except ImportError:
        print(f"[AutoInstall] ⚠️ 缺少套件 {package}，Goblin 正在召喚魔法陣安裝中...")

        pkg_spec = f"{package}=={version}" if version else package
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg_spec])
            _update_requirements(pkg_spec)
            print(f"[AutoInstall] ✅ 套件 {pkg_spec} 安裝完成！")
            return importlib.import_module(module_name)
        except subprocess.CalledProcessError as e:
            print(f"[AutoInstall] ❌ 安裝失敗：{e}")
            raise ImportError(f"無法安裝套件 {pkg_spec}，請手動處理。")

def _update_requirements(package_line):
    """將套件名稱加入 requirements.txt（如果尚未存在）"""
    try:
        if not os.path.exists(REQ_FILE):
            open(REQ_FILE, "w", encoding="utf-8").close()

        with open(REQ_FILE, "r+", encoding="utf-8") as f:
            lines = f.read().splitlines()
            pkg_name = package_line.split("==")[0]
            if not any(line.startswith(pkg_name) for line in lines):
                f.write(package_line + "\n")
                print(f"[AutoInstall] 📦 已將 {package_line} 加入 requirements.txt")
    except Exception as e:
        print(f"[AutoInstall] ⚠️ 無法更新 requirements.txt：{e}")
