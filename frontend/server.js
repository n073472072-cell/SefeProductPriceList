const express = require('express');
const path = require('path');
const { createProxyMiddleware } = require('http-proxy-middleware');
const app = express();

// 1. API 代理設定 (最優先)
// 使用這種掛載方式：確保 /api 完整路徑會直接傳遞給後端，不做路徑重寫
app.use(createProxyMiddleware('/api', {
    target: 'http://127.0.0.1:8000',
    changeOrigin: true,
    onProxyReq: (proxyReq, req, res) => {
        // console.log(`[Proxy Request]: ${req.method} ${req.url}`);
    },
    onError: (err, req, res) => {
        console.error('[Proxy Error]:', err.message);
        res.status(502).json({
            error: 'Backend Connection Failed',
            message: '後端服務啟動中，請於 30 秒後重新整理頁面。',
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
    console.log(`🔗 內部轉送目標：http://127.0.0.1:8000`);
});
