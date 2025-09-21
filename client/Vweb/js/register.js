import { api, hideLoading, showLoading } from './core/api.js';

document.getElementById('btnLogin').addEventListener('click', () => {
  windows.location.href = 'login.html';
});

document.getElementById('btnSendCode').onclick = async () => {
  const email = document.querySelector('#formRegister [name="email"]').value;
  try {
    showLoading();
    await api.sendCode({ email });
    hideLoading();
    alert('验证码已发送');
  } catch (e) {
    alert(e.message);
  }
};

document.getElementById('formRegister').onsubmit = async (e) => {
  e.preventDefault();
  const fd = new FormData(e.target);
  try {
    showLoading();
    await api.register(Object.fromEntries(fd));
    hideLoading();
    alert('注册成功，请登录');
  } catch (err) {
    alert(err.message);
  }
};