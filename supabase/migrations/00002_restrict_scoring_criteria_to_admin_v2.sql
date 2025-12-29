-- 删除现有的评分标准表策略
DROP POLICY IF EXISTS "用户可以创建评分标准" ON scoring_criteria;
DROP POLICY IF EXISTS "用户可以更新自己的评分标准" ON scoring_criteria;
DROP POLICY IF EXISTS "用户可以删除自己的评分标准" ON scoring_criteria;

-- 创建新的策略：只有管理员可以创建、更新、删除评分标准
CREATE POLICY "管理员可以创建评分标准" ON scoring_criteria
  FOR INSERT TO authenticated
  WITH CHECK (is_admin(auth.uid()));

CREATE POLICY "管理员可以更新评分标准" ON scoring_criteria
  FOR UPDATE TO authenticated
  USING (is_admin(auth.uid()))
  WITH CHECK (is_admin(auth.uid()));

CREATE POLICY "管理员可以删除评分标准" ON scoring_criteria
  FOR DELETE TO authenticated
  USING (is_admin(auth.uid()));