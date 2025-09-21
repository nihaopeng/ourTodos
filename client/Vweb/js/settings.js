import { api,showLoading,hideLoading } from './core/api.js';
import { state } from './core/state.js';

const btnIndex = document.getElementById("btnIndex");

document.addEventListener('DOMContentLoaded', async () => {
    if (!state.session || !state.session.email) {
        window.location.href = 'login.html';
        return;
    }
    const form = document.getElementById("formSettings");
    form.username.value = state.session.username;
    form.password.value = state.session.password;
    const res = await api.getProfile({"email":state.session.email});
    form.profile.value = res.profile;
});

document.getElementById('formSettings').onsubmit = async (e) => {
  e.preventDefault();
  const fd = new FormData(e.target);
  const jsonData = Object.fromEntries(fd);
  jsonData.email = state.session.email;
  try {
    showLoading();
    await api.updateUsernameAndPassword(jsonData)
    await api.setProfile(jsonData);
    hideLoading();
    state.setSession({"username":jsonData.username,"password":jsonData.password,"email":jsonData.email})
    alert('更新成功');
  } catch (err) {
    alert(err.message);
  }
};

btnIndex.addEventListener("click",() => {
    window.location.href = 'index.html';
})