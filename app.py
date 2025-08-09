# =============================================================
#  HNAS - 轻量级家庭NAS工具
#  Copyright (c) 2024-2025 George06350. All Rights Reserved.
#  项目地址: https://github.com/george06350/HNAS
#
#  本项目源码仅供学习与个人非商业用途使用。
#  未经许可，不得用于商业用途或翻版传播。
# =============================================================

import os
import platform
import socket
import datetime
import requests
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory, abort

DATA_ROOT = os.path.abspath('data')
USER_BASE = os.path.join(DATA_ROOT, 'users')
USER_CFG_BASE = os.path.join(DATA_ROOT, 'system', 'user')
WALLPAPER_DIR = os.path.join(DATA_ROOT, "system", "wallpaper")

def ensure_wallpaper_dir_and_files():
    """自动创建壁纸目录，并下载默认壁纸文件（如不存在）"""
    os.makedirs(WALLPAPER_DIR, exist_ok=True)
    default_wallpapers = {
        "wallpaper1.png": "https://raw.githubusercontent.com/george06350/HNAS-File/main/wallpaper/wallpaper1.png",
        "wallpaper2.png": "https://raw.githubusercontent.com/george06350/HNAS-File/main/wallpaper/wallpaper2.png"
    }
    for fname, url in default_wallpapers.items():
        fpath = os.path.join(WALLPAPER_DIR, fname)
        if not os.path.exists(fpath):
            try:
                resp = requests.get(url, timeout=10)
                if resp.status_code == 200:
                    with open(fpath, "wb") as f:
                        f.write(resp.content)
            except Exception as e:
                print(f"[WARN] 下载壁纸 {fname} 失败: {e}")

ensure_wallpaper_dir_and_files()

app = Flask(__name__)
app.secret_key = os.urandom(24)
os.makedirs(USER_BASE, exist_ok=True)
os.makedirs(USER_CFG_BASE, exist_ok=True)

def user_config_path(username):
    return os.path.join(USER_CFG_BASE, f"{username}.txt")

def user_file_dir(username):
    path = os.path.join(USER_BASE, username, "file")
    os.makedirs(path, exist_ok=True)
    return path

def user_exists(username):
    return os.path.exists(user_config_path(username))

def create_user(username, password):
    now = datetime.datetime.now().strftime('%Y/%m/%d+%H:%M:%S')
    os.makedirs(os.path.join(USER_BASE, username, "file"), exist_ok=True)
    cfg_path = user_config_path(username)
    with open(cfg_path, 'w', encoding='utf-8') as f:
        f.write(f"username : {username}\n")
        f.write(f"password : {password}\n")
        f.write(f"register-time : {now}\n")

