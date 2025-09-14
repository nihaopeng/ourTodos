/**
 * 统一的 HTTP 请求工具
 * @param {string} url - 请求地址
 * @param {string} method - 请求方法 (GET, POST, PUT, DELETE...)
 * @param {Object} data - 请求体 JSON 数据
 * @param {Object} headers - 额外的请求头
 * @returns {Promise<Object>} - 返回 JSON 响应
 */
const baseUrl = 'http://141.11.238.11:5000'; // 替换为你的后端服务器地址

export async function httpRequest(url, method = 'GET', data = null, headers = {}) {
    const defaultHeaders = {
        'Content-Type': 'application/json',
        ...headers
    };

    const options = {
        method,
        headers: defaultHeaders
    };

    // 如果有请求体且不是 GET，就序列化为 JSON
    if (data && method.toUpperCase() !== 'GET') {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(`${baseUrl}${url}`, options);

        if (!response.ok) {
            throw new Error(`HTTP 错误！状态码: ${response.status}`);
        }

        // 解析 JSON 响应
        const result = await response.json();
        return result;
    } catch (error) {
        console.error('请求失败:', error);
        throw error;
    }
}

