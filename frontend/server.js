const express = require('express');
const path = require('path');
const { createProxyMiddleware } = require('http-proxy-middleware');
const app = express();

// 1. API 代理設定
// 當請求路徑以 /api 開頭時，轉發給內部的 FastAPI (8000 端口)
app.use('/api', createProxyMiddleware({
    target: 'http://127.0.0.1:8000',
    changeOrigin: true,
    onError: (err, req, res) => {
        console.error('Proxy Error:', err);
        res.status(502).send('後端服務啟動中或暫時無法連線，請稍後再試。');
    }
}));

// 2. 靜態檔案設定
app.use(express.static(path.join(__dirname, 'public')));

// 3. 處理 SPA 路由
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// 使用環境變數中的 PORT 或預設 3000
const PORT = process.env.PORT || 3000;
app.listen(PORT, '0.0.0.0', () => {
    console.log(`🚀 伺服器已啟動：端口 ${PORT}`);
    console.log(`🔗 API 代理目標：http://127.0.0.1:8000`);
});
