document.getElementById('start-menu-btn').onclick = function() {
    var menu = document.getElementById('start-menu');
    menu.style.display = (menu.style.display === 'block') ? 'none' : 'block';
};
document.body.onclick = function(e) {
    if (!e.target.closest('#start-menu') && !e.target.closest('#start-menu-btn')) {
        document.getElementById('start-menu').style.display = 'none';
    }
}

let zIndexCounter = 1000;
let winIdCounter = 0;
const winIcons = {
    filemanager: `<svg width="18" height="18" viewBox="0 0 24 24"><path fill="#2356a6" d="M3 6V4a2 2 0 0 1 2-2h5.17a2 2 0 0 1 1.41.59L13.59 4H21a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2zm0 2v10h18V6h-8.59l-2-2H5v2zm5 2h2v2h-2v-2z"></path></svg>`,
    about: `<svg width="18" height="18" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="#2356a6"/><rect x="11" y="11" width="2" height="6" fill="#fff"/><rect x="11" y="7" width="2" height="2" fill="#fff"/></svg>`,
    settings: `<svg width="18" height="18" viewBox="0 0 24 24"><path fill="#2356a6" d="M12 15.5A3.5 3.5 0 1 0 12 8.5a3.5 3.5 0 0 0 0 7zm7.43-3.78l2.06-1.63a1 1 0 0 0 .21-1.32l-2-3.46a1 1 0 0 0-1.25-.45l-2.43.98a7.03 7.03 0 0 0-1.5-.87l-.37-2.6A1 1 0 0 0 12 2h-4a1 1 0 0 0-1 .88l-.38 2.6c-.54.23-1.05.51-1.5.87l-2.43-.98a1 1 0 0 0-1.25.45l-2 3.46a1 1 0 0 0 .21 1.32l2.06 1.63a6.85 6.85 0 0 0 0 1.74l-2.06 1.63a1 1 0 0 0-.21 1.32l2 3.46a1 1 0 0 0 1.25.45l2.43-.98c.45.36.96.64 1.5.87l.38 2.6A1 1 0 0 0 8 22h4a1 1 0 0 0 1-.88l.37-2.6c.54-.23 1.05-.51 1.5-.87l2.43.98a1 1 0 0 0 1.25-.45l2-3.46a1 1 0 0 0-.21-1.32l-2.06-1.63c.09-.29.09-.6 0-.89z"></path></svg>`
};
function openWindow(app) {
    let winTitle, url, icon;
    if (app === 'filemanager') {
        winTitle = '文件管理器';
        url = '/filemanager_inner/';
        icon = winIcons.filemanager;
    } else if (app === 'about') {
        winTitle = '关于 HNAS';
        url = '/about_inner';
        icon = winIcons.about;
    } else if (app === 'settings') {
        winTitle = '设置';
        url = '/settings_inner';
        icon = winIcons.settings;
    } else {
        return;
    }
    createWindow(winTitle, url, app, icon);
}

