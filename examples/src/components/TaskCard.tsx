import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Check, Clock, Star, Zap } from "lucide-react";

export interface Task {
  id: string;
  title: string;
  description: string;
  points: number;
  bonusPoints?: number;
  category: "家务" | "学习" | "其他";
  completed: boolean;
  difficulty: "简单" | "中等" | "困难";
  deadline?: Date;
  progress?: number;
  maxProgress?: number;
}

interface TaskCardProps {
  task: Task;
  onComplete: (taskId: string) => void;
  onProgress?: (taskId: string, progress: number) => void;
}

export function TaskCard({ task, onComplete, onProgress }: TaskCardProps) {
  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case "简单": return "success";
      case "中等": return "secondary";
      case "困难": return "accent";
      default: return "default";
    }
  };

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case "家务": return "🏠";
      case "学习": return "📚";
      default: return "⭐";
    }
  };

  const progressPercentage = task.maxProgress 
    ? ((task.progress || 0) / task.maxProgress) * 100 
    : 0;

  const isPartiallyComplete = task.maxProgress && (task.progress || 0) > 0;
  const canComplete = !task.maxProgress || (task.progress || 0) >= task.maxProgress;

  return (
    <Card className={`transition-all duration-300 hover:shadow-glow hover:scale-105 ${
      task.completed ? 'bg-success/10 border-success' : ''
    }`}>
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-2">
            <span className="text-2xl">{getCategoryIcon(task.category)}</span>
            <div>
              <CardTitle className="text-lg">{task.title}</CardTitle>
              <p className="text-sm text-muted-foreground mt-1">{task.description}</p>
            </div>
          </div>
          <Badge variant={getDifficultyColor(task.difficulty) as any}>
            {task.difficulty}
          </Badge>
        </div>
      </CardHeader>

      <CardContent>
        <div className="space-y-4">
          {/* Progress bar for incremental tasks */}
          {task.maxProgress && (
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span>进度</span>
                <span>{task.progress || 0} / {task.maxProgress}</span>
              </div>
              <Progress value={progressPercentage} className="h-2" />
            </div>
          )}

          {/* Points display */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Star className="w-4 h-4 text-yellow-500" />
              <span className="font-bold text-primary">{task.points} 积分</span>
              {task.bonusPoints && (
                <div className="flex items-center gap-1">
                  <Zap className="w-3 h-3 text-orange-500" />
                  <span className="text-xs text-orange-600 font-medium">
                    +{task.bonusPoints} 奖励
                  </span>
                </div>
              )}
            </div>

            {task.deadline && (
              <div className="flex items-center gap-1 text-xs text-muted-foreground">
                <Clock className="w-3 h-3" />
                <span>{task.deadline.toLocaleDateString()}</span>
              </div>
            )}
          </div>

          {/* Action buttons */}
          <div className="flex gap-2">
            {task.completed ? (
              <Button variant="success" className="w-full" disabled>
                <Check className="w-4 h-4 mr-2" />
                已完成
              </Button>
            ) : (
              <>
                {task.maxProgress && onProgress && (
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => onProgress(task.id, (task.progress || 0) + 1)}
                    disabled={canComplete}
                    title="点击增加任务进度，达到要求后才能完成任务"
                  >
                    +1 进度
                  </Button>
                )}
                <Button
                  variant={canComplete ? "hero" : "outline"}
                  className="flex-1"
                  onClick={() => onComplete(task.id)}
                  disabled={!canComplete}
                  title={!canComplete ? "需要先完成所有进度要求才能提交任务" : "点击完成任务并获得积分"}
                >
                  {canComplete ? "完成任务" : `进度不足 (${task.progress || 0}/${task.maxProgress})`}
                </Button>
              </>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}