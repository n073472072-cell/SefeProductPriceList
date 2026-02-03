// frontend/public/js/pages/login.js
const loginForm = document.getElementById('login-form');
const loginButton = document.getElementById('login-button');
const formError = document.getElementById('form-error');

loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    formError.textContent = '';

    const formData = new FormData(loginForm);
    const span = loginButton.querySelector('span');
    const loader = loginButton.querySelector('.loader');

    span.style.display = 'none';
    loader.style.display = 'inline';
    loginButton.disabled = true;

    try {
        const body = new URLSearchParams();
        body.append('username', formData.get('username'));
        body.append('password', formData.get('password'));
        body.append('remember_me', loginForm.remember_me.checked);

        const response = await fetch('http://localhost:8000/api/auth/token', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: body,
        });

        const data = await response.json();
        if (!response.ok) throw new Error(data.detail || '登入失敗');

        auth.login(data.access_token);
        window.location.hash = '#/dashboard';

    } catch (error) {
        formError.textContent = error.message;
    } finally {
        span.style.display = 'inline';
        loader.style.display = 'none';
        loginButton.disabled = false;
    }
});
