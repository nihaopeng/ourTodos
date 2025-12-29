// 用户角色
export type UserRole = 'user' | 'admin';

// 待办状态
export type TodoStatus = 'pending' | 'completed' | 'deleted';

// 优先级
export type PriorityLevel = 'low' | 'medium' | 'high' | 'urgent';

// 积分来源类型
export type PointsSourceType = 'todo_completed' | 'todo_early' | 'todo_late' | 'todo_deleted';

// 用户Profile
export interface Profile {
  id: string;
  email: string | null;
  username: string;
  total_points: number;
  role: UserRole;
  created_at: string;
}

// 分组
export interface Group {
  id: string;
  user_id: string;
  name: string;
  color: string;
  order_index: number;
  created_at: string;
}

// 评分标准
export interface ScoringCriteria {
  id: string;
  user_id: string;
  name: string;
  criteria_json: {
    importance?: number;
    urgency?: number;
    complexity?: number;
    impact?: number;
    [key: string]: number | undefined;
  };
  is_default: boolean;
  created_at: string;
}

// 待办事项
export interface Todo {
  id: string;
  user_id: string;
  title: string;
  description: string | null;
  due_date: string | null;
  score: number;
  status: TodoStatus;
  group_id: string | null;
  priority: PriorityLevel;
  criteria_id: string | null;
  created_at: string;
  completed_at: string | null;
  // 关联数据
  group?: Group;
  criteria?: ScoringCriteria;
}

// 积分历史
export interface PointsHistory {
  id: string;
  user_id: string;
  points: number;
  source_type: PointsSourceType;
  source_id: string | null;
  description: string | null;
  created_at: string;
}

// 月排行榜
export interface MonthlyRanking {
  id: string;
  year_month: string;
  user_id: string;
  rank: number;
  points: number;
  awarded_at: string;
  // 关联数据
  profile?: Profile;
}

// 排行榜条目（用于显示）
export interface LeaderboardEntry {
  user_id: string;
  username: string;
  total_points: number;
  rank: number;
  trend?: 'up' | 'down' | 'same';
}

// AI评分请求
export interface ScoreRequest {
  title: string;
  description: string;
  criteria: ScoringCriteria['criteria_json'];
}

// AI评分响应
export interface ScoreResponse {
  score: number;
  reasoning: string;
  breakdown: {
    [key: string]: number;
  };
}

// 统计数据
export interface Statistics {
  total_todos: number;
  completed_todos: number;
  pending_todos: number;
  total_points: number;
  completion_rate: number;
  average_score: number;
}

// 积分趋势数据
export interface PointsTrend {
  date: string;
  points: number;
  cumulative_points: number;
}
