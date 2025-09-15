import { state } from './state.js';
import { api } from './api.js';

// Helpers
function setText(el, text) { if (el) el.textContent = text ?? ''; }
function setHtml(el, html) { if (el) el.innerHTML = html ?? ''; }
function show(el) { el?.classList.remove('hidden'); }
function hide(el) { el?.classList.add('hidden'); }
function fmtDate(s) { return s; } // backend date is already yyyy-mm-dd

// Elements
const el = {
  welcome: document.getElementById('welcome'),
  btnShowLogin: document.getElementById('btnShowLogin'),
  btnShowRegister: document.getElementById('btnShowRegister'),
  btnLogout: document.getElementById('btnLogout'),

  formSendCode: document.getElementById('formSendCode'),
  logSendCode: document.getElementById('logSendCode'),

  formRegister: document.getElementById('formRegister'),
  logRegister: document.getElementById('logRegister'),

  formLogin: document.getElementById('formLogin'),
  logLogin: document.getElementById('logLogin'),

  formUpdateUser: document.getElementById('formUpdateUser'),
  logUpdateUser: document.getElementById('logUpdateUser'),

  formSetProfile: document.getElementById('formSetProfile'),
  btnGetProfile: document.getElementById('btnGetProfile'),
  currentProfile: document.getElementById('currentProfile'),
  logProfile: document.getElementById('logProfile'),

  btnGetMyScore: document.getElementById('btnGetMyScore'),
  myScore: document.getElementById('myScore'),
  logMyScore: document.getElementById('logMyScore'),

  btnRefreshScores: document.getElementById('btnRefreshScores'),
  tableScores: document.getElementById('tableScores').querySelector('tbody'),
  logScores: document.getElementById('logScores'),

  formAddTodo: document.getElementById('formAddTodo'),
  logAddTodo: document.getElementById('logAddTodo'),
  btnRefreshTodos: document.getElementById('btnRefreshTodos'),
  todosList: document.getElementById('todosList'),
  logTodos: document.getElementById('logTodos')
};

// Session UI
export function refreshSessionUI() {
  if (state.isLogged()) {
    setText(el.welcome, `你好，${state.session.username ?? ''}（${state.session.email}）`);
    hide(el.btnShowLogin);
    hide(el.btnShowRegister);
    show(el.btnLogout);
  } else {
    setText(el.welcome, '');
    show(el.btnShowLogin);
    show(el.btnShowRegister);
    hide(el.btnLogout);
    setText(el.myScore, '-');
    setHtml(el.tableScores, '');
    setHtml(el.todosList, '');
  }
}

// Logs
function log(elm, msg, isError=false) {
  if (!elm) return;
  elm.textContent = `[${new Date().toLocaleTimeString()}] ${msg}`;
  elm.style.color = isError ? '#ff9a9a' : '';
}

// Scores table
export async function loadScores() {
  if (!state.isLogged()) return;
  try {
    const { data } = await api.getScores(state.session.email);
    el.tableScores.innerHTML = data.map((row, idx) => `
      <tr>
        <td>${idx + 1}</td>
        <td>${row.username ?? '-'}</td>
        <td>${row.email}</td>
        <td>${row.score}</td>
      </tr>
    `).join('');
    log(el.logScores, '排行榜已更新');
  } catch (e) {
    log(el.logScores, `加载排行榜失败：${e.message}`, true);
  }
}

// My score
export async function loadMyScore() {
  if (!state.isLogged()) return;
  try {
    const { score } = await api.getMyScore(state.session.email);
    setText(el.myScore, String(score));
    log(el.logMyScore, '积分已刷新');
  } catch (e) {
    log(el.logMyScore, `获取积分失败：${e.message}`, true);
  }
}

// Profile
async function fetchProfile() {
  if (!state.isLogged()) return;
  try {
    const { profile } = await api.getProfile(state.session.email);
    setText(el.currentProfile, profile ?? '');
    log(el.logProfile, '获取简介成功');
  } catch (e) {
    log(el.logProfile, `获取简介失败：${e.message}`, true);
  }
}

