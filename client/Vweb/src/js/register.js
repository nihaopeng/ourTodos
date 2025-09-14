// 发送验证码按钮
import { httpRequest } from '../../core/http.js';

document.getElementById("sendCodeBtn").addEventListener("click", async function () {
    const email = document.getElementById("email").value.trim();
    const result = await httpRequest('/send_code', 'POST', { email: email });
    if (!email) {
        alert("请先输入邮箱！");
        return;
    }
    alert(`验证码已发送到 ${email}（模拟）`);
    // 这里可以调用后端 API 发送验证码
});

// 注册表单提交
document.getElementById("registerForm").addEventListener("submit", function (e) {
    e.preventDefault();

    const email = document.getElementById("email").value.trim();
    const code = document.getElementById("code").value.trim();
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();

    if (!email || !code || !username || !password) {
        alert("请填写完整信息！");
        return;
    }

    alert(`注册成功！\n邮箱: ${email}\n用户名: ${username}`);
    // 这里可以调用后端 API 进行注册
});

// 返回登录
document.getElementById("backLoginBtn").addEventListener("click", function () {
    window.location.href = "login.html";
});
