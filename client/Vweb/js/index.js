import { state } from './core/state.js';
import { api, hideLoading,showLoading, testSession } from './core/api.js';
import * as todof from './core/todo.js'

const form = document.getElementById('formAddTodo');
const todosList = document.getElementById('todosList');
const btnRank = document.getElementById('btnRank');
const btnSettings = document.getElementById('btnSettings');

let todos = [];

document.addEventListener('DOMContentLoaded', async () => {
    if (!state.session || !state.session.email) {
        window.location.href = 'login.html';
        return;
    }
    const res = await testSession({"email":state.session.email});
    if(!res){
        window.location.href = 'login.html';
        return;
    }
    showLoading();
    // await new Promise(resolve => setTimeout(resolve, 1000));
    todos = await todof.getTodos() || [];
    // console.log(todos);
    renderTodos();
    hideLoading();
});

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = form.todoName.value.trim();
    const description = form.todoDescription.value.trim();
    const ddl = form.ddl.value;

    if (!name || !description || !ddl) return;

    let todo = {
        todoName: name,
        todoDescription: description,
        ddl,
        steps: [],
        status: "True",
    };
    showLoading();
    const res =await todof.addTodo(todo);
    hideLoading();
    if (res.code !== 200) {
        alert('添加失败: ' + res.msg);
        return;
    }else{
        todo.todoUid = res.todoUid;
        todo.score = res.score;
        todo.expanded = true;
    }
    todos.push(todo);
    form.reset();
    renderTodos();
});

function renderTodos() {
  todosList.innerHTML = '';

  todos
    .slice()
    .sort((a, b) => a.status === "False" ? 1 : -1)
    .forEach(todo => {
      const item = document.createElement('div');
      item.className = 'todo-item';

      const isExpired = new Date(todo.ddl) < new Date();

      item.innerHTML = `
        <div class="todo-header">
          <div>
            <strong style="color: ${isExpired ? 'red' : '#ecf0f1'}">${todo.todoName}</strong> - 
            <em style="color: ${isExpired ? 'red' : '#ecf0f1'}">${todo.ddl}</em>
          </div>
          <div class="todo-actions">
            <button onclick="toggleExpand(${todo.todoUid})">${todo.expanded ? '展开' : '收起'}</button>
            <button onclick="markComplete(${todo.todoUid})" ${todo.status == "False" ? 'disabled' : ''}>${todo.status == "False" ? '已完成' : '完成'}</button>
            <button onclick="deleteTodo(${todo.todoUid})">删除</button>
          </div>
        </div>
        ${todo.expanded ? '' : `
          <div class="todo-details">
            <p>分数:${todo.score} - ${todo.todoDescription}</p>
            <form onsubmit="addStep(event, ${todo.todoUid})">
              <input name="step" placeholder="添加步骤" required>
              <button type="submit">添加步骤</button>
            </form>
            <ul>
              ${todo.steps.map((step, index) => `
                <li>
                  <span style="text-decoration:${step.status == "False" ? 'line-through' : 'none'}">${step.stepName}</span>
                  <button onclick="toggleStep(${todo.todoUid}, ${index})">${step.status == "False" ? '取消完成' : '完成'}</button>
                  <button onclick="deleteStep(${todo.todoUid}, ${index})">删除</button>
                </li>
              `).join('')}
            </ul>
          </div>
        `}
      `;

      todosList.appendChild(item);
    });
}


window.toggleExpand = function (id) {
    const todo = todos.find(t => t.todoUid === id);
    todo.expanded = !todo.expanded;
    renderTodos();
};

window.markComplete = async function (id) {
    const result = window.confirm("是否确认完成该待办？");
    if (!result) {
        return;
    }
    const todo = todos.find(t => t.todoUid === id);
    const res = await todof.completeTodo(id);
    if (res.code !== 200) {
        alert('操作失败: ' + res.msg);
        return;
    }
    todo.status = todo.status=="False" ? "True" : "False";
    renderTodos();
};

window.deleteTodo = async function (id) {
    const res = await todof.delTodo(id);
    if (res.code !== 200) {
        alert('删除失败: ' + res.msg);
        return;
    }
    todos = todos.filter(t => t.todoUid !== id);
    renderTodos();
};

window.addStep = async function (e, id) {
    e.preventDefault();
    const input = e.target.step;
    const text = input.value.trim();
    if (!text) return;
    const res = await todof.addStep(id, text);
    if (res.code !== 200) {
        alert('添加步骤失败: ' + res.msg);
        return;
    }

    const todo = todos.find(t => t.todoUid === id);
    todo.steps.push({ stepName:text, status: "True" });
    input.value = '';
    renderTodos();
};

window.toggleStep = async function (todoId, stepIndex) {
    const todo = todos.find(t => t.todoUid === todoId);
    const step = todo.steps[stepIndex];
    let newStatus = step.status == "False" ? "True" : "False";
    const res = await todof.changeStep(step.stepUid, newStatus);
    if (res.code !== 200) {
        alert('操作失败: ' + res.msg);
        return;
    }
    todo.steps[stepIndex].status = todo.steps[stepIndex].status == "False" ? "True" : "False";
    renderTodos();
};

window.deleteStep = async function (todoId, stepIndex) {
    const step = todos.find(t => t.todoUid === todoId).steps[stepIndex];
    console.log(todos);
    console.log(step);
    const res = await todof.delStep(step.stepUid);
    if (res.code !== 200) {
        alert('删除步骤失败: ' + res.msg);
        return;
    }
    const todo = todos.find(t => t.todoUid === todoId);
    todo.steps.splice(stepIndex, 1);
    renderTodos();
};

btnRank.addEventListener('click', () => {
    window.location.href = 'rank.html';
});

btnLogout.addEventListener('click', () => {
    api.logout({ 'email': state.session.email });
    state.clear();
    window.location.href = 'login.html';
});

btnSettings.addEventListener('click', () => {
    window.location.href = 'settings.html';
});