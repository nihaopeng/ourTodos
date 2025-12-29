import { useState } from 'react';
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
import { Slider } from '@/components/ui/slider';
import { Switch } from '@/components/ui/switch';
import { useToast } from '@/hooks/use-toast';
import { Loader2 } from 'lucide-react';
import { createScoringCriteria } from '@/db/api';

interface AddCriteriaDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSuccess: () => void;
}

export default function AddCriteriaDialog({ open, onOpenChange, onSuccess }: AddCriteriaDialogProps) {
  const { user } = useAuth();
  const { toast } = useToast();
  const [loading, setLoading] = useState(false);

  const [formData, setFormData] = useState({
    name: '',
    is_default: false,
    importance: 40,
    urgency: 30,
    complexity: 20,
    impact: 10,
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!user) return;

    if (!formData.name) {
      toast({
        title: '错误',
        description: '请填写标准名称',
        variant: 'destructive',
      });
      return;
    }

    // 验证权重总和是否为100
    const total = formData.importance + formData.urgency + formData.complexity + formData.impact;
    if (total !== 100) {
      toast({
        title: '错误',
        description: '权重总和必须为100%',
        variant: 'destructive',
      });
      return;
    }

    try {
      setLoading(true);

      await createScoringCriteria({
        user_id: user.id,
        name: formData.name,
        criteria_json: {
          importance: formData.importance / 100,
          urgency: formData.urgency / 100,
          complexity: formData.complexity / 100,
          impact: formData.impact / 100,
        },
        is_default: formData.is_default,
      });

      toast({
        title: '创建成功',
        description: '评分标准已创建',
      });

      // 重置表单
      setFormData({
        name: '',
        is_default: false,
        importance: 40,
        urgency: 30,
        complexity: 20,
        impact: 10,
      });

      onSuccess();
      onOpenChange(false);
    } catch (error) {
      console.error('创建评分标准失败:', error);
      toast({
        title: '错误',
        description: '创建评分标准失败，请重试',
        variant: 'destructive',
      });
    } finally {
      setLoading(false);
    }
  };

  const total = formData.importance + formData.urgency + formData.complexity + formData.impact;

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>添加评分标准</DialogTitle>
          <DialogDescription>创建新的评分标准，自定义AI评分规则</DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit}>
          <div className="space-y-4 py-4">
            <div className="space-y-2">
              <Label htmlFor="name">标准名称 *</Label>
              <Input
                id="name"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                placeholder="例如：工作任务标准"
                disabled={loading}
              />
            </div>

            <div className="flex items-center justify-between">
              <Label htmlFor="is_default">设为默认标准</Label>
              <Switch
                id="is_default"
                checked={formData.is_default}
                onCheckedChange={(checked) => setFormData({ ...formData, is_default: checked })}
                disabled={loading}
              />
            </div>

            <div className="space-y-4 pt-2">
              <div className="flex items-center justify-between mb-2">
                <h4 className="text-sm font-medium">权重分配</h4>
                <span className={`text-sm font-medium ${total === 100 ? 'text-success' : 'text-destructive'}`}>
                  总计: {total}%
                </span>
              </div>

              <div className="space-y-4">
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <Label>重要性</Label>
                    <span className="text-sm font-medium">{formData.importance}%</span>
                  </div>
                  <Slider
                    value={[formData.importance]}
                    onValueChange={([value]) => setFormData({ ...formData, importance: value })}
                    max={100}
                    step={5}
                    disabled={loading}
                  />
                </div>

                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <Label>紧急性</Label>
                    <span className="text-sm font-medium">{formData.urgency}%</span>
                  </div>
                  <Slider
                    value={[formData.urgency]}
                    onValueChange={([value]) => setFormData({ ...formData, urgency: value })}
                    max={100}
                    step={5}
                    disabled={loading}
                  />
                </div>

                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <Label>复杂性</Label>
                    <span className="text-sm font-medium">{formData.complexity}%</span>
                  </div>
                  <Slider
                    value={[formData.complexity]}
                    onValueChange={([value]) => setFormData({ ...formData, complexity: value })}
                    max={100}
                    step={5}
                    disabled={loading}
                  />
                </div>

                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <Label>影响力</Label>
                    <span className="text-sm font-medium">{formData.impact}%</span>
                  </div>
                  <Slider
                    value={[formData.impact]}
                    onValueChange={([value]) => setFormData({ ...formData, impact: value })}
                    max={100}
                    step={5}
                    disabled={loading}
                  />
                </div>
              </div>
            </div>
          </div>

          <DialogFooter>
            <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>
              取消
            </Button>
            <Button type="submit" disabled={loading || total !== 100}>
              {loading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  创建中...
                </>
              ) : (
                '创建'
              )}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
