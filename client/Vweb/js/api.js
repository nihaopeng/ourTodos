export const API_BASE = 'http://127.0.0.1:5000';

async function request(path, data) {
  const res = await fetch(API_BASE + path, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data),
    credentials: 'include'
  });
  const json = await res.json();
  if (json.code !== 200) throw new Error(json.msg);
  return json;
}

export const api = {
  sendCode: (email) => request('/send_verification_code', {email}),
  register: (p) => request('/regist', p),
  login: (p) => request('/login', p),
  logout: (email) => request('/logout', {email}),
  getScores: (email) => request('/get_scores', {email}),
  getTodos: (email) => request('/get_todos', {email}),
  addTodo: (p) => request('/add_todo', p)
};
