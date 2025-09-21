import { api } from './core/api.js';
import { state } from './core/state.js';

document.getElementById('btnRegister').addEventListener('click', () => {
  location.href = 'register.html';
});

document.getElementById('formLogin').onsubmit = async (e) => {
  e.preventDefault();
  const fd = new FormData(e.target);
  try {
    const res = await api.login(Object.fromEntries(fd));
    state.setSession({ email: fd.get('email'), username: res.username, password: Object.fromEntries(fd).password});
    location.href = 'index.html';
  } catch (err) {
    alert(err.message);
  }
};

