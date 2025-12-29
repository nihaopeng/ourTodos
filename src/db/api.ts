import { supabase } from './supabase';
import type {
  Profile,
  Group,
  ScoringCriteria,
  Todo,
  PointsHistory,
  MonthlyRanking,
  LeaderboardEntry,
  Statistics,
  PointsTrend,
} from '@/types/types';

// ==================== Profile相关 ====================

export const getProfile = async (userId: string): Promise<Profile | null> => {
  const { data, error } = await supabase
    .from('profiles')
    .select('*')
    .eq('id', userId)
    .maybeSingle();

  if (error) throw error;
  return data;
};

export const updateProfile = async (
  userId: string,
  updates: Partial<Profile>
): Promise<Profile | null> => {
  const { data, error } = await supabase
    .from('profiles')
    .update(updates)
    .eq('id', userId)
    .select()
    .maybeSingle();

  if (error) throw error;
  return data;
};

export const getAllProfiles = async (): Promise<Profile[]> => {
  const { data, error } = await supabase
    .from('profiles')
    .select('*')
    .order('total_points', { ascending: false });

  if (error) throw error;
  return Array.isArray(data) ? data : [];
};

// ==================== Group相关 ====================

export const getGroups = async (userId: string): Promise<Group[]> => {
  const { data, error } = await supabase
    .from('groups')
    .select('*')
    .eq('user_id', userId)
    .order('order_index', { ascending: true });

  if (error) throw error;
  return Array.isArray(data) ? data : [];
};

export const createGroup = async (group: Omit<Group, 'id' | 'created_at'>): Promise<Group | null> => {
  const { data, error } = await supabase
    .from('groups')
    .insert(group)
    .select()
    .maybeSingle();

  if (error) throw error;
  return data;
};

export const updateGroup = async (
  groupId: string,
  updates: Partial<Group>
): Promise<Group | null> => {
  const { data, error } = await supabase
    .from('groups')
    .update(updates)
    .eq('id', groupId)
    .select()
    .maybeSingle();

  if (error) throw error;
  return data;
};

export const deleteGroup = async (groupId: string): Promise<void> => {
  const { error } = await supabase.from('groups').delete().eq('id', groupId);
  if (error) throw error;
};

// ==================== ScoringCriteria相关 ====================

export const getScoringCriteria = async (userId: string): Promise<ScoringCriteria[]> => {
  const { data, error } = await supabase
    .from('scoring_criteria')
    .select('*')
    .eq('user_id', userId)
    .order('created_at', { ascending: false });

  if (error) throw error;
  return Array.isArray(data) ? data : [];
};

export const getDefaultCriteria = async (userId: string): Promise<ScoringCriteria | null> => {
  const { data, error } = await supabase
    .from('scoring_criteria')
    .select('*')
    .eq('user_id', userId)
    .eq('is_default', true)
    .maybeSingle();

  if (error) throw error;
  return data;
};

export const createScoringCriteria = async (
  criteria: Omit<ScoringCriteria, 'id' | 'created_at'>
): Promise<ScoringCriteria | null> => {
  const { data, error } = await supabase
    .from('scoring_criteria')
    .insert(criteria)
    .select()
    .maybeSingle();

  if (error) throw error;
  return data;
};

export const updateScoringCriteria = async (
  criteriaId: string,
  updates: Partial<ScoringCriteria>
): Promise<ScoringCriteria | null> => {
  const { data, error } = await supabase
    .from('scoring_criteria')
    .update(updates)
    .eq('id', criteriaId)
    .select()
    .maybeSingle();

  if (error) throw error;
  return data;
};

export const deleteScoringCriteria = async (criteriaId: string): Promise<void> => {
  const { error } = await supabase.from('scoring_criteria').delete().eq('id', criteriaId);
  if (error) throw error;
};

// ==================== Todo相关 ====================

export const getTodos = async (
  userId: string,
  status?: 'pending' | 'completed' | 'deleted'
): Promise<Todo[]> => {
  let query = supabase
    .from('todos')
    .select(`
      *,
      group:groups(*),
      criteria:scoring_criteria(*)
    `)
    .eq('user_id', userId);

  if (status) {
    query = query.eq('status', status);
  }

  const { data, error } = await query.order('created_at', { ascending: false });

  if (error) throw error;
  return Array.isArray(data) ? data : [];
};

export const getTodosByGroup = async (
  userId: string,
  groupId: string | null
): Promise<Todo[]> => {
  let query = supabase
    .from('todos')
    .select(`
      *,
      group:groups(*),
      criteria:scoring_criteria(*)
    `)
    .eq('user_id', userId)
    .eq('status', 'pending');

  if (groupId === null) {
    query = query.is('group_id', null);
  } else {
    query = query.eq('group_id', groupId);
  }

  const { data, error } = await query.order('due_date', { ascending: true });

  if (error) throw error;
  return Array.isArray(data) ? data : [];
};

export const createTodo = async (todo: Omit<Todo, 'id' | 'created_at'>): Promise<Todo | null> => {
  const { data, error } = await supabase
    .from('todos')
    .insert(todo)
    .select(`
      *,
      group:groups(*),
      criteria:scoring_criteria(*)
    `)
    .maybeSingle();

  if (error) throw error;
  return data;
};

export const updateTodo = async (
  todoId: string,
  updates: Partial<Todo>
): Promise<Todo | null> => {
  const { data, error } = await supabase
    .from('todos')
    .update(updates)
    .eq('id', todoId)
    .select(`
      *,
      group:groups(*),
      criteria:scoring_criteria(*)
    `)
    .maybeSingle();

  if (error) throw error;
  return data;
};

export const deleteTodo = async (todoId: string): Promise<void> => {
  const { error } = await supabase.from('todos').delete().eq('id', todoId);
  if (error) throw error;
};

export const completeTodo = async (todoId: string): Promise<Todo | null> => {
  const { data, error } = await supabase
    .from('todos')
    .update({
      status: 'completed',
      completed_at: new Date().toISOString(),
    })
    .eq('id', todoId)
    .select(`
      *,
      group:groups(*),
      criteria:scoring_criteria(*)
    `)
    .maybeSingle();

  if (error) throw error;
  return data;
};

// ==================== PointsHistory相关 ====================

export const getPointsHistory = async (
  userId: string,
  limit?: number
): Promise<PointsHistory[]> => {
  let query = supabase
    .from('points_history')
    .select('*')
    .eq('user_id', userId)
    .order('created_at', { ascending: false });

  if (limit) {
    query = query.limit(limit);
  }

  const { data, error } = await query;

  if (error) throw error;
  return Array.isArray(data) ? data : [];
};

export const createPointsHistory = async (
  history: Omit<PointsHistory, 'id' | 'created_at'>
): Promise<PointsHistory | null> => {
  const { data, error } = await supabase
    .from('points_history')
    .insert(history)
    .select()
    .maybeSingle();

  if (error) throw error;
  return data;
};

export const getPointsTrend = async (
  userId: string,
  days: number = 30
): Promise<PointsTrend[]> => {
  const startDate = new Date();
  startDate.setDate(startDate.getDate() - days);

  const { data, error } = await supabase
    .from('points_history')
    .select('points, created_at')
    .eq('user_id', userId)
    .gte('created_at', startDate.toISOString())
    .order('created_at', { ascending: true });

  if (error) throw error;

  // 按日期聚合积分
  const trendMap = new Map<string, number>();
  let cumulative = 0;

  (data || []).forEach((item) => {
    const date = new Date(item.created_at).toISOString().split('T')[0];
    const current = trendMap.get(date) || 0;
    trendMap.set(date, current + item.points);
  });

  const trend: PointsTrend[] = [];
  trendMap.forEach((points, date) => {
    cumulative += points;
    trend.push({ date, points, cumulative_points: cumulative });
  });

  return trend;
};

// ==================== MonthlyRanking相关 ====================

export const getMonthlyRankings = async (yearMonth: string): Promise<MonthlyRanking[]> => {
  const { data, error } = await supabase
    .from('monthly_rankings')
    .select(`
      *,
      profile:profiles(*)
    `)
    .eq('year_month', yearMonth)
    .order('rank', { ascending: true })
    .limit(100);

  if (error) throw error;
  return Array.isArray(data) ? data : [];
};

export const createMonthlyRanking = async (
  ranking: Omit<MonthlyRanking, 'id' | 'awarded_at'>
): Promise<MonthlyRanking | null> => {
  const { data, error } = await supabase
    .from('monthly_rankings')
    .insert(ranking)
    .select()
    .maybeSingle();

  if (error) throw error;
  return data;
};

// ==================== 排行榜相关 ====================

export const getLeaderboard = async (
  type: 'all' | 'week' | 'month' = 'all',
  limit: number = 10
): Promise<LeaderboardEntry[]> => {
  let query = supabase
    .from('profiles')
    .select('id, username, total_points')
    .order('total_points', { ascending: false })
    .limit(limit);

  const { data, error } = await query;

  if (error) throw error;

  return (data || []).map((item, index) => ({
    user_id: item.id,
    username: item.username,
    total_points: item.total_points,
    rank: index + 1,
  }));
};

// ==================== 统计相关 ====================

export const getStatistics = async (userId: string): Promise<Statistics> => {
  const { data: todos, error } = await supabase
    .from('todos')
    .select('status, score')
    .eq('user_id', userId);

  if (error) throw error;

  const total_todos = todos?.length || 0;
  const completed_todos = todos?.filter((t) => t.status === 'completed').length || 0;
  const pending_todos = todos?.filter((t) => t.status === 'pending').length || 0;
  const total_score = todos?.reduce((sum, t) => sum + (t.score || 0), 0) || 0;
  const average_score = total_todos > 0 ? total_score / total_todos : 0;
  const completion_rate = total_todos > 0 ? (completed_todos / total_todos) * 100 : 0;

  const { data: profile } = await supabase
    .from('profiles')
    .select('total_points')
    .eq('id', userId)
    .maybeSingle();

  return {
    total_todos,
    completed_todos,
    pending_todos,
    total_points: profile?.total_points || 0,
    completion_rate,
    average_score,
  };
};
