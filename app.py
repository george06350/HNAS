# =============================================================
#  HNAS - 轻量级家庭NAS工具
#  Copyright (c) 2024-2025 George06350. All Rights Reserved.
#  项目地址: https://github.com/george06350/HNAS
# 
#  本项目源码仅供学习与个人非商业用途使用。
#  未经许可，不得用于商业用途或翻版传播。
# =============================================================
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory, abort
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)  # 每次重启强制所有人下线

DATA_ROOT = os.path.abspath('data')
USER_BASE = os.path.join(DATA_ROOT, 'users')
USER_CFG_BASE = os.path.join(DATA_ROOT, 'system', 'user')
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
    now = datetime.now().strftime('%Y/%m/%d+%H:%M:%S')
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
    return render_template('index.html', username=session['username'])

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)