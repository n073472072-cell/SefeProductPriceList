// frontend/public/js/pages/users.js
async function initUsers() {
    const tableBody = document.querySelector('#users-table tbody');
    const modal = document.getElementById('add-user-modal');
    const addBtn = document.getElementById('add-user-btn');
    const cancelBtn = document.getElementById('cancel-add-user');
    const form = document.getElementById('add-user-form');

    // Load users
    async function loadUsers() {
        try {
            const users = await api.get('/api/users/');
            renderUsers(users);
        } catch (error) {
            alert('無法載入使用者列表: ' + error.message);
        }
    }

    function renderUsers(users) {
        tableBody.innerHTML = users.map(user => `
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;">${user.id}</td>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;">${user.username}</td>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;">${user.full_name || '-'}</td>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;">
                    <span style="background: ${user.role === 'admin' ? '#fee2e2' : '#e0f2fe'}; color: ${user.role === 'admin' ? '#991b1b' : '#075985'}; padding: 4px 8px; border-radius: 9999px; font-size: 0.8rem;">
                        ${user.role}
                    </span>
                </td>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;">
                    <button onclick="editUser('${user.id}', '${user.username}', '${user.role}', '${user.full_name || ''}')" style="color: #2563eb; border: 1px solid #2563eb; background: white; padding: 4px 8px; border-radius: 4px; cursor: pointer; margin-right: 5px;">
                        編輯
                    </button>
                    <button onclick="deleteUser(${user.id})" style="color: #ef4444; border: 1px solid #ef4444; background: white; padding: 4px 8px; border-radius: 4px; cursor: pointer;">
                        刪除
                    </button>
                </td>
            </tr>
        `).join('');
    }

    // Add User
    addBtn.onclick = () => modal.style.display = 'flex';
    cancelBtn.onclick = () => modal.style.display = 'none';

    form.onsubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        try {
            await api.post('/api/users/', data);
            alert('使用者建立成功');
            modal.style.display = 'none';
            form.reset();
            loadUsers();
        } catch (error) {
            alert('建立失敗: ' + error.message);
        }
    };

    // Edit User
    const editModal = document.getElementById('edit-user-modal');
    const editForm = document.getElementById('edit-user-form');
    const cancelEditBtn = document.getElementById('cancel-edit-user');

    cancelEditBtn.onclick = () => editModal.style.display = 'none';

    window.editUser = (id, username, role, fullName) => {
        editForm.id.value = id;
        editForm.username.value = username;
        editForm.full_name.value = fullName || '';
        editForm.role.value = role;
        editForm.password.value = ''; // 清空密碼欄位
        editModal.style.display = 'flex';
    };

    editForm.onsubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData(editForm);
        const data = Object.fromEntries(formData.entries());

        // 如果密碼為空，移除該欄位，避免不小心將密碼設為空字串
        if (!data.password) {
            delete data.password;
        }

        try {
            await api.request(`/api/users/${data.id}`, {
                method: 'PUT',
                body: JSON.stringify(data)
            });
            alert('使用者更新成功');
            editModal.style.display = 'none';
            loadUsers();
        } catch (error) {
            alert('更新失敗: ' + error.message);
        }
    };

    // Delete User (Global function for onclick)
    window.deleteUser = async (id) => {
        if (!confirm('確定要刪除此使用者嗎？此動作無法復原。')) return;

        try {
            await api.delete(`/api/users/${id}`);
            loadUsers();
        } catch (error) {
            alert('刪除失敗: ' + error.message);
        }
    };

    // Initial load
    loadUsers();
}

initUsers();
