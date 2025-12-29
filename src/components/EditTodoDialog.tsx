import { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { useToast } from '@/hooks/use-toast';
import { Loader2, Sparkles } from 'lucide-react';
import { updateTodo, getGroups, getDefaultCriteria } from '@/db/api';
import { supabase } from '@/db/supabase';
import type { Todo, Group, ScoringCriteria, PriorityLevel } from '@/types/types';
import { format } from 'date-fns';

interface EditTodoDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  todo: Todo;
  onSuccess: () => void;
}

export default function EditTodoDialog({ open, onOpenChange, todo, onSuccess }: EditTodoDialogProps) {
  const { user } = useAuth();
  const { toast } = useToast();
  const [loading, setLoading] = useState(false);
  const [scoringLoading, setScoringLoading] = useState(false);
  const [groups, setGroups] = useState<Group[]>([]);
  const [defaultCriteria, setDefaultCriteria] = useState<ScoringCriteria | null>(null);

  const [formData, setFormData] = useState({
    title: todo.title,
    description: todo.description || '',
    due_date: todo.due_date ? format(new Date(todo.due_date), "yyyy-MM-dd'T'HH:mm") : '',
    priority: todo.priority,
    group_id: todo.group_id || 'none',
  });

  const [score, setScore] = useState(todo.score);

  useEffect(() => {
    if (open && user) {
      loadGroups();
      loadDefaultCriteria();
    }
  }, [open, user]);

  useEffect(() => {
    if (open) {
      setFormData({
        title: todo.title,
        description: todo.description || '',
        due_date: todo.due_date ? format(new Date(todo.due_date), "yyyy-MM-dd'T'HH:mm") : '',
        priority: todo.priority,
        group_id: todo.group_id || 'none',
      });
      setScore(todo.score);
    }
  }, [open, todo]);

  const loadGroups = async () => {
    if (!user) return;
    try {
      const data = await getGroups(user.id);
      setGroups(data);
    } catch (error) {
      console.error('加载分组失败:', error);
    }
  };

  const loadDefaultCriteria = async () => {
    if (!user) return;
    try {
      const data = await getDefaultCriteria(user.id);
      setDefaultCriteria(data);
    } catch (error) {
      console.error('加载评分标准失败:', error);
    }
  };

  const handleScoreCalculation = async () => {
    if (!formData.title || !formData.description || !defaultCriteria) {
      toast({
        title: '提示',
        description: '请填写标题和描述后再进行评分',
        variant: 'destructive',
      });
      return;
    }

    try {
      setScoringLoading(true);

      const { data, error } = await supabase.functions.invoke('score-todo', {
        body: {
          title: formData.title,
          description: formData.description,
          criteria: defaultCriteria.criteria_json,
        },
      });

      if (error) {
        const errorMsg = await error?.context?.text();
        console.error('AI评分失败:', errorMsg || error?.message);
        throw new Error('AI评分失败');
      }

      if (data?.score) {
        setScore(data.score);
        toast({
          title: '评分完成',
          description: `AI评分：${data.score} 分`,
        });
      } else {
        throw new Error('评分结果无效');
      }
    } catch (error) {
      console.error('评分失败:', error);
      toast({
        title: '评分失败',
        description: 'AI评分暂时不可用',
        variant: 'destructive',
      });
    } finally {
      setScoringLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!user) return;

    if (!formData.title) {
      toast({
        title: '错误',
        description: '请填写待办标题',
        variant: 'destructive',
      });
      return;
    }

    try {
      setLoading(true);

      await updateTodo(todo.id, {
        title: formData.title,
        description: formData.description || null,
        due_date: formData.due_date || null,
        priority: formData.priority,
        group_id: formData.group_id === 'none' ? null : formData.group_id || null,
        score,
      });

      toast({
        title: '更新成功',
        description: '待办事项已更新',
      });

      onSuccess();
      onOpenChange(false);
    } catch (error) {
      console.error('更新待办失败:', error);
      toast({
        title: '错误',
        description: '更新待办失败，请重试',
        variant: 'destructive',
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>编辑待办事项</DialogTitle>
          <DialogDescription>修改待办事项信息并重新评分</DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit}>
          <div className="space-y-4 py-4">
            <div className="space-y-2">
              <Label htmlFor="edit-title">标题 *</Label>
              <Input
                id="edit-title"
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                placeholder="输入待办事项标题"
                disabled={loading}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="edit-description">描述</Label>
              <Textarea
                id="edit-description"
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                placeholder="详细描述待办事项内容"
                rows={3}
                disabled={loading}
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="edit-priority">优先级</Label>
                <Select
                  value={formData.priority}
                  onValueChange={(value) =>
                    setFormData({ ...formData, priority: value as PriorityLevel })
                  }
                  disabled={loading}
                >
                  <SelectTrigger id="edit-priority">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="low">低</SelectItem>
                    <SelectItem value="medium">中</SelectItem>
                    <SelectItem value="high">高</SelectItem>
                    <SelectItem value="urgent">紧急</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="edit-group">分组</Label>
                <Select
                  value={formData.group_id}
                  onValueChange={(value) => setFormData({ ...formData, group_id: value })}
                  disabled={loading}
                >
                  <SelectTrigger id="edit-group">
                    <SelectValue placeholder="选择分组" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="none">无分组</SelectItem>
                    {groups.map((group) => (
                      <SelectItem key={group.id} value={group.id}>
                        {group.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="edit-due_date">截止时间</Label>
              <Input
                id="edit-due_date"
                type="datetime-local"
                value={formData.due_date}
                onChange={(e) => setFormData({ ...formData, due_date: e.target.value })}
                disabled={loading}
              />
            </div>

            {/* AI评分区域 */}
            <div className="p-4 rounded-lg bg-muted space-y-2">
              <div className="flex items-center justify-between">
                <Label>AI评分</Label>
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={handleScoreCalculation}
                  disabled={scoringLoading || !formData.title || !formData.description}
                >
                  {scoringLoading ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      评分中...
                    </>
                  ) : (
                    <>
                      <Sparkles className="mr-2 h-4 w-4" />
                      重新评分
                    </>
                  )}
                </Button>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold gradient-text">{score}</div>
                <p className="text-xs text-muted-foreground">完成后可获得的积分</p>
              </div>
            </div>
          </div>

          <DialogFooter>
            <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>
              取消
            </Button>
            <Button type="submit" disabled={loading || scoringLoading}>
              {loading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  更新中...
                </>
              ) : (
                '更新'
              )}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