// Todos rendering
function renderTodo(todo) {
  const statusTrue = String(todo.status).toLowerCase() === 'true';
  const header = `
    <div class="todo" data-id="${todo.todoid}">
      <div class="meta">
        <span><strong>标题：</strong>${todo.content}</span>
        <span><strong>描述：</strong>${todo.describe}</span>
        <span><strong>截止：</strong>${fmtDate(todo.ddl)}</span>
        <span><strong>积分：</strong>${todo.score}</span>
        <span class="status ${statusTrue ? 'status-true' : 'status-false'}">
          ${statusTrue ? '已完成' : '未完成'}
        </span>
      </div>
      <div class="actions">
        <button class="secondary btn-show-steps">查看步骤</button>
        <button class="secondary btn-add-step">新增步骤</button>
        <button class="secondary btn-complete">标记完成</button>
        <button class="danger btn-delete">删除</button>
      </div>
      <div class="steps hidden">
        <div class="steps-body"></div>
      </div>
    </div>
  `;
  const div = document.createElement('div');
  div.innerHTML = header;
  return div.firstElementChild;
}

function renderStep(step) {
  const done = String(step.status).toLowerCase() === 'true';
  const el = document.createElement('div');
  el.className = 'step';
  el.dataset.stepUid = step.stepUid;
  el.innerHTML = `
    <div class="name">
      <span class="status ${done ? 'status-true' : 'status-false'}">${done ? '完成' : '未完成'}</span>
      <span>${step.stepName}</span>
    </div>
    <div class="actions">
      <button class="secondary btn-toggle-step">${done ? '标记未完成' : '标记完成'}</button>
      <button class="danger btn-del-step">删除</button>
    </div>
  `;
  return el;
}

async function loadSteps(todoEl, todoId) {
  try {
    const { steps } = await api.getSteps({ email: state.session.email, todo_id: todoId });
    const body = todoEl.querySelector('.steps-body');
    body.innerHTML = '';
    steps.forEach(s => body.appendChild(renderStep(s)));
  } catch (e) {
    log(el.logTodos, `加载步骤失败：${e.message}`, true);
  }
}

// Todos list
export async function loadTodos() {
  if (!state.isLogged()) return;
  try {
    const { todos } = await api.getTodos(state.session.email);
    el.todosList.innerHTML = '';
    todos.forEach(t => el.todosList.appendChild(renderTodo(t)));
    log(el.logTodos, '待办列表已刷新');
  } catch (e) {
    log(el.logTodos, `加载待办失败：${e.message}`, true);
  }
}

