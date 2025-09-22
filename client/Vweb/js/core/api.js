// export const API_BASE = 'http://127.0.0.1:5000';
export const API_BASE = 'http://141.11.238.11:5000';

async function request(path, data) {
  const res = await fetch(API_BASE + path, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data),
    credentials: 'include'
  });
  const json = await res.json();
//   if (json.code !== 200) throw new Error(json.msg);
  return json;
}

export const api = {
  sendCode: (p) => request('/send_verification_code', p),
  register: (p) => request('/regist', p),
  login: (p) => request('/login', p),
  logout: (p) => request('/logout', p),
  updateUsernameAndPassword: (p) => request('/update_username_and_password', p),
  setProfile: (p) => request('/set_profile', p),
  getProfile: (p) => request('/get_profile', p),
  getUserScore: (p) => request('/get_user_score', p),
  getScores: (p) => request('/get_scores', p),
  getTodos: (p) => request('/get_todos', p),
  addTodo: (p) => request('/add_todo', p),
  getSteps: (p) => request('/get_steps', p),
  addStep: (p) => request('/step_add', p),
  delTodo: (p) => request('/del_todo', p),
  completeTodo: (p) => request('/todo_complete', p),
  changeStep: (p) => request('/step_change', p),
  delStep: (p) => request('/step_del', p),
};

export async function testSession(p) {
    const res = await api.getProfile(p);
    if(res.code!=200){
        return false;
    }else{
        return true;
    }
}

export function showLoading() {
  document.getElementById('loadingOverlay').style.display = 'flex';
}

export function hideLoading() {
  document.getElementById('loadingOverlay').style.display = 'none';
}
