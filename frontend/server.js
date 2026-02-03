const express = require('express');
const path = require('path');
const { createProxyMiddleware } = require('http-proxy-middleware');
const app = express();

// 1. 優先處理靜態檔案
app.use(express.static(path.join(__dirname, 'public')));

// 2. API 代理設定
// 我們將請求直接轉發，不進行 pathRewrite，因為 FastAPI 內部路由已包含 /api
app.use('/api', createProxyMiddleware({
    target: 'http://127.0.0.1:8000',
    changeOrigin: true,
    ws: true, // 支援 websocket (如果以後需要)
    onProxyReq: (proxyReq, req, res) => {
        // console.log(`[Proxy Request]: ${req.method} ${req.url}`);
    },
    onProxyRes: (proxyRes, req, res) => {
        // console.log(`[Proxy Response]: ${proxyRes.statusCode} ${req.url}`);
    },
    onError: (err, req, res) => {
        console.error('[Proxy Error]:', err.message);
        res.status(502).json({
            error: 'Backend Connection Failed',
            message: '後端服務響應超時或未啟動',
            detail: err.message
        });
    }
}));

// 3. 處理 SPA 路由
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, '0.0.0.0', () => {
    console.log(`🚀 雲端入口代理由端口 ${PORT} 啟動`);
    console.log(`🔗 API 目標定位：http://127.0.0.1:8000`);
});
