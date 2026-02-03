// frontend/public/js/pages/dashboard.js
async function initDashboard() {
    const modal = document.getElementById('news-modal');
    const title = document.getElementById('modal-title');
    const content = document.getElementById('modal-content');
    const hideCheck = document.getElementById('hide-news-check');
    const closeBtn = document.getElementById('close-modal');

    // 檢查 "今天不再顯示"
    const hideUntil = localStorage.getItem('hideNewsUntil');
    const now = new Date().getTime();

    // 檢查權限並顯示管理員卡片
    const user = auth.getUser();
    if (user && user.role === 'admin') {
        console.log('Rendering Admin Section: Users -> News');
        const grid = document.querySelector('.card-grid');

        // 建立管理員區塊
        // 建立管理員區塊
        const adminSection = `
            <div class="card" onclick="window.location.hash='#/users'"
                style="cursor:pointer; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; min-height: 160px; border-left: 4px solid var(--accent-red); background: white;">
                <span style="font-size: 40px; margin-bottom: 16px;">👥</span>
                <h3 style="margin: 0; font-size: 18px; color: var(--accent-red);">帳號管理</h3>
                <p style="margin: 8px 0 0 0; font-size: 13px; color: var(--text-secondary);">新增或修改使用者權限</p>
            </div>
            <div class="card" onclick="window.location.hash='#/news-management'"
                style="cursor:pointer; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; min-height: 160px; border-left: 4px solid var(--accent-red); background: white;">
                <span style="font-size: 40px; margin-bottom: 16px;">📰</span>
                <h3 style="margin: 0; font-size: 18px; color: var(--accent-red);">最新消息管理</h3>
                <p style="margin: 8px 0 0 0; font-size: 13px; color: var(--text-secondary);">發布或編輯系統公告</p>
            </div>
        `;
        grid.insertAdjacentHTML('beforeend', adminSection);
    }

    // 處理最新消息彈窗逻辑
    try {
        const news = await api.get('/api/news/latest');

        if (news) {
            const hiddenNewsId = localStorage.getItem('hiddenNewsId');
            const hideUntil = localStorage.getItem('hideNewsUntil');
            const now = new Date().getTime();

            // 判斷是否顯示:
            // 1. 如果沒有隱藏紀錄 -> 顯示
            // 2. 如果隱藏期限已過 -> 顯示
            // 3. 如果是新的公告 (ID 不同) -> 強制顯示
            let shouldShow = true;

            if (hiddenNewsId && parseInt(hiddenNewsId) === news.id) {
                // ID 相同，檢查是否在隱藏期限內
                if (hideUntil && now < parseInt(hideUntil)) {
                    shouldShow = false;
                }
            }

            if (shouldShow) {
                title.textContent = news.title;
                content.innerHTML = news.content;
                modal.style.display = 'flex';

                // 綁定關閉事件
                closeBtn.onclick = () => {
                    if (hideCheck.checked) {
                        // 設定到明天凌晨
                        const tomorrow = new Date();
                        tomorrow.setHours(24, 0, 0, 0);
                        localStorage.setItem('hideNewsUntil', tomorrow.getTime().toString());
                        // 紀錄目前已隱藏的公告 ID
                        localStorage.setItem('hiddenNewsId', news.id.toString());
                    }
                    modal.style.display = 'none';
                };
            } else {
                // 即使不顯示，也要綁定關閉按鈕以防萬一 (雖然 modal 是 hidden)
                closeBtn.onclick = () => modal.style.display = 'none';
            }
        }
    } catch (error) {
        console.error('取得最新消息失敗:', error);
        closeBtn.onclick = () => modal.style.display = 'none';
    }
}

initDashboard();
