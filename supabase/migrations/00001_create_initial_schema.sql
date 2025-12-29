-- 创建用户角色枚举
CREATE TYPE public.user_role AS ENUM ('user', 'admin');

-- 创建待办状态枚举
CREATE TYPE public.todo_status AS ENUM ('pending', 'completed', 'deleted');

-- 创建优先级枚举
CREATE TYPE public.priority_level AS ENUM ('low', 'medium', 'high', 'urgent');

-- 创建积分来源类型枚举
CREATE TYPE public.points_source_type AS ENUM ('todo_completed', 'todo_early', 'todo_late', 'todo_deleted');

-- 创建profiles表
CREATE TABLE public.profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email TEXT,
  username TEXT UNIQUE NOT NULL,
  total_points INTEGER DEFAULT 0,
  role public.user_role DEFAULT 'user'::public.user_role,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 创建分组表
CREATE TABLE public.groups (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  color TEXT NOT NULL DEFAULT '#4361EE',
  order_index INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 创建评分标准表
CREATE TABLE public.scoring_criteria (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  criteria_json JSONB NOT NULL,
  is_default BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 创建待办事项表
CREATE TABLE public.todos (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  description TEXT,
  due_date TIMESTAMPTZ,
  score INTEGER DEFAULT 0,
  status public.todo_status DEFAULT 'pending'::public.todo_status,
  group_id UUID REFERENCES public.groups(id) ON DELETE SET NULL,
  priority public.priority_level DEFAULT 'medium'::public.priority_level,
  criteria_id UUID REFERENCES public.scoring_criteria(id) ON DELETE SET NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  completed_at TIMESTAMPTZ
);

-- 创建积分历史表
CREATE TABLE public.points_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
  points INTEGER NOT NULL,
  source_type public.points_source_type NOT NULL,
  source_id UUID,
  description TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 创建月排行榜快照表
CREATE TABLE public.monthly_rankings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  year_month TEXT NOT NULL,
  user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
  rank INTEGER NOT NULL,
  points INTEGER NOT NULL,
  awarded_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(year_month, user_id)
);

-- 创建索引
CREATE INDEX idx_todos_user_id ON public.todos(user_id);
CREATE INDEX idx_todos_status ON public.todos(status);
CREATE INDEX idx_todos_due_date ON public.todos(due_date);
CREATE INDEX idx_groups_user_id ON public.groups(user_id);
CREATE INDEX idx_scoring_criteria_user_id ON public.scoring_criteria(user_id);
CREATE INDEX idx_points_history_user_id ON public.points_history(user_id);
CREATE INDEX idx_monthly_rankings_year_month ON public.monthly_rankings(year_month);

-- 创建用户同步触发器函数
CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER SET search_path = public
AS $$
DECLARE
  user_count int;
BEGIN
  SELECT COUNT(*) INTO user_count FROM profiles;
  
  -- 插入用户profile
  INSERT INTO public.profiles (id, email, username, role)
  VALUES (
    NEW.id,
    NEW.email,
    COALESCE(NEW.raw_user_meta_data->>'username', split_part(NEW.email, '@', 1)),
    CASE WHEN user_count = 0 THEN 'admin'::public.user_role ELSE 'user'::public.user_role END
  );
  
  -- 创建默认分组
  INSERT INTO public.groups (user_id, name, color, order_index)
  VALUES 
    (NEW.id, '工作', '#4361EE', 0),
    (NEW.id, '学习', '#F3722C', 1),
    (NEW.id, '生活', '#38B000', 2);
  
  -- 创建默认评分标准
  INSERT INTO public.scoring_criteria (user_id, name, criteria_json, is_default)
  VALUES (
    NEW.id,
    '默认评分标准',
    '{"importance": 0.4, "urgency": 0.3, "complexity": 0.2, "impact": 0.1}'::jsonb,
    true
  );
  
  RETURN NEW;
END;
$$;

-- 创建触发器
DROP TRIGGER IF EXISTS on_auth_user_confirmed ON auth.users;
CREATE TRIGGER on_auth_user_confirmed
  AFTER UPDATE ON auth.users
  FOR EACH ROW
  WHEN (OLD.confirmed_at IS NULL AND NEW.confirmed_at IS NOT NULL)
  EXECUTE FUNCTION handle_new_user();

-- 创建is_admin辅助函数
CREATE OR REPLACE FUNCTION is_admin(uid uuid)
RETURNS boolean LANGUAGE sql SECURITY DEFINER AS $$
  SELECT EXISTS (
    SELECT 1 FROM profiles p
    WHERE p.id = uid AND p.role = 'admin'::user_role
  );
$$;

-- 启用RLS
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.todos ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.groups ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.scoring_criteria ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.points_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.monthly_rankings ENABLE ROW LEVEL SECURITY;

-- Profiles表策略
CREATE POLICY "管理员可以查看所有用户" ON public.profiles
  FOR SELECT TO authenticated USING (is_admin(auth.uid()));

CREATE POLICY "用户可以查看自己的profile" ON public.profiles
  FOR SELECT TO authenticated USING (auth.uid() = id);

CREATE POLICY "用户可以更新自己的profile" ON public.profiles
  FOR UPDATE TO authenticated USING (auth.uid() = id)
  WITH CHECK (role IS NOT DISTINCT FROM (SELECT role FROM profiles WHERE id = auth.uid()));

CREATE POLICY "管理员可以更新所有用户" ON public.profiles
  FOR UPDATE TO authenticated USING (is_admin(auth.uid()));

-- Todos表策略
CREATE POLICY "用户可以查看自己的待办" ON public.todos
  FOR SELECT TO authenticated USING (auth.uid() = user_id);

CREATE POLICY "用户可以创建待办" ON public.todos
  FOR INSERT TO authenticated WITH CHECK (auth.uid() = user_id);

CREATE POLICY "用户可以更新自己的待办" ON public.todos
  FOR UPDATE TO authenticated USING (auth.uid() = user_id);

CREATE POLICY "用户可以删除自己的待办" ON public.todos
  FOR DELETE TO authenticated USING (auth.uid() = user_id);

-- Groups表策略
CREATE POLICY "用户可以查看自己的分组" ON public.groups
  FOR SELECT TO authenticated USING (auth.uid() = user_id);

CREATE POLICY "用户可以创建分组" ON public.groups
  FOR INSERT TO authenticated WITH CHECK (auth.uid() = user_id);

CREATE POLICY "用户可以更新自己的分组" ON public.groups
  FOR UPDATE TO authenticated USING (auth.uid() = user_id);

CREATE POLICY "用户可以删除自己的分组" ON public.groups
  FOR DELETE TO authenticated USING (auth.uid() = user_id);

-- Scoring Criteria表策略
CREATE POLICY "用户可以查看自己的评分标准" ON public.scoring_criteria
  FOR SELECT TO authenticated USING (auth.uid() = user_id);

CREATE POLICY "用户可以创建评分标准" ON public.scoring_criteria
  FOR INSERT TO authenticated WITH CHECK (auth.uid() = user_id);

CREATE POLICY "用户可以更新自己的评分标准" ON public.scoring_criteria
  FOR UPDATE TO authenticated USING (auth.uid() = user_id);

CREATE POLICY "用户可以删除自己的评分标准" ON public.scoring_criteria
  FOR DELETE TO authenticated USING (auth.uid() = user_id);

-- Points History表策略
CREATE POLICY "用户可以查看自己的积分历史" ON public.points_history
  FOR SELECT TO authenticated USING (auth.uid() = user_id);

CREATE POLICY "用户可以创建积分历史" ON public.points_history
  FOR INSERT TO authenticated WITH CHECK (auth.uid() = user_id);

-- Monthly Rankings表策略（所有人可查看）
CREATE POLICY "所有人可以查看排行榜" ON public.monthly_rankings
  FOR SELECT TO authenticated USING (true);

CREATE POLICY "管理员可以插入排行榜" ON public.monthly_rankings
  FOR INSERT TO authenticated WITH CHECK (is_admin(auth.uid()));

-- 创建公共视图
CREATE VIEW public.public_profiles AS
  SELECT id, username, total_points, role, created_at FROM profiles;