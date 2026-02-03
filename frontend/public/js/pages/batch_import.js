// frontend/public/js/pages/batch_import.js
async function initBatchImport() {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const status = document.getElementById('upload-status');

    dropZone.onclick = () => fileInput.click();

    dropZone.ondragover = (e) => {
        e.preventDefault();
        dropZone.style.borderColor = '#2563eb';
    };

    dropZone.ondragleave = () => {
        dropZone.style.borderColor = '#cbd5e1';
    };

    dropZone.ondrop = (e) => {
        e.preventDefault();
        dropZone.style.borderColor = '#cbd5e1';
        const files = e.dataTransfer.files;
        if (files.length > 0) handleUpload(files[0]);
    };

    fileInput.onchange = () => {
        if (fileInput.files.length > 0) handleUpload(fileInput.files[0]);
    };

    // 從 Hash 取得匯入模式 (支援 #/batch-import?mode=customer)
    function getImportMode() {
        const fullHash = window.location.hash;
        console.log('[DEBUG] Current Hash:', fullHash);
        const hashParts = fullHash.split('?');
        const queryStr = hashParts.length > 1 ? hashParts[1] : '';
        const urlParams = new URLSearchParams(queryStr);
        const mode = urlParams.get('mode') || 'all';
        console.log('[DEBUG] Resolved Mode:', mode);
        return mode;
    }

    async function handleUpload(file) {
        const importMode = getImportMode();
        status.innerHTML = `<p style="color:blue;">正在上傳: ${file.name} (模式: ${importMode === 'customer' ? '客戶售價' : '經銷售價'})...</p>`;

        const formData = new FormData();
        formData.append('file', file);

        try {
            const importMode = getImportMode();
            // 將模式作為 Query Parameter 傳遞
            const result = await api.upload(`/api/products/upload?import_mode=${importMode}`, formData);
            status.innerHTML = `<p style="color:green;">✅ ${result.message}</p>`;
        } catch (error) {
            const msg = error.message || (typeof error === 'string' ? error : JSON.stringify(error));
            status.innerHTML = `<p style="color:red;">❌ 上傳失敗: ${msg}</p>`;
        }
    }
}

initBatchImport();
