// frontend/public/js/pages/products.js
async function initProducts() {
    const hash = window.location.hash;
    const isDistributor = hash.startsWith('#/distributor-price');
    const isCustomer = hash.startsWith('#/customer-price');
    const user = auth.getUser();
    const isAdmin = user && user.role === 'admin';

    // UI elements
    const pageTitle = document.getElementById('page-title');
    const priceHeader = document.getElementById('price-header');
    const actionHeader = document.getElementById('action-header');
    const searchInput = document.getElementById('search-input');
    const searchIcon = document.getElementById('search-icon');
    const categoryFilter = document.getElementById('category-filter');
    const resetFilterBtn = document.getElementById('reset-filter-btn');
    const resultCount = document.getElementById('result-count');
    const addProductBtn = document.getElementById('add-product-btn');
    const productModal = document.getElementById('product-modal');
    const productForm = document.getElementById('product-form');
    const modalTitle = document.getElementById('modal-title');
    const pPriceLabel = document.getElementById('p-price-label');

    pageTitle.textContent = isDistributor ? '產品經銷售價' : '產品客戶售價(未稅)';
    priceHeader.textContent = isDistributor ? '經銷售價' : '售價 (未稅)';
    pPriceLabel.textContent = isDistributor ? '經銷售價' : '售價 (未稅)';

    if (isAdmin) {
        document.getElementById('admin-actions').style.display = 'block';
        if (actionHeader) actionHeader.style.display = 'table-cell';

        // Add Product Logic
        if (addProductBtn) {
            addProductBtn.onclick = () => {
                modalTitle.textContent = '新增產品';
                productForm.reset();
                document.getElementById('p-id').value = '';
                document.getElementById('p-updated').value = new Date().toLocaleDateString('zh-TW', { year: 'numeric', month: '2-digit', day: '2-digit' }).replaceAll('-', '/');
                productModal.style.display = 'block';
            };
        }

        // Form Submit
        productForm.onsubmit = async (e) => {
            e.preventDefault();
            const id = document.getElementById('p-id').value;
            const data = {
                product_code: document.getElementById('p-code').value,
                name: document.getElementById('p-name').value,
                category: document.getElementById('p-category').value,
                specification: document.getElementById('p-specification').value,
                price_spec: document.getElementById('p-price-spec').value,
                status: document.getElementById('p-status').value,
                notes: document.getElementById('p-notes').value,
                price_type: isDistributor ? 'distributor' : 'customer'
            };

            if (isDistributor) {
                data.distributor_price = document.getElementById('p-price').value || '0';
                data.customer_price = '0';
            } else {
                data.customer_price = document.getElementById('p-price').value || '0';
                data.distributor_price = '0';
            }

            try {
                if (id) {
                    await api.put(`/api/products/${id}`, data);
                } else {
                    await api.post('/api/products/', data);
                }
                productModal.style.display = 'none';
                renderProducts(); // Refresh list
            } catch (error) {
                alert('儲存失敗: ' + error.message);
            }
        };

        // 匯入功能
        const importBtn = document.getElementById('import-btn');
        if (importBtn) {
            importBtn.onclick = () => {
                const mode = isDistributor ? 'distributor' : 'customer';
                window.location.hash = `#/batch-import?mode=${mode}`;
            };
        }



        // 清除功能
        const clearBtn = document.getElementById('clear-btn');
        if (clearBtn) {
            clearBtn.onclick = async () => {
                const mode = isDistributor ? 'distributor' : 'customer';
                const modeText = isDistributor ? '經銷商價格' : '產品客戶售價';
                if (confirm(`⚠️ 確定要刪除所有「${modeText}」資料嗎？\n這將永久移除目前分頁的所有售價與備註，但不會影響另一分頁的資料。`)) {
                    try {
                        const result = await api.delete(`/api/products/clear-all?mode=${mode}`);
                        alert(result.message || '資料已成功刪除');
                        renderProducts();
                    } catch (error) {
                        console.error('清除錯誤詳情:', error);
                        const errorMsg = error.message || error.detail || JSON.stringify(error);
                        alert('刪除失敗: ' + errorMsg);
                    }
                }
            };
        }
    }

    // Search & Filter Logic
    let searchTimeout;
    if (searchInput) {
        searchInput.oninput = () => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => renderProducts(), 300); // 體驗優化：自動搜尋 (Debounce)
        };
    }
    if (categoryFilter) {
        categoryFilter.onchange = () => renderProducts();
    }
    if (resetFilterBtn) {
        resetFilterBtn.onclick = () => {
            searchInput.value = '';
            categoryFilter.value = '';
            renderProducts();
        };
    }

    // Excel 匯出 (原為下載範本)
    const templateBtn = document.getElementById('download-template-btn');
    if (templateBtn) {
        templateBtn.onclick = async () => {
            const mode = isDistributor ? 'distributor' : 'customer';
            try {
                const response = await api.request(`/api/products/export?mode=${mode}`, { method: 'GET' });
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                const dateStr = new Date().toISOString().slice(0, 10);
                a.download = isDistributor ? `經銷售價匯出_${dateStr}.xlsx` : `客戶售價匯出_${dateStr}.xlsx`;
                document.body.appendChild(a);
                a.click();
                a.remove();
            } catch (error) {
                alert('匯出失敗: ' + error.message);
            }
        };
    }

    window.editProduct = (id, productJson) => {
        const p = JSON.parse(decodeURIComponent(productJson));
        modalTitle.textContent = '修改產品';
        document.getElementById('p-id').value = p.id;
        document.getElementById('p-code').value = p.product_code;
        document.getElementById('p-name').value = p.name;
        document.getElementById('p-category').value = p.category || '';
        document.getElementById('p-specification').value = p.specification || '';
        document.getElementById('p-price').value = isDistributor ? p.distributor_price : p.customer_price;
        document.getElementById('p-price-spec').value = p.price_spec || '';
        document.getElementById('p-status').value = (p.status || '').toLowerCase().includes('inactive') || p.status === '下架' ? 'inactive' : 'active';
        document.getElementById('p-notes').value = p.notes || '';
        document.getElementById('p-updated').value = p.updated_at ? new Date(p.updated_at).toLocaleDateString('zh-TW', { year: 'numeric', month: '2-digit', day: '2-digit' }).replaceAll('-', '/') : '-';
        productModal.style.display = 'block';
    };

    window.deleteProduct = async (id, name) => {
        if (confirm(`確定要刪除產品「${name}」嗎？`)) {
            try {
                await api.delete(`/api/products/${id}`);
                alert('刪除成功');
                renderProducts();
            } catch (error) {
                console.error('刪除錯誤詳情:', error);
                const errorMsg = error.message || error.detail || JSON.stringify(error);
                alert('刪除失敗: ' + errorMsg);
            }
        }
    };

    async function renderProducts() {
        const tbody = document.querySelector('#product-table tbody');
        const query = searchInput.value.toLowerCase().trim();
        const selectedCategory = categoryFilter.value;

        tbody.innerHTML = '<tr><td colspan="10" style="text-align:center;">載入中...</td></tr>';

        try {
            const currentType = isDistributor ? 'distributor' : 'customer';
            const products = await api.get(`/api/products/?price_type=${currentType}&limit=5000`);

            // Update category dropdown
            const currentSelection = categoryFilter.value;
            const uniqueCategories = [...new Set(products.map(p => p.category).filter(c => c))].sort();
            if (uniqueCategories.length + 1 !== categoryFilter.options.length) {
                categoryFilter.innerHTML = '<option value="">所有分類</option>';
                uniqueCategories.forEach(cat => {
                    const opt = document.createElement('option');
                    opt.value = cat;
                    opt.textContent = cat;
                    categoryFilter.appendChild(opt);
                });
                categoryFilter.value = currentSelection;
            }

            // Apply Filters (智慧搜尋：包含編號、名稱、分類、規格)
            const filteredProducts = products.filter(p => {
                const matchesSearch = !query ||
                    p.product_code.toLowerCase().includes(query) ||
                    p.name.toLowerCase().includes(query) ||
                    (p.category || '').toLowerCase().includes(query) ||
                    (p.specification || '').toLowerCase().includes(query);
                const matchesCategory = !selectedCategory || p.category === selectedCategory;
                return matchesSearch && matchesCategory;
            });

            // Update Result Count
            if (resultCount) {
                resultCount.textContent = `共找到 ${filteredProducts.length} 筆資料`;
            }

            tbody.innerHTML = '';
            if (filteredProducts.length === 0) {
                tbody.innerHTML = '<tr><td colspan="10" style="text-align:center;">尚無相關資料</td></tr>';
                return;
            }

            filteredProducts.forEach(p => {
                const tr = document.createElement('tr');
                const statusText = (() => {
                    const s = (p.status || '').toString().trim().toLowerCase();
                    if (s === 'active' || s === '上架') return '上架';
                    if (s === 'inactive' || s === '下架') return '下架';
                    return p.status || '-';
                })();

                const actionCell = isAdmin ? `
                    <td style="display:flex; gap:5px;">
                        <button onclick="editProduct(${p.id}, '${encodeURIComponent(JSON.stringify(p))}')" 
                            style="background:#f59e0b; color:white; border:none; padding:4px 8px; border-radius:4px; cursor:pointer;">修改</button>
                        <button onclick="deleteProduct(${p.id}, '${p.name}')" 
                            style="background:#ef4444; color:white; border:none; padding:4px 8px; border-radius:4px; cursor:pointer;">刪除</button>
                    </td>
                ` : '';

                tr.innerHTML = `
                    <td>${p.product_code}</td>
                    <td>${p.name}</td>
                    <td>${p.category || '-'}</td>
                    <td>${p.specification || '-'}</td>
                    <td>${isDistributor ? p.distributor_price : p.customer_price}</td>
                    <td>${p.price_spec || '-'}</td>
                    <td>${p.updated_at ? new Date(p.updated_at).toLocaleDateString('zh-TW', { year: 'numeric', month: '2-digit', day: '2-digit' }).replaceAll('-', '/') : '-'}</td>
                    <td>${statusText}</td>
                    <td class="notes-cell" data-notes="${p.notes || ''}">${p.notes || ''}</td>
                    ${actionCell}
                `;
                tr.style.borderBottom = '1px solid #eee';
                tbody.appendChild(tr);

                const notesCell = tr.querySelector('.notes-cell');
                const tooltip = document.getElementById('custom-tooltip');

                notesCell.onmouseenter = (e) => {
                    const text = notesCell.getAttribute('data-notes').trim();
                    if (!text) return;
                    tooltip.textContent = text;
                    tooltip.style.display = 'block';
                };
                notesCell.onmousemove = (e) => {
                    tooltip.style.left = (e.clientX + 15) + 'px';
                    tooltip.style.top = (e.clientY + 15) + 'px';
                };
                notesCell.onmouseleave = () => {
                    tooltip.style.display = 'none';
                };
            });
        } catch (error) {
            tbody.innerHTML = `<tr><td colspan="10" style="text-align:center; color:red;">載入失敗: ${error.message}</td></tr>`;
        }
    }

    renderProducts();
}

initProducts();
