const express = require('express');
const path = require('path');
const app = express();

// 1. 靜態檔案設定 (確保 public 資料夾路徑正確)
app.use(express.static(path.join(__dirname, 'public')));

// 2. 處理根目錄 (/) 的請求
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// 3. 處理 SPA 前端路由的請求 (放在最後)
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(3000, () => {
    console.log('🚀 伺服器已啟動：http://localhost:3000');
});
