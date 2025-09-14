import { httpRequest } from '../../core/http.js';

document.addEventListener("DOMContentLoaded", async () => {
  const userInfo = JSON.parse(localStorage.getItem("userInfo"));
  if (!userInfo || !userInfo.email) {
    alert("未登录，请先登录");
    window.location.href = "login.html";
    return;
  }

  try {
    // 获取用户信息
    // const user = await httpRequest(`/user?email=${userInfo.email}`);
    document.getElementById("email").textContent = userInfo.email;
    document.getElementById("username").textContent = userInfo.username;
    const res = await httpRequest('/get_user_score', 'POST', { email: userInfo.email });
    document.getElementById("score").textContent = res.score;
    res = await httpRequest('/get_profile', 'POST', { email: userInfo.email });
    document.getElementById("profile").textContent = res.profile;

    // 获取 todos 列表
    const todos = await httpRequest('/get_todos', 'POST', { email: userInfo.email });
    console.log("获取 todos:", todos);
    renderTodos(todos);
  } catch (err) {
    console.error("加载数据失败:", err);
    alert("加载失败，请稍后再试");
  }
});

// ✅ 渲染 todos（传入参数）
function renderTodos(todos) {
  const todoList = document.getElementById("todoList");
  todoList.innerHTML = "";

  todos.forEach(todo => {
    const li = document.createElement("li");
    li.className = "todo-item";

    const todoDetailId = `todo-detail-${todo.todoid}`;
    const stepsId = `steps-${todo.todoid}`;

    li.innerHTML = `
      <div class="todo-header" onclick="toggleTodo('${todoDetailId}')">
        <h3>${todo.content}</h3>
      </div>

      <div class="todo-detail" id="${todoDetailId}" style="display: none;">
        <p>${todo.describe}</p>
        <p>截止日期: ${todo.ddl}</p>
        <p>积分: ${todo.score} | 状态: ${todo.status}</p>
        <button onclick="completeTodo(${todo.todoid})">完成</button>
        <button onclick="deleteTodo(${todo.todoid})">删除</button>
        <button onclick="toggleSteps('${stepsId}')">展开/折叠步骤</button>

        <div class="step-list" id="${stepsId}" style="display: none;">
          <h4>步骤</h4>
          <ul>
            ${todo.steps.map(step => `
              <li class="step-item">
                ${step.stepName} - ${step.status}
                <button onclick="completeStep(${step.id})">完成</button>
                <button onclick="deleteStep(${step.id})">删除</button>
              </li>
            `).join("")}
          </ul>
          <input type="text" placeholder="新步骤名称" id="stepInput-${todo.todoid}">
          <button onclick="addStep(${todo.todoid})">添加步骤</button>
        </div>
      </div>
    `;

    todoList.appendChild(li);
  });
}

// ✅ 折叠函数挂到全局
function toggleTodo(id) {
  const el = document.getElementById(id);
  if (el) {
    el.style.display = el.style.display === "none" ? "block" : "none";
  }
}
window.toggleTodo = toggleTodo;

function toggleSteps(id) {
  const el = document.getElementById(id);
  if (el) {
    el.style.display = el.style.display === "none" ? "block" : "none";
  }
}
window.toggleSteps = toggleSteps;

// ✅ 添加 todo（你可以改成发请求）
document.getElementById("todoForm").addEventListener("submit", async function (e) {
  e.preventDefault();
  const content = document.getElementById("content").value;
  const describe = document.getElementById("describe").value;
  const ddl = document.getElementById("ddl").value;

  const newTodo = {
    content,
    describe,
    ddl,
    email: JSON.parse(localStorage.getItem("userInfo")).email
  };

  try {
    const result = await httpRequest('/todos', 'POST', newTodo);
    console.log("添加成功:", result);
    const updatedTodos = await httpRequest(`/todos?email=${newTodo.email}`);
    renderTodos(updatedTodos);
  } catch (err) {
    console.error("添加失败:", err);
  }
});

// ✅ 其他操作函数（你自己实现接口）
function completeTodo(id) {
  console.log("完成 todo:", id);
}
window.completeTodo = completeTodo;

function deleteTodo(id) {
  console.log("删除 todo:", id);
}
window.deleteTodo = deleteTodo;

function addStep(todoid) {
  const input = document.getElementById(`stepInput-${todoid}`);
  const stepName = input.value.trim();
  if (!stepName) return;
  console.log("添加步骤:", stepName, "到 todo:", todoid);
}
window.addStep = addStep;

function completeStep(id) {
  console.log("完成步骤:", id);
}
window.completeStep = completeStep;

function deleteStep(id) {
  console.log("删除步骤:", id);
}
window.deleteStep = deleteStep;
