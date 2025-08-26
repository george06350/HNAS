# 自動安裝模組工具
from autoinstall import import_or_install

# ===== 標準庫 =====
os = import_or_install("os")
platform = import_or_install("platform")
socket = import_or_install("socket")
datetime_module = import_or_install("datetime")
datetime = datetime_module.datetime
hashlib = import_or_install("hashlib")

# ===== 第三方套件 =====
Flask = import_or_install("flask").Flask
render_template = import_or_install("flask").render_template
request = import_or_install("flask").request
redirect = import_or_install("flask").redirect
url_for = import_or_install("flask").url_for
session = import_or_install("flask").session
flash = import_or_install("flask").flash
send_from_directory = import_or_install("flask").send_from_directory
abort = import_or_install("flask").abort
generate_password_hash = import_or_install("werkzeug.security").generate_password_hash
check_password_hash = import_or_install("werkzeug.security").check_password_hash
secure_filename = import_or_install("werkzeug.utils").secure_filename
make_ssl_devcert = import_or_install("werkzeug.serving").make_ssl_devcert  # 補上這行
socket_std = import_or_install("socket")  # 改名
requests = import_or_install("requests")
GoblinAI = import_or_install("ai_module.goblin_ai").GoblinAI

make_ssl_devcert = import_or_install("werkzeug.serving").make_ssl_devcert
import_or_install("cryptography")  # SSL 憑證生成必須有

# ===== 資料夾路徑 =====
DATA_ROOT = os.path.abspath('data')
SYSTEM_ROOT = os.path.join(DATA_ROOT, 'system')
USER_BASE = os.path.join(SYSTEM_ROOT, 'users')       # 由 data/users -> data/system/users
USER_CFG_BASE = os.path.join(SYSTEM_ROOT, 'user-data')  # 由 data/system/user -> data/system/user-data
WALLPAPER_DIR = os.path.join(SYSTEM_ROOT, "wallpaper")

SSL_CERT = 'ssl'  # 會生成 ssl.crt 和 ssl.key
if not (os.path.exists(f"{SSL_CERT}.crt") and os.path.exists(f"{SSL_CERT}.key")):
    print("[SSL] 憑證不存在，自動生成中...")
    make_ssl_devcert(SSL_CERT, host='localhost')
    print("[SSL] 憑證已生成")

def get_lan_ip():
    ip_list = []
    hostname = socket.gethostname()
    try:
        # 嘗試用 hostname 取得 IP
        host_ip = socket.gethostbyname(hostname)
        if not host_ip.startswith("127."):
            ip_list.append(host_ip)
    except:
        pass

    # 遍歷所有網路介面
    try:
        for addr in socket.getaddrinfo(hostname, None):
            ip = addr[4][0]
            if ":" not in ip and not ip.startswith("127."):
                ip_list.append(ip)
    except:
        pass

    if ip_list:
        return ip_list[0]  # 回傳第一個非 127.0.0.1 的 IP
    return "127.0.0.1"

if __name__ == '__main__':
    LAN_IP = get_lan_ip()
    print(f"[INFO] 自動檢測 LAN IP: {LAN_IP}")

def ensure_wallpaper_dir_and_files():
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
    os.makedirs(USER_CFG_BASE, exist_ok=True)
    now = datetime.now().strftime('%Y/%m/%d+%H:%M:%S')
    os.makedirs(os.path.join(USER_BASE, username, "file"), exist_ok=True)
    cfg_path = user_config_path(username)
    password = hashlib.sha256(password.encode()).hexdigest()
    with open(cfg_path, 'w', encoding='utf-8') as f:
        f.write(f"username : {username}\n")
        f.write(f"password : {password}\n")
        f.write(f"register-time : {now}\n")

