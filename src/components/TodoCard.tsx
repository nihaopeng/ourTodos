import { useState } from 'react';
import { format, formatDistanceToNow, isPast } from 'date-fns';
import { zhCN } from 'date-fns/locale';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog';
import { useToast } from '@/hooks/use-toast';
import { MoreVertical, CheckCircle2, Pencil, Trash2, Clock, Star } from 'lucide-react';
import { completeTodo, deleteTodo, updateTodo, createPointsHistory, updateProfile } from '@/db/api';
import { useAuth } from '@/contexts/AuthContext';
import type { Todo } from '@/types/types';
import { cn } from '@/lib/utils';
import EditTodoDialog from './EditTodoDialog';

interface TodoCardProps {
  todo: Todo;
  onUpdate: () => void;
}

const priorityConfig = {
  low: { label: '低', color: 'bg-muted text-muted-foreground' },
  medium: { label: '中', color: 'bg-primary/10 text-primary' },
  high: { label: '高', color: 'bg-secondary/10 text-secondary' },
  urgent: { label: '紧急', color: 'bg-destructive/10 text-destructive' },
};

export default function TodoCard({ todo, onUpdate }: TodoCardProps) {
  const { user, profile, refreshProfile } = useAuth();
  const { toast } = useToast();
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [loading, setLoading] = useState(false);

  const isOverdue = todo.due_date && isPast(new Date(todo.due_date));

  const handleComplete = async () => {
    if (!user || !profile) return;

    try {
      setLoading(true);

      // 完成待办
      await completeTodo(todo.id);

      // 计算积分
      let points = todo.score;
      let multiplier = 1;
      let description = `完成待办：${todo.title}`;

      if (todo.due_date) {
        const now = new Date();
        const dueDate = new Date(todo.due_date);
        if (now < dueDate) {
          // 提前完成
          multiplier = 1.1;
          description += ' (提前完成)';
        } else if (now > dueDate) {
          // 延期完成
          multiplier = 0.8;
          description += ' (延期完成)';
        }
      }

      points = Math.round(points * multiplier);

      // 添加积分历史
      await createPointsHistory({
        user_id: user.id,
        points,
        source_type: multiplier > 1 ? 'todo_early' : multiplier < 1 ? 'todo_late' : 'todo_completed',
        source_id: todo.id,
        description,
      });

      // 更新用户总积分
      await updateProfile(user.id, {
        total_points: (profile.total_points || 0) + points,
      });

      // 刷新profile
      await refreshProfile();

      toast({
        title: '完成待办',
        description: `获得 ${points} 积分！`,
      });

      onUpdate();
    } catch (error) {
      console.error('完成待办失败:', error);
      toast({
        title: '错误',
        description: '完成待办失败，请重试',
        variant: 'destructive',
      });
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!user) return;

    try {
      setLoading(true);
      await deleteTodo(todo.id);

      toast({
        title: '删除成功',
        description: '待办事项已删除',
      });

      onUpdate();
    } catch (error) {
      console.error('删除待办失败:', error);
      toast({
        title: '错误',
        description: '删除待办失败，请重试',
        variant: 'destructive',
      });
    } finally {
      setLoading(false);
      setDeleteDialogOpen(false);
    }
  };

  return (
    <>
      <div className="group p-4 border border-border rounded-lg hover:shadow-md transition-shadow bg-card">
        <div className="flex items-start gap-4">
          {/* 评分显示 */}
          <div className="flex flex-col items-center justify-center w-16 h-16 rounded-lg gradient-primary text-primary-foreground shrink-0">
            <Star className="w-5 h-5 mb-1" />
            <span className="text-lg font-bold">{todo.score}</span>
          </div>

          {/* 内容区 */}
          <div className="flex-1 min-w-0">
            <div className="flex items-start justify-between gap-2 mb-2">
              <h3 className="font-semibold text-lg">{todo.title}</h3>
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" size="icon" className="shrink-0">
                    <MoreVertical className="w-4 h-4" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                  <DropdownMenuItem onClick={handleComplete} disabled={loading}>
                    <CheckCircle2 className="mr-2 h-4 w-4" />
                    完成
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={() => setEditDialogOpen(true)}>
                    <Pencil className="mr-2 h-4 w-4" />
                    编辑
                  </DropdownMenuItem>
                  <DropdownMenuItem
                    onClick={() => setDeleteDialogOpen(true)}
                    className="text-destructive"
                  >
                    <Trash2 className="mr-2 h-4 w-4" />
                    删除
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>

            {todo.description && (
              <p className="text-sm text-muted-foreground mb-3 line-clamp-2">
                {todo.description}
              </p>
            )}

            <div className="flex flex-wrap items-center gap-2">
              <Badge className={priorityConfig[todo.priority].color}>
                {priorityConfig[todo.priority].label}
              </Badge>

              {todo.group && (
                <Badge variant="outline" style={{ borderColor: todo.group.color }}>
                  <span style={{ color: todo.group.color }}>●</span>
                  <span className="ml-1">{todo.group.name}</span>
                </Badge>
              )}

              {todo.due_date && (
                <Badge
                  variant="outline"
                  className={cn(
                    'flex items-center gap-1',
                    isOverdue && 'border-destructive text-destructive'
                  )}
                >
                  <Clock className="w-3 h-3" />
                  {isOverdue ? '已逾期' : formatDistanceToNow(new Date(todo.due_date), {
                    addSuffix: true,
                    locale: zhCN,
                  })}
                </Badge>
              )}
            </div>
          </div>
        </div>
      </div>

      <AlertDialog open={deleteDialogOpen} onOpenChange={setDeleteDialogOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>确认删除</AlertDialogTitle>
            <AlertDialogDescription>
              确定要删除待办事项"{todo.title}"吗？此操作无法撤销。
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>取消</AlertDialogCancel>
            <AlertDialogAction onClick={handleDelete} disabled={loading}>
              删除
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>

      <EditTodoDialog
        open={editDialogOpen}
        onOpenChange={setEditDialogOpen}
        todo={todo}
        onSuccess={onUpdate}
      />
    </>
  );
}
