import { api } from './api.js';
import { state } from './state.js';

if (state.isLogged()) {
//   location.href = 'main.html';
}

document.getElementById('btnSendCode').onclick = async () => {
  const email = document.querySelector('#formRegister [name="email"]').value;
  try {
    await api.sendCode(email);
    alert('验证码已发送');
  } catch (e) {
    alert(e.message);
  }
};

document.getElementById('formRegister').onsubmit = async (e) => {
  e.preventDefault();
  const fd = new FormData(e.target);
  try {
    await api.register(Object.fromEntries(fd));
    alert('注册成功，请登录');
  } catch (err) {
    alert(err.message);
  }
};

document.getElementById('formLogin').onsubmit = async (e) => {
  e.preventDefault();
  const fd = new FormData(e.target);
  try {
    const res = await api.login(Object.fromEntries(fd));
    state.setSession({ email: fd.get('email'), username: res.username });
    location.href = 'main.html';
  } catch (err) {
    alert(err.message);
  }
};
