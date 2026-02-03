const express = require('express');
const path = require('path');
const { createProxyMiddleware } = require('http-proxy-middleware');
const app = express();

// 1. 優先處理靜態檔案 (包含 favicon.ico)
// 將靜態檔案放在代理之前，確保它們不會被轉發給後端
app.use(express.static(path.join(__dirname, 'public')));

// 2. API 代理設定
app.use('/api', createProxyMiddleware({
    target: 'http://127.0.0.1:8000',
    changeOrigin: true,
    onProxyReq: (proxyReq, req, res) => {
        // console.log(`[Proxy] ${req.method} ${req.url}`);
    },
    onError: (err, req, res) => {
        console.error('[Proxy Error]:', err.message);
        res.status(502).json({
            error: 'Backend Unreachable',
            message: '服務啟動中，請於 1 分鐘後重新整理。',
            detail: err.message
        });
    }
}));

// 3. 處理 SPA 路由 (如果找不到檔案，回傳 index.html)
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, '0.0.0.0', () => {
    console.log(`🚀 伺服器已啟動：http://0.0.0.0:${PORT}`);
});
