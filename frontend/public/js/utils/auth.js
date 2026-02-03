// frontend/public/js/utils/auth.js
const auth = {
    login: (token) => {
        localStorage.setItem('accessToken', token);
    },
    logout: () => {
        localStorage.removeItem('accessToken');
    },
    getToken: () => {
        return localStorage.getItem('accessToken');
    },
    isAuthenticated: () => {
        return !!localStorage.getItem('accessToken');
    },
    getUser: () => {
        const token = auth.getToken();
        if (!token) return null;
        try {
            const payload = JSON.parse(atob(token.split('.')[1]));

            // 檢查是否已過期
            const now = Math.floor(Date.now() / 1000);
            if (payload.exp && now > payload.exp) {
                console.warn('Token 已過期');
                auth.logout();
                return null;
            }

            return { username: payload.sub, role: payload.role, exp: payload.exp };
        } catch (e) {
            console.error('解析 Token 失敗:', e);
            auth.logout();
            return null;
        }
    }
};