def check_login(username, password):
    cfg = user_config_path(username)
    if not os.path.exists(cfg):
        return False
    with open(cfg, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        if line.startswith('password : '):
            return line.strip().split(' : ')[1] == password
    return False

def secure_path(rel_path):
    # 防止目录穿越攻击，返回绝对路径
    full_path = os.path.abspath(os.path.join(DATA_ROOT, rel_path))
    if not full_path.startswith(DATA_ROOT):
        abort(403)
    return full_path

def get_all_users():
    """获取所有用户名及注册时间，按注册时间升序"""
    users = []
    for fname in os.listdir(USER_CFG_BASE):
        if fname.endswith('.txt'):
            uname = fname[:-4]
            reg_time = ''
            with open(os.path.join(USER_CFG_BASE, fname), encoding='utf-8') as f:
                for line in f:
                    if line.startswith('register-time') or line.startswith('register_time'):
                        reg_time = line.strip().split(':', 1)[-1].strip()
            users.append({'username': uname, 'register_time': reg_time})
    users.sort(key=lambda u: u['register_time'])
    return users

def is_super_admin(username):
    users = get_all_users()
    return users and users[0]['username'] == username

def get_current_wallpapers():
    """读取当前生效的壁纸设置"""
    current_wallpapers = {"wallpaper1": "wallpaper1.png", "wallpaper2": "wallpaper2.png"}
    wall_select_path = os.path.join(DATA_ROOT, "system", "wallpaper_select.txt")
    if os.path.exists(wall_select_path):
        with open(wall_select_path, encoding="utf-8") as f:
            for line in f:
                if line.startswith("wallpaper1:"):
                    current_wallpapers["wallpaper1"] = line.split(":", 1)[1].strip()
                elif line.startswith("wallpaper2:"):
                    current_wallpapers["wallpaper2"] = line.split(":", 1)[1].strip()
    return current_wallpapers

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect(url_for('desktop'))
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        if not username or not password:
            flash('用户名和密码不能为空', 'danger')
        elif user_exists(username):
            flash('用户名已存在', 'danger')
        else:
            create_user(username, password)
            session['username'] = username
            flash('注册成功！', 'success')
            return redirect(url_for('desktop'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('desktop'))
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        if not username or not password:
            flash('用户名和密码不能为空', 'danger')
        elif not user_exists(username):
            flash('用户不存在', 'danger')
        elif not check_login(username, password):
            flash('密码不正确', 'danger')
        else:
            session['username'] = username
            flash('登录成功！', 'success')
            return redirect(url_for('desktop'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('已退出登录', 'info')
    return redirect(url_for('login'))

@app.route('/')
def index():
    if 'username' not in session:
        if not os.listdir(USER_CFG_BASE):
            return redirect(url_for('register'))
        else:
            return redirect(url_for('login'))
    return redirect(url_for('desktop'))

@app.route('/desktop')
def desktop():
    if 'username' not in session:
        return redirect(url_for('login'))
    current_wallpapers = get_current_wallpapers()
    return render_template('index.html', username=session['username'], current_wallpapers=current_wallpapers)

@app.route('/filemanager_inner/', defaults={'path': ''})
@app.route('/filemanager_inner/<path:path>')
def filemanager_inner(path):
    if 'username' not in session:
        return "请重新登录！", 401
    abs_path = secure_path(path)
    if not os.path.exists(abs_path):
        return "路径不存在", 404
    entries = []
    for name in sorted(os.listdir(abs_path)):
        entry_path = os.path.join(abs_path, name)
        entries.append({
            'name': name,
            'is_dir': os.path.isdir(entry_path),
            'rel_path': os.path.relpath(os.path.join(abs_path, name), DATA_ROOT).replace("\\", "/")
        })
    return render_template('filemanager_inner.html', entries=entries, cur_path=path)

@app.route('/filemanager_inner/upload', methods=['POST'])
def upload_file_inner():
    if 'username' not in session:
        return "请重新登录！", 401
    cur_path = request.form.get('cur_path', '')
    abs_path = secure_path(cur_path)
    file = request.files['file']
    if file:
        file.save(os.path.join(abs_path, file.filename))
        return "上传成功"
    else:
        return "请选择文件", 400

@app.route('/filemanager_inner/download/<path:path>')
def download_file_inner(path):
    if 'username' not in session:
        return "请重新登录！", 401
    abs_path = secure_path(path)
    if not os.path.isfile(abs_path):
        return "文件不存在", 404
    rel_dir = os.path.dirname(path)
    filename = os.path.basename(path)
    return send_from_directory(secure_path(rel_dir), filename, as_attachment=True)

@app.route('/about_inner')
def about_inner():
    if 'username' not in session:
        return "请重新登录！", 401
    return render_template('about_inner.html')

@app.route('/settings_inner', methods=['GET', 'POST'])
def settings_inner():
    if 'username' not in session:
        return "请重新登录！", 401
    message = ''
    users = get_all_users()
    super_admin = is_super_admin(session['username'])

    # -- 壁纸设置 --
    ensure_wallpaper_dir_and_files()
    wall_files = sorted([f for f in os.listdir(WALLPAPER_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    current_wallpapers = get_current_wallpapers()
    current_wall_path = os.path.join(DATA_ROOT, "system", "wallpaper_select.txt")
    if request.method == 'POST' and request.form.get('action') == 'change_wallpaper':
        wp1 = request.form.get('wallpaper1', 'wallpaper1.png')
        wp2 = request.form.get('wallpaper2', 'wallpaper2.png')
        with open(current_wall_path, "w", encoding="utf-8") as f:
            f.write(f"wallpaper1:{wp1}\nwallpaper2:{wp2}\n")
        current_wallpapers["wallpaper1"] = wp1
        current_wallpapers["wallpaper2"] = wp2
        message = "壁纸设置已更新"
    # -- 多用户管理 --
    if request.method == 'POST' and request.form.get('action') == 'create_user':
        new_username = request.form.get('new_username', '').strip()
        new_password = request.form.get('new_password', '').strip()
        if not new_username or not new_password:
            message = "用户名和密码不能为空"
        elif user_exists(new_username):
            message = "该用户名已存在"
        else:
            create_user(new_username, new_password)
            message = f"用户 {new_username} 创建成功"
        users = get_all_users()
    if request.method == 'POST' and request.form.get('action') == 'delete_user' and super_admin:
        del_username = request.form.get('del_username', '').strip()
        if del_username == session['username']:
            message = "不能删除自己"
        elif not user_exists(del_username):
            message = "该用户不存在"
        else:
            os.remove(user_config_path(del_username))
            user_folder = os.path.join(USER_BASE, del_username)
            if os.path.isdir(user_folder):
                import shutil
                shutil.rmtree(user_folder)
            message = f"用户 {del_username} 已删除"
        users = get_all_users()
    # -- 账号设置 --
    if request.method == 'POST' and not request.form.get('action'):
        pwd = request.form.get('new_password', '').strip()
        if pwd:
            path = user_config_path(session['username'])
            with open(path, "r", encoding='utf-8') as f:
                lines = f.readlines()
            with open(path, "w", encoding='utf-8') as f:
                for line in lines:
                    if line.startswith("password : "):
                        f.write(f"password : {pwd}\n")
                    else:
                        f.write(line)
            message = "密码已更新！"
        else:
            message = "未作更改。"
    sysinfo = {
        'hostname': socket.gethostname(),
        'os': f"{platform.system()} {platform.release()}",
        'arch': platform.machine(),
        'python_version': platform.python_version(),
        'now': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    user_email = ""
    cfg_path = user_config_path(session['username'])
    if os.path.exists(cfg_path):
        with open(cfg_path, encoding='utf-8') as f:
            for line in f:
                if line.startswith("email : "):
                    user_email = line.strip().split(":",1)[1].strip()
    return render_template('settings_inner.html',
        username=session['username'],
        user_email=user_email,
        message=message,
        sysinfo=sysinfo,
        users=users,
        super_admin=super_admin,
        wall_files=wall_files,
        current_wallpapers=current_wallpapers
    )

@app.route('/wallpaper/<filename>')
def serve_wallpaper(filename):
    ensure_wallpaper_dir_and_files()
    return send_from_directory(WALLPAPER_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)