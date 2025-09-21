import { api } from './api.js';
import { state } from './state.js';

export async function getRankings() {
    const res = await api.getScores({ email: state.session.email });
    if (res.code !== 200) {
        throw new Error('获取排行榜失败: ' + res.msg);
    }
    const rankings = res.data; // 假设返回的数据结构是 { code: 200, scores: [...] }
    // 对数据进行格式化
    return rankings;
}