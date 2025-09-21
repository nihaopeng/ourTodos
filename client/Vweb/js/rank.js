import { state } from './core/state.js';
import { getRankings } from './core/rank.js';
import { api,hideLoading, showLoading } from './core/api.js';

const tableBody = document.getElementById('tableScores');
const btnRefresh = document.getElementById('btnRefreshScores');
const btnIndex = document.getElementById('btnIndex');
const btnLogout = document.getElementById('btnLogout');

// 模拟用户数据
let users = [];

document.addEventListener('DOMContentLoaded', async () => {
    loadRankings();
});

function rankUsersByScore(users) {
    return users.sort((a, b) => b.score - a.score);
}

async function loadRankings() {
    if (!state.session || !state.session.email) {
        window.location.href = 'login.html';
        return;
    }
    showLoading();
    //休眠1秒，模拟加载时间
    // await new Promise(resolve => setTimeout(resolve, 1000));
    users = await getRankings();
    hideLoading();
    // 假设返回的数据结构是 { code: 200, data: [...] }
    // users.splice(0, users.length, ...res.data);
    rankUsersByScore(users);
    renderScores();
}

// 渲染排行榜
function renderScores() {
  tableBody.innerHTML = '';
  users
    .sort((a, b) => b.score - a.score)
    .forEach((user, index) => {
      const row = document.createElement('tr');

      // 如果是当前用户，添加绿色字体样式
      if (user.email === state.session.email) {
        row.style.color = 'limegreen'; // 或者 '#2ecc71' 更柔和
        row.style.fontWeight = 'bold';
      }

      row.innerHTML = `
        <td>${index + 1}</td>
        <td>${user.username}</td>
        <td>${user.email}</td>
        <td>${user.score}</td>
      `;
      tableBody.appendChild(row);
    });
}


// 页面加载时渲染
window.addEventListener('DOMContentLoaded', renderScores);

// 点击刷新按钮重新渲染（可用于更新数据）
btnRefresh.addEventListener('click', () => {
    // alert("刷新排行榜");
  loadRankings();
});

btnIndex.addEventListener('click', () => {
  window.location.href = 'index.html';
});

btnLogout.addEventListener('click', () => {
    // 清除登录状态（这里假设使用localStorage存储登录状态）
    // alert("email:"+state.session.email);
    const res = api.logout({'email':state.session.email});
    state.clear();
    window.location.href = 'login.html';
});