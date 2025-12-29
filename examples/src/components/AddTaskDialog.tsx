import { useState } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Plus } from "lucide-react";
import { Task } from "@/components/TaskCard";

interface AddTaskDialogProps {
  onAddTask: (task: Omit<Task, 'id' | 'completed'>) => void;
}

export function AddTaskDialog({ onAddTask }: AddTaskDialogProps) {
  const [open, setOpen] = useState(false);
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    points: 50,
    bonusPoints: 0,
    category: "家务" as Task['category'],
    difficulty: "简单" as Task['difficulty'],
    hasProgress: false,
    maxProgress: 1,
    deadline: ""
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.title.trim()) return;

    const newTask: Omit<Task, 'id' | 'completed'> = {
      title: formData.title,
      description: formData.description,
      points: formData.points,
      bonusPoints: formData.bonusPoints || undefined,
      category: formData.category,
      difficulty: formData.difficulty,
      deadline: formData.deadline ? new Date(formData.deadline) : undefined,
      progress: formData.hasProgress ? 0 : undefined,
      maxProgress: formData.hasProgress ? formData.maxProgress : undefined
    };

    onAddTask(newTask);
    
    // Reset form
    setFormData({
      title: "",
      description: "",
      points: 50,
      bonusPoints: 0,
      category: "家务",
      difficulty: "简单",
      hasProgress: false,
      maxProgress: 1,
      deadline: ""
    });
    
    setOpen(false);
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="floating" size="sm">
          <Plus className="w-4 h-4 mr-2" />
          新增任务
        </Button>
      </DialogTrigger>
      
      <DialogContent className="max-w-md">
        <DialogHeader>
          <DialogTitle>添加新任务</DialogTitle>
        </DialogHeader>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="title">任务名称 *</Label>
            <Input
              id="title"
              value={formData.title}
              onChange={(e) => setFormData(prev => ({ ...prev, title: e.target.value }))}
              placeholder="例如：整理书桌"
              required
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="description">任务描述</Label>
            <Textarea
              id="description"
              value={formData.description}
              onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
              placeholder="描述任务的具体要求..."
              rows={3}
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="category">分类</Label>
              <Select value={formData.category} onValueChange={(value: Task['category']) => 
                setFormData(prev => ({ ...prev, category: value }))
              }>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="家务">🏠 家务</SelectItem>
                  <SelectItem value="学习">📚 学习</SelectItem>
                  <SelectItem value="其他">⭐ 其他</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="difficulty">难度</Label>
              <Select value={formData.difficulty} onValueChange={(value: Task['difficulty']) => 
                setFormData(prev => ({ ...prev, difficulty: value }))
              }>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="简单">简单</SelectItem>
                  <SelectItem value="中等">中等</SelectItem>
                  <SelectItem value="困难">困难</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="points">基础积分</Label>
              <Input
                id="points"
                type="number"
                min="10"
                max="500"
                value={formData.points}
                onChange={(e) => setFormData(prev => ({ ...prev, points: Number(e.target.value) }))}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="bonusPoints">奖励积分</Label>
              <Input
                id="bonusPoints"
                type="number"
                min="0"
                max="200"
                value={formData.bonusPoints}
                onChange={(e) => setFormData(prev => ({ ...prev, bonusPoints: Number(e.target.value) }))}
              />
            </div>
          </div>

          <div className="space-y-2">
            <div className="flex items-center gap-2">
              <input
                type="checkbox"
                id="hasProgress"
                checked={formData.hasProgress}
                onChange={(e) => setFormData(prev => ({ ...prev, hasProgress: e.target.checked }))}
                className="rounded"
              />
              <Label htmlFor="hasProgress">需要累积进度完成</Label>
            </div>
            
            {formData.hasProgress && (
              <div className="space-y-2 pl-6">
                <Label htmlFor="maxProgress">总进度数</Label>
                <Input
                  id="maxProgress"
                  type="number"
                  min="2"
                  max="20"
                  value={formData.maxProgress}
                  onChange={(e) => setFormData(prev => ({ ...prev, maxProgress: Number(e.target.value) }))}
                />
                <p className="text-xs text-muted-foreground">
                  例如：完成6页作业，总进度设为6，每页作业点击"+1进度"
                </p>
              </div>
            )}
          </div>

          <div className="space-y-2">
            <Label htmlFor="deadline">截止日期 (可选)</Label>
            <Input
              id="deadline"
              type="date"
              value={formData.deadline}
              onChange={(e) => setFormData(prev => ({ ...prev, deadline: e.target.value }))}
              min={new Date().toISOString().split('T')[0]}
            />
          </div>

          <div className="flex gap-2 pt-4">
            <Button type="button" variant="outline" onClick={() => setOpen(false)} className="flex-1">
              取消
            </Button>
            <Button type="submit" variant="hero" className="flex-1">
              添加任务
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}