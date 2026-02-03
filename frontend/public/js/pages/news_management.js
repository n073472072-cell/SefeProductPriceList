// frontend/public/js/pages/news_management.js
async function initNewsManagement() {
    // 確保 Quill 已載入 (透過 router 動態注入腳本可能需要檢查)
    if (typeof Quill === 'undefined') {
        setTimeout(initNewsManagement, 100);
        return;
    }

    // 完整工具列配置
    const toolbarOptions = [
        ['bold', 'italic', 'underline', 'strike'],        // 切換按鈕
        ['blockquote', 'code-block'],
        [{ 'header': 1 }, { 'header': 2 }],               // 標題
        [{ 'list': 'ordered' }, { 'list': 'bullet' }],
        [{ 'script': 'sub' }, { 'script': 'super' }],      // 上標/下標
        [{ 'indent': '-1' }, { 'indent': '+1' }],          // 縮排
        [{ 'direction': 'rtl' }],                         // 文字方向
        [{ 'size': ['small', false, 'large', 'huge'] }],  // 字體大小
        [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
        [{ 'color': [] }, { 'background': [] }],          // 顏色
        [{ 'font': [] }],
        [{ 'align': [] }],
        ['clean'],                                         // 清除格式
        ['link', 'image', 'video']                        // 媒體
    ];

    // 確保容器存在
    const container = document.getElementById('editor-container');
    if (!container) {
        // 如果找不到容器，稍後重試 (這在 SPA 切換過快時可能發生)
        setTimeout(initNewsManagement, 50);
        return;
    }

    // 防止重複初始化
    if (document.querySelector('.ql-toolbar')) {
        return;
    }

    const quill = new Quill('#editor-container', {
        modules: {
            toolbar: toolbarOptions
        },
        theme: 'snow'
    });

    const titleInput = document.getElementById('news-title');

    // 載入草稿或最新消息
    async function loadContent() {
        const draftTitle = localStorage.getItem('news_draft_title');
        const draftContent = localStorage.getItem('news_draft_content');

        if (draftTitle || draftContent) {
            titleInput.value = draftTitle || '';
            if (draftContent) {
                quill.clipboard.dangerouslyPasteHTML(draftContent);
            }
            console.log('已載入草稿');
        } else {
            try {
                const latest = await api.get('/api/news/latest');
                if (latest) {
                    titleInput.value = latest.title;
                    quill.clipboard.dangerouslyPasteHTML(latest.content);
                }
            } catch (error) {
                console.log('尚無最新消息或載入失敗', error);
            }
        }
    }

    loadContent();

    // 自動儲存草稿
    quill.on('text-change', () => {
        localStorage.setItem('news_draft_content', quill.root.innerHTML);
    });

    titleInput.addEventListener('input', () => {
        localStorage.setItem('news_draft_title', titleInput.value);
    });

    // 預覽功能
    const previewBtn = document.getElementById('preview-btn');
    const previewModal = document.getElementById('preview-modal');
    const closePreviewBtn = document.getElementById('close-preview');
    const previewTitle = document.getElementById('preview-title');
    const previewContent = document.getElementById('preview-content');

    if (previewBtn) {
        previewBtn.onclick = () => {
            previewTitle.textContent = titleInput.value;
            previewContent.innerHTML = quill.root.innerHTML;
            previewModal.style.display = 'flex';
        };

        closePreviewBtn.onclick = () => {
            previewModal.style.display = 'none';
        };

        // 點擊背景關閉
        previewModal.onclick = (e) => {
            if (e.target === previewModal) {
                previewModal.style.display = 'none';
            }
        };
    }

    const form = document.getElementById('news-form');
    form.onsubmit = async (e) => {
        e.preventDefault();
        const title = titleInput.value;
        const content = quill.root.innerHTML;

        try {
            await api.post('/api/news/', {
                title,
                content,
                category: '一般',
                is_active: true
            });

            // 清除草稿
            localStorage.removeItem('news_draft_title');
            localStorage.removeItem('news_draft_content');

            alert('公告已發布');
            window.location.hash = '#/dashboard';
        } catch (error) {
            alert('發布失敗: ' + error.message);
        }
    };
}

initNewsManagement();