def check_login(username, password):
    global debug
    cfg = user_config_path(username)
    password = hashlib.sha256(password.encode()).hexdigest()
    if not os.path.exists(cfg):
        return False
    with open(cfg, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        if line.startswith('password : '):
            if app.debug:
                print(f"[DEBUG] 检查登录：用户名 {username}，输入的密码哈希值 {password}，实际存储的哈希值 {line.strip().split(' : ')[1]}")
            return line.strip().split(' : ')[1] == password
    return False

def secure_path(rel_path):
    full_path = os.path.abspath(os.path.join(DATA_ROOT, rel_path))
    if not full_path.startswith(DATA_ROOT):
        abort(403)
    return full_path

def get_all_users():
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
    current_wallpapers = {"wallpaper1": "wallpaper1.png", "wallpaper2": "wallpaper2.png"}
    wall_select_path = os.path.join(SYSTEM_ROOT, "wallpaper_select.txt")
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
        password = hashlib.sha256(password.encode()).hexdigest()
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
        password = hashlib.sha256(password.encode()).hexdigest()
        if not username or not password:
            flash('用户名和密码不能为空', 'danger')
        elif not user_exists(username):
            flash('用户不存在', 'danger')
        elif not check_login(username, password):
            flash('密码不正确', 'danger')
            if app.debug:
                print(f"登录失败：用户名 {username} 密码错误，輸入的密码哈希值为 {password}, 但实际存储的哈希值不匹配。")
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
    username = session['username']
    super_admin = is_super_admin(username)

    # 首页
    if not path.strip():
        roots = [
            {"name": "图片文件夹", "rel_path": "system/wallpaper", "type": "wallpaper"},
            {"name": "用户文件夹", "rel_path": f"system/users/{username}/file", "type": "user"},
            {"name": "system目录", "rel_path": "system_dir", "type": "system"},
        ]
        return render_template('filemanager_inner.html', entries=None, cur_path="", roots=roots)

    # 超级管理员：可以访问全部目录
    if super_admin:
        # “system目录”入口和其下所有内容，均只映射 data/system 目录
        if path == "system_dir" or path.startswith("system_dir/"):
            # 提取在system_dir后的相对路径
            sub_path = path[len("system_dir"):].lstrip("/")
            abs_path = os.path.join(SYSTEM_ROOT, sub_path)
            if not os.path.exists(abs_path):
                return "路径不存在", 404
            entries = []
            for name in sorted(os.listdir(abs_path)):
                entry_path = os.path.join(abs_path, name)
                # rel_path 保证继续带 system_dir 前缀
                rel_entry = f"system_dir/{sub_path}/{name}".replace("//", "/").strip("/")
                entries.append({
                    'name': name,
                    'is_dir': os.path.isdir(entry_path),
                    'rel_path': rel_entry
                })
            return render_template('filemanager_inner.html', entries=entries, cur_path=path, roots=None)
        # 其余路径，直接展示
        abs_path = secure_path(path)
        if not os.path.exists(abs_path):
            return "路径不存在", 404
        entries = []
        for name in sorted(os.listdir(abs_path)):
            entry_path = os.path.join(abs_path, name)
            rel_entry = os.path.relpath(entry_path, DATA_ROOT).replace("\\", "/")
            entries.append({
                'name': name,
                'is_dir': os.path.isdir(entry_path),
                'rel_path': rel_entry
            })
        return render_template('filemanager_inner.html', entries=entries, cur_path=path, roots=None)

    # 普通用户
    if path == f"system/users/{username}/file" or path.startswith(f"system/users/{username}/file/"):
        abs_path = secure_path(path)
        if not os.path.exists(abs_path):
            return "路径不存在", 404
        entries = []
        for name in sorted(os.listdir(abs_path)):
            entry_path = os.path.join(abs_path, name)
            rel_entry = os.path.relpath(entry_path, DATA_ROOT).replace("\\", "/")
            entries.append({
                'name': name,
                'is_dir': os.path.isdir(entry_path),
                'rel_path': rel_entry
            })
        return render_template('filemanager_inner.html', entries=entries, cur_path=path, roots=None)

    if path == "system/wallpaper" or path.startswith("system/wallpaper/"):
        abs_path = secure_path(path)
        if not os.path.exists(abs_path):
            return "路径不存在", 404
        entries = []
        for name in sorted(os.listdir(abs_path)):
            entry_path = os.path.join(abs_path, name)
            rel_entry = os.path.relpath(entry_path, DATA_ROOT).replace("\\", "/")
            entries.append({
                'name': name,
                'is_dir': os.path.isdir(entry_path),
                'rel_path': rel_entry
            })
        return render_template('filemanager_inner.html', entries=entries, cur_path=path, roots=None)

    # 非超级管理员禁止访问其他目录
    return "无权限访问此目录", 403

@app.route('/filemanager_inner/upload', methods=['POST'])
def upload_file_inner():
    if 'username' not in session:
        return "请重新登录！", 401
    cur_path = request.form.get('cur_path', '')
    abs_path = secure_path(cur_path)
    username = session['username']
    super_admin = is_super_admin(username)
    if not super_admin and not (
        cur_path.startswith("system/wallpaper")
        or cur_path.startswith(f"system/users/{username}/file")
    ):
        return "无权限上传到此目录", 403
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
    username = session['username']
    super_admin = is_super_admin(username)
    if not super_admin and not (
        path.startswith("system/wallpaper")
        or path.startswith(f"system/users/{username}/file")
    ):
        return "无权限下载此文件", 403
    if not os.path.isfile(abs_path):
        return "文件不存在", 404
    rel_dir = os.path.dirname(path)
    filename = os.path.basename(path)
    return send_from_directory(secure_path(rel_dir), filename, as_attachment=True)

@app.route('/filemanager_inner/preview/<path:path>')
def filemanager_image_preview(path):
    if 'username' not in session:
        return "请重新登录！", 401
    username = session['username']
    super_admin = is_super_admin(username)
    if not super_admin and not (
        path.startswith("system/wallpaper")
        or path.startswith(f"system/users/{username}/file")
    ):
        return "无权限在线预览", 403
    abs_path = secure_path(path)
    if not os.path.isfile(abs_path):
        return "文件不存在", 404
    ext = os.path.splitext(path)[-1].lower()
    if ext not in [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"]:
        return "仅支持图片在线预览", 400
    rel_dir = os.path.dirname(path)
    filename = os.path.basename(path)
    return send_from_directory(secure_path(rel_dir), filename)

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

    ensure_wallpaper_dir_and_files()
    wall_files = sorted([f for f in os.listdir(WALLPAPER_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    current_wallpapers = get_current_wallpapers()
    current_wall_path = os.path.join(SYSTEM_ROOT, "wallpaper_select.txt")
    if request.method == 'POST' and request.form.get('action') == 'change_wallpaper':
        wp1 = request.form.get('wallpaper1', 'wallpaper1.png')
        wp2 = request.form.get('wallpaper2', 'wallpaper2.png')
        with open(current_wall_path, "w", encoding="utf-8") as f:
            f.write(f"wallpaper1:{wp1}\nwallpaper2:{wp2}\n")
        current_wallpapers["wallpaper1"] = wp1
        current_wallpapers["wallpaper2"] = wp2
        message = "壁纸设置已更新"
    if request.method == 'POST' and request.form.get('action') == 'create_user':
        new_username = request.form.get('new_username', '').strip()
        new_password = request.form.get('new_password', '').strip()
        new_password = hashlib.sha256(new_password.encode()).hexdigest()
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
    if request.method == 'POST' and not request.form.get('action'):
        pwd = request.form.get('new_password', '').strip()
        if pwd:
            path = user_config_path(session['username'])
            pwd = hashlib.sha256(pwd.encode()).hexdigest()
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

import ssl

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('cert.pem', 'key.pem')

app.run(ssl_context=context, debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    #app.run(ssl_context=(f"{SSL_CERT}.crt", f"{SSL_CERT}.key"), debug=True, host='0.0.0.0', port=5000)

goblin = GoblinAI(username="hray1413")

@app.route("/upload", methods=["POST"])
def upload_file():
    # ...原本的上傳邏輯
    print(goblin.respond_to_action("upload"))
    return "上傳完成"

@app.route("/error")
def error_page():
    print(goblin.respond_to_action("error"))
    return "出錯了"
@app.route("/window/goblin_ai")
def goblin_ai_window():
    return render_template("goblin_ai_inner.html")
import os
from flask import Flask
from werkzeug.serving import make_ssl_devcert

SSL_CERT_DIR = os.path.join(SYSTEM_ROOT, 'ssl')
SSL_CERT_FILE = os.path.join(SSL_CERT_DIR, 'goblin_ssl')
CRT = f"{SSL_CERT_FILE}.crt"
KEY = f"{SSL_CERT_FILE}.key"

def init_ssl():
    if not (os.path.exists(CRT) and os.path.exists(KEY)):
        print("[SSL] 憑證不存在，Goblin 正在召喚魔法陣...")
        try:
            os.makedirs(SSL_CERT_DIR, exist_ok=True)
            make_ssl_devcert(SSL_CERT_FILE, host='localhost')
            print("[SSL] 憑證召喚成功！")
        except Exception as e:
            print(f"[SSL] 憑證生成失敗：{e}")
            try:
                print(goblin.respond_to_action("error"))
            except:
                print("[GoblinAI] 無法啟動情緒支援，請手動檢查 SSL 問題。")

def run_server():
    init_ssl()
    try:
        app.run(ssl_context=context, debug=True, host='0.0.0.0', port=5000)
        app.run(ssl_context=(CRT, KEY), debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"[SSL] 啟動失敗，改用非加密模式：{e}")
        app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    run_server()
# 確保 SSL 憑證目錄存在
os.makedirs(SSL_CERT_DIR, exist_ok=True)
if not (os.path.exists(CRT) and os.path.exists(KEY)):
        try:
            make_ssl_devcert(SSL_CERT_FILE, host='localhost')
            print("[SSL] 根目錄憑證生成成功")
        except Exception as e:
            print(f"[SSL] 憑證生成失敗：{e}")



