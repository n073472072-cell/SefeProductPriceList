// frontend/public/js/utils/api.js
const API_BASE = 'http://localhost:8000';

const api = {
    async request(endpoint, options = {}) {
        const token = localStorage.getItem('accessToken');
        const headers = {
            ...options.headers,
        };

        // 如果沒有手動指定 Content-Type，且不是 FormData，才預設為 application/json
        if (!headers['Content-Type'] && !(options.body instanceof FormData)) {
            headers['Content-Type'] = 'application/json';
        }

        // 如果手動傳入 null 或 'undefined'，則刪除該 header (讓瀏覽器自動處理)
        if (headers['Content-Type'] === null || headers['Content-Type'] === 'undefined') {
            delete headers['Content-Type'];
        }
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        try {
            const response = await fetch(`${API_BASE}${endpoint}`, {
                ...options,
                headers,
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ detail: `HTTP 錯誤: ${response.status}` }));
                let errorMsg = errorData.detail || '發生未知錯誤';
                if (typeof errorMsg !== 'string') {
                    errorMsg = JSON.stringify(errorMsg);
                }
                throw new Error(errorMsg);
            }

            if (response.headers.get('content-type')?.includes('application/json')) {
                return response.json();
            }
            return response;
        } catch (error) {
            console.error(`API 錯誤 [${options.method || 'GET'} ${endpoint}]:`, error);
            throw error;
        }
    },
    get: (endpoint) => api.request(endpoint, { method: 'GET' }),
    post: (endpoint, body) => api.request(endpoint, { method: 'POST', body: JSON.stringify(body) }),
    put: (endpoint, body) => api.request(endpoint, { method: 'PUT', body: JSON.stringify(body) }),
    delete: (endpoint) => api.request(endpoint, { method: 'DELETE' }),
    upload: (endpoint, formData) => {
        return api.request(endpoint, {
            method: 'POST',
            body: formData,
            headers: { 'Content-Type': null } // 告知 request 不要設定任何 Content-Type
        });
    },
};
