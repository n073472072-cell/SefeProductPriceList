// frontend/public/js/router.js
const routes = {
    '#/login': { path: '/pages/login.html', script: '/js/pages/login.js' },
    '#/dashboard': { path: '/pages/dashboard.html', script: '/js/pages/dashboard.js', private: true },
    '#/customer-price': { path: '/pages/products.html', script: '/js/pages/products.js', private: true, type: 'customer' },
    '#/distributor-price': { path: '/pages/products.html', script: '/js/pages/products.js', private: true, type: 'distributor' },
    '#/news-management': { path: '/pages/news_management.html', script: '/js/pages/news_management.js', private: true, adminOnly: true },
    '#/batch-import': { path: '/pages/batch_import.html', script: '/js/pages/batch_import.js', private: true, adminOnly: true },
    '#/users': { path: '/pages/users.html', script: '/js/pages/users.js', private: true, adminOnly: true },
};

const appContainer = document.getElementById('app');

async function router() {
    const fullHash = window.location.hash || '#/login';
    const hash = fullHash.split('?')[0]; // 移除查詢參數部分再進行路由比對
    const route = routes[hash] || { path: '/pages/404.html' };

    // 權限檢查
    if (route.private && !auth.isAuthenticated()) {
        window.location.hash = '#/login';
        return;
    }

    const user = auth.getUser();
    if (route.adminOnly && (!user || user.role !== 'admin')) {
        alert('權限不足！');
        window.location.hash = '#/dashboard';
        return;
    }

    try {
        const response = await fetch(route.path);
        if (!response.ok) throw new Error('頁面不存在');
        appContainer.innerHTML = await response.text();

        // 載入腳本
        if (route.script) {
            const oldScript = document.getElementById('page-script');
            if (oldScript) oldScript.remove();

            const script = document.createElement('script');
            script.id = 'page-script';
            script.src = `${route.script}?v=${Date.now()}_${Math.random()}`;
            script.type = 'module';
            document.body.appendChild(script);
        }
    } catch (error) {
        console.error('路由錯誤:', error);
        appContainer.innerHTML = '<h1>載入頁面失敗</h1>';
    }
}

window.addEventListener('hashchange', router);
window.addEventListener('DOMContentLoaded', router);
export { router };