// Event wiring
export function setupEvents() {
  // Header buttons
  el.btnLogout.addEventListener('click', async () => {
    if (!state.isLogged()) return;
    try {
      await api.logout(state.session.email);
      state.clearSession();
      refreshSessionUI();
      log(el.logLogin, '已退出登录');
    } catch (e) {
      log(el.logLogin, `退出失败：${e.message}`, true);
    }
  });

  // Send code
  el.formSendCode.addEventListener('submit', async (ev) => {
    ev.preventDefault();
    const email = new FormData(ev.target).get('email').trim();
    try {
      await api.sendCode(email);
      log(el.logSendCode, '验证码发送成功');
    } catch (e) {
      log(el.logSendCode, `发送失败：${e.message}`, true);
    }
  });

  // Register
  el.formRegister.addEventListener('submit', async (ev) => {
    ev.preventDefault();
    const fd = new FormData(ev.target);
    const payload = {
      username: fd.get('username').trim(),
      email: fd.get('email').trim(),
      password: fd.get('password'),
      code: fd.get('code').trim()
    };
    try {
      await api.register(payload);
      log(el.logRegister, '注册成功，请前往登录');
    } catch (e) {
      log(el.logRegister, `注册失败：${e.message}`, true);
    }
  });

  // Login
  el.formLogin.addEventListener('submit', async (ev) => {
    ev.preventDefault();
    const fd = new FormData(ev.target);
    const email = fd.get('email').trim();
    const password = fd.get('password');
    try {
      const res = await api.login({ email, password });
      state.setSession({ email, username: res.username || '' });
      refreshSessionUI();
      log(el.logLogin, '登录成功');
      // Initial loads
      await Promise.all([loadMyScore(), loadScores(), loadTodos(), fetchProfile()]);
    } catch (e) {
      log(el.logLogin, `登录失败：${e.message}`, true);
    }
  });

  // Update user
  el.formUpdateUser.addEventListener('submit', async (ev) => {
    ev.preventDefault();
    if (!state.isLogged()) return;
    const fd = new FormData(ev.target);
    const username = fd.get('username').trim();
    const password = fd.get('password');
    try {
      await api.updateUser({ email: state.session.email, username, password });
      state.setSession({ username });
      refreshSessionUI();
      log(el.logUpdateUser, '更新成功');
    } catch (e) {
      log(el.logUpdateUser, `更新失败：${e.message}`, true);
    }
  });

  // Profile
  el.formSetProfile.addEventListener('submit', async (ev) => {
    ev.preventDefault();
    if (!state.isLogged()) return;
    const profile = new FormData(ev.target).get('profile').trim();
    try {
      await api.setProfile({ email: state.session.email, profile });
      log(el.logProfile, '简介已更新');
      setText(el.currentProfile, profile);
    } catch (e) {
      log(el.logProfile, `更新失败：${e.message}`, true);
    }
  });

  el.btnGetProfile.addEventListener('click', fetchProfile);

  // My score
  el.btnGetMyScore.addEventListener('click', loadMyScore);

  // Scores
  el.btnRefreshScores.addEventListener('click', loadScores);

  // Add todo
  el.formAddTodo.addEventListener('submit', async (ev) => {
    ev.preventDefault();
    if (!state.isLogged()) return;
    const fd = new FormData(ev.target);
    const todoName = fd.get('todoName').trim();
    const todoDescription = fd.get('todoDescription').trim();
    const ddl = fd.get('ddl');
    try {
      await api.addTodo({ email: state.session.email, todoName, todoDescription, ddl });
      log(el.logAddTodo, '新增待办成功');
      ev.target.reset();
      await loadTodos();
    } catch (e) {
      log(el.logAddTodo, `新增失败：${e.message}`, true);
    }
  });

  // Refresh todos
  el.btnRefreshTodos.addEventListener('click', loadTodos);

  // Todo actions (event delegation)
  el.todosList.addEventListener('click', async (ev) => {
    const btn = ev.target.closest('button');
    if (!btn) return;
    const todoEl = ev.target.closest('.todo');
    if (!todoEl) return;
    const todoId = Number(todoEl.dataset.id);

    // Show steps
    if (btn.classList.contains('btn-show-steps')) {
      const stepsBox = todoEl.querySelector('.steps');
      if (stepsBox.classList.contains('hidden')) {
        await loadSteps(todoEl, todoId);
        stepsBox.classList.remove('hidden');
      } else {
        stepsBox.classList.add('hidden');
      }
      return;
    }

    // Add step
    if (btn.classList.contains('btn-add-step')) {
      const name = prompt('步骤名称：');
      if (!name) return;
      try {
        await api.addStep({ email: state.session.email, todo_id: todoId, stepName: name.trim() });
        await loadSteps(todoEl, todoId);
        log(el.logTodos, '新增步骤成功');
      } catch (e) {
        log(el.logTodos, `新增步骤失败：${e.message}`, true);
      }
      return;
    }

    // Complete todo
    if (btn.classList.contains('btn-complete')) {
      try {
        await api.completeTodo({ email: state.session.email, todo_id: todoId });
        await loadTodos();
        log(el.logTodos, '已标记完成');
      } catch (e) {
        log(el.logTodos, `标记完成失败：${e.message}`, true);
      }
      return;
    }

    // Delete todo
    if (btn.classList.contains('btn-delete')) {
      if (!confirm('确定删除该待办吗？')) return;
      try {
        await api.delTodo({ email: state.session.email, todo_id: todoId });
        await loadTodos();
        log(el.logTodos, '已删除待办');
      } catch (e) {
        log(el.logTodos, `删除失败：${e.message}`, true);
      }
      return;
    }

    // Step operations
    if (btn.classList.contains('btn-toggle-step') || btn.classList.contains('btn-del-step')) {
      const stepEl = btn.closest('.step');
      const stepUid = stepEl.dataset.stepUid;

      if (btn.classList.contains('btn-toggle-step')) {
        const isDone = stepEl.querySelector('.status').classList.contains('status-true');
        const next = isDone ? 'False' : 'True';
        try {
          await api.changeStep({ email: state.session.email, stepUid, status: next });
          await loadSteps(todoEl, todoId);
          log(el.logTodos, '步骤状态已更新');
        } catch (e) {
          log(el.logTodos, `更新步骤失败：${e.message}`, true);
        }
      }

      if (btn.classList.contains('btn-del-step')) {
        if (!confirm('确定删除该步骤吗？')) return;
        try {
          await api.delStep({ email: state.session.email, stepUid });
          await loadSteps(todoEl, todoId);
          log(el.logTodos, '步骤已删除');
        } catch (e) {
          log(el.logTodos, `删除步骤失败：${e.message}`, true);
        }
      }
    }
  });
}