function createWindow(title, url, appType, icon) {
    const windowArea = document.getElementById('window-area');
    const win = document.createElement('div');
    win.className = 'win';
    win.dataset.appType = appType;
    win.dataset.winId = 'win' + (++winIdCounter);
    win.style.zIndex = ++zIndexCounter;
    win.innerHTML = `<div class="win-titlebar">
        <span class="win-title">${title}</span>
        <span class="win-titlebar-btns">
          <button class="win-titlebar-btn minimize" title="最小化">${minSvg()}</button>
          <button class="win-titlebar-btn maximize" title="最大化">${maxSvg()}</button>
          <button class="win-titlebar-btn close" title="关闭">${closeSvg()}</button>
        </span>
    </div>
    <iframe src="${url}" class="win-content" frameborder="0"></iframe>`;
    windowArea.appendChild(win);

    // 拖动
    const titlebar = win.querySelector('.win-titlebar');
    let isMaximized = false;
    let prevRect = null;
    titlebar.onmousedown = function (e) {
        if (e.target.closest('.win-titlebar-btn')) return;
        if (win.classList.contains('maximized')) return;
        let offsetX = e.clientX - win.offsetLeft;
        let offsetY = e.clientY - win.offsetTop;
        win.style.zIndex = ++zIndexCounter;
        document.onmousemove = function (e2) {
            win.style.left = (e2.clientX - offsetX) + 'px';
            win.style.top = (e2.clientY - offsetY) + 'px';
        }
        document.onmouseup = function () {
            document.onmousemove = null;
            document.onmouseup = null;
        }
    };
    // 关闭
    win.querySelector('.win-titlebar-btn.close').onclick = function() {
        win.remove();
        updateTaskbar();
    };
    // 最小化
    win.querySelector('.win-titlebar-btn.minimize').onclick = function() {
        win.classList.add('minimized');
        updateTaskbar();
    };
    // 最大化/还原
    win.querySelector('.win-titlebar-btn.maximize').onclick = function() {
        if (win.classList.contains('maximized')) {
            // 还原
            if (prevRect) {
                win.style.left = prevRect.left;
                win.style.top = prevRect.top;
                win.style.width = prevRect.width;
                win.style.height = prevRect.height;
            }
            win.classList.remove('maximized');
        } else {
            // 最大化
            prevRect = {
                left: win.style.left,
                top: win.style.top,
                width: win.style.width,
                height: win.style.height
            };
            win.style.left = '0';
            win.style.top = '0';
            win.style.width = '100vw';
            win.style.height = 'calc(100vh - 48px)';
            win.classList.add('maximized');
        }
    };
    // 默认位置
    win.style.left = 80 + (winIdCounter * 30) + 'px';
    win.style.top = 80 + (winIdCounter * 30) + 'px';
    win.style.width = '600px';
    win.style.height = '380px';
    win.classList.remove('minimized');
    updateTaskbar();
    win.focus();
}

window.reloadFileManager = function(path) {
    let win = document.querySelector('.win iframe[src^="/filemanager_inner"]');
    if (win) win.src = '/filemanager_inner/' + (path || '');
};

// 任务栏相关
function updateTaskbar() {
    const taskbar = document.getElementById('taskbar');
    taskbar.innerHTML = '';
    const wins = document.querySelectorAll('.win');
    wins.forEach(win => {
        const isMin = win.classList.contains('minimized');
        const isActive = !isMin && (+win.style.zIndex === zIndexCounter);
        let iconHtml = winIcons[win.dataset.appType] || '';
        let title = win.querySelector('.win-title')?.innerText || '';
        const btn = document.createElement('div');
        btn.className = 'taskbar-btn' + (isActive ? ' active' : '');
        btn.innerHTML = iconHtml + '<span>' + title + '</span>';
        btn.onclick = function() {
            if (win.classList.contains('minimized')) {
                win.classList.remove('minimized');
            }
            win.style.zIndex = ++zIndexCounter;
            updateTaskbar();
        }
        taskbar.appendChild(btn);
    });
}

// SVG 图标
function minSvg() {
    return `<svg width="18" height="18"><rect x="4" y="13" width="10" height="2" rx="1" fill="#fff"/></svg>`;
}
function maxSvg() {
    return `<svg width="18" height="18"><rect x="4" y="5" width="10" height="8" rx="2" fill="#fff" stroke="#fff" stroke-width="1"/></svg>`;
}
function closeSvg() {
    return `<svg width="18" height="18"><line x1="5" y1="5" x2="13" y2="13" stroke="#fff" stroke-width="2"/><line x1="13" y1="5" x2="5" y2="13" stroke="#fff" stroke-width="2"/></svg>`;
}

// 保证窗口激活时高亮任务栏
document.addEventListener('click', function(e){
    let win = e.target.closest('.win');
    if (win) {
        win.style.zIndex = ++zIndexCounter;
        updateTaskbar();
    }
});