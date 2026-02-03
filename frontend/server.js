const express = require('express');
const path = require('path');
const { createProxyMiddleware } = require('http-proxy-middleware');
const app = express();

// 1. API 代理設定
// http-proxy-middleware v3.0 建議寫法：
// 使用 pathFilter 確保 /api 請求被轉發，且完整保留路徑
app.use(createProxyMiddleware({
    target: 'http://127.0.0.1:8000',
    changeOrigin: true,
    pathFilter: '/api',
    onError: (err, req, res) => {
        console.error('[Proxy Error]:', err.message);
        res.status(502).json({
            error: 'Backend Connection Failed',
            message: '後端服務準備中，請稍候重試。',
            detail: err.message
        });
    }
}));

// 2. 靜態檔案設定
app.use(express.static(path.join(__dirname, 'public')));

// 3. 處理 SPA 路由
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, '0.0.0.0', () => {
    console.log(`🚀 網關已啟動：http://0.0.0.0:${PORT}`);
});
