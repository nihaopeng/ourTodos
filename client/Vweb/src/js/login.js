import httpRequest from '../../core/http.js';

document.getElementById("registerBtn").addEventListener("click", function () {
    // 跳转到注册页面
    window.location.href = "page/register.html";
});

document.getElementById("loginForm").addEventListener("submit", function (e) {
    e.preventDefault(); // 阻止表单默认提交
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();
    
    if (email && password) {
        alert(`登录成功！\n邮箱: ${email}`);
        // 这里可以添加实际的登录逻辑，比如调用后端API
    } else {
        alert("请输入邮箱和密码！");
    }
});
