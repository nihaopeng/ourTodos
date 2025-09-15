import { api } from './api.js';
import { state } from './state.js';

if (!state.isLogged()) {
  location.href = 'login.html';
}

document.getElementById('welcome').textContent = `你好，${state.session.username}`;

document.getElementById('btnLogout').onclick = async () => {
  await api.logout(state.session.email);
  state.clear();
  location.href = 'login.html';
};

async function loadScores() {
  const { data } = await api.getScores(state.session.email);
  document.getElementById('tableScores').innerHTML = data.map((r,i) =>
    `<tr><td>${i+1}</td><td>${r.username}</td><td>${r.email}</td><td>${r.score}</td></tr>`
  ).join('');
}
document.getElementById('btnRefreshScores').onclick = loadScores;
loadScores();

async function loadTodos() {
  const { todos } = await api.getTodos(state.session.email);
  console.log(todos);
  let rendered = [];
  todos.forEach(element => {
    rendered.push(
        {
            "content": element[0],
            "describe": element[1],
            "ddl": element[2],
            "score": element[3],
            "status": element[4]
        }
    );
  });
  
  document.getElementById('todosList').innerHTML = rendered.map(t =>
    `<div>${t.content} - ${t.describe} - ${t.ddl} - ${t.score} - ${t.status}</div>`
  ).join('');
}

document.getElementById('formAddTodo').onsubmit = async (e) => {
  e.preventDefault();
  const fd = new FormData(e.target);
  await api.addTodo({ email: state.session.email, ...Object.fromEntries(fd) });
  e.target.reset();
  loadTodos();
};
loadTodos();
