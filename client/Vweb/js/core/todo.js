import { api } from './api.js';
import { state } from './state.js';

export async function getSteps(todo_id) {
    const res = await api.getSteps({ email: state.session.email, todo_id });
    let steps = [];
    if (res.code === 200) {
        steps = res.steps.map(s => ({
            stepUid: s[1],
            stepName: s[2],
            status: s[3]
        }));
    }
    return steps;
}

export async function getTodos() {
    const resTodos = await api.getTodos({ email: state.session.email });
    if (resTodos.code!=200) {
        return []
    }
    let formatTodos = []
    for (let t of resTodos.todos) {
        const resSteps = await getSteps(t[0]);
        const steps = resSteps || [];
        let formatT = {
            todoUid: t[0],
            todoName: t[1],
            todoDescription: t[2],
            ddl: t[3],
            score: t[4],
            status: t[5],
            steps: steps,
            expanded: true// 这个字段前端自己加的，不存在数据库里
        }
        formatTodos.push(formatT);
    };
    return formatTodos;
}

export async function addTodo(todo) {
    const res = await api.addTodo({
        email: state.session.email,
        todoName: todo.todoName,
        todoDescription: todo.todoDescription,
        ddl: todo.ddl,
        score: todo.score || 0,
        status: todo.status || false
    });
    return res;
}

export async function addStep(todo_id, stepName) {
    const res = await api.addStep({
        email: state.session.email,
        todo_id,
        stepName
    });
    return res;
}

export async function delTodo(todo_id) {
    const res = await api.delTodo({
        email: state.session.email,
        todo_id
    });
    return res;
}

export async function completeTodo(todo_id) {
    const res = await api.completeTodo({
        email: state.session.email,
        todo_id
    });
    return res;
}

export async function changeStep(stepUid, status) {
    const res = await api.changeStep({
        email: state.session.email,
        stepUid,
        status
    });
    return res;
}

export async function delStep(stepUid) {
    // alert("stepUid:"+stepUid);
    const res = await api.delStep({
        email: state.session.email,
        stepUid
    });
    return res;
}// window.getTodos = getTodos;