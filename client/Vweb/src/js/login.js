import { httpRequest } from '../../core/http.js';

document.getElementById("registerBtn").addEventListener("click", function () {
    // 跳转到注册页面
    console.log("跳转到注册页面");
    window.location.href = "register.html";
});

document.getElementById("loginForm").addEventListener("submit", async function (e) {
    e.preventDefault(); // 阻止表单默认提交
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();

    const data = { 
        "email":email, "password":password 
    };
    const result = await httpRequest('/login', 'POST', data);
    console.log(typeof(result),result);
    if (result.code === 200) {
        alert("登录成功！");
        // 登录成功后跳转到待办事项页面
        localStorage.setItem("userInfo", JSON.stringify({"email":email,"username":result.username}));
        window.location.href = "todoList.html";
    } else {
        alert("登录失败：" + result.message);
    }
});
