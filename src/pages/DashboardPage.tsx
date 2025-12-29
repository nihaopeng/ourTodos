import { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import MainLayout from '@/components/layouts/MainLayout';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { Plus, ListTodo, CheckCircle2, Clock } from 'lucide-react';
import { getTodos, getStatistics } from '@/db/api';
import type { Todo, Statistics } from '@/types/types';
import TodoCard from '@/components/TodoCard';
import AddTodoDialog from '@/components/AddTodoDialog';

export default function DashboardPage() {
  const { user } = useAuth();
  const [todos, setTodos] = useState<Todo[]>([]);
  const [statistics, setStatistics] = useState<Statistics | null>(null);
  const [loading, setLoading] = useState(true);
  const [addDialogOpen, setAddDialogOpen] = useState(false);

  const loadData = async () => {
    if (!user) return;

    try {
      setLoading(true);
      const [todosData, statsData] = await Promise.all([
        getTodos(user.id, 'pending'),
        getStatistics(user.id),
      ]);
      setTodos(todosData);
      setStatistics(statsData);
    } catch (error) {
      console.error('加载数据失败:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [user]);

  const handleTodoAdded = () => {
    loadData();
  };

  const handleTodoUpdated = () => {
    loadData();
  };

  return (
    <MainLayout>
      <div className="space-y-6">
        {/* 统计卡片 */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {loading ? (
            <>
              {[...Array(4)].map((_, i) => (
                <Card key={i}>
                  <CardHeader className="pb-2">
                    <Skeleton className="h-4 w-20 bg-muted" />
                  </CardHeader>
                  <CardContent>
                    <Skeleton className="h-8 w-16 bg-muted" />
                  </CardContent>
                </Card>
              ))}
            </>
          ) : (
            <>
              <Card>
                <CardHeader className="pb-2">
                  <CardDescription className="flex items-center gap-2">
                    <ListTodo className="w-4 h-4" />
                    总待办
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{statistics?.total_todos || 0}</div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-2">
                  <CardDescription className="flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4" />
                    已完成
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-success">
                    {statistics?.completed_todos || 0}
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-2">
                  <CardDescription className="flex items-center gap-2">
                    <Clock className="w-4 h-4" />
                    进行中
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-secondary">
                    {statistics?.pending_todos || 0}
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-2">
                  <CardDescription>完成率</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">
                    {statistics?.completion_rate.toFixed(0) || 0}%
                  </div>
                </CardContent>
              </Card>
            </>
          )}
        </div>

        {/* 待办列表 */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>我的待办事项</CardTitle>
                <CardDescription>管理您的任务并获得积分奖励</CardDescription>
              </div>
              <Button onClick={() => setAddDialogOpen(true)} className="gap-2">
                <Plus className="w-4 h-4" />
                添加待办
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="space-y-4">
                {[...Array(3)].map((_, i) => (
                  <div key={i} className="p-4 border border-border rounded-lg">
                    <Skeleton className="h-6 w-3/4 mb-2 bg-muted" />
                    <Skeleton className="h-4 w-1/2 bg-muted" />
                  </div>
                ))}
              </div>
            ) : todos.length === 0 ? (
              <div className="text-center py-12">
                <div className="w-16 h-16 rounded-full bg-muted mx-auto mb-4 flex items-center justify-center">
                  <ListTodo className="w-8 h-8 text-muted-foreground" />
                </div>
                <h3 className="text-lg font-medium mb-2">暂无待办事项</h3>
                <p className="text-muted-foreground mb-4">
                  创建您的第一个待办事项，开始获得积分吧！
                </p>
                <Button onClick={() => setAddDialogOpen(true)} className="gap-2">
                  <Plus className="w-4 h-4" />
                  添加待办
                </Button>
              </div>
            ) : (
              <div className="space-y-4">
                {todos.map((todo) => (
                  <TodoCard key={todo.id} todo={todo} onUpdate={handleTodoUpdated} />
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      <AddTodoDialog open={addDialogOpen} onOpenChange={setAddDialogOpen} onSuccess={handleTodoAdded} />
    </MainLayout>
  );
}
