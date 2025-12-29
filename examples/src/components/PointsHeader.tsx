import { Badge } from "@/components/ui/badge";
import { Star, Trophy, Target } from "lucide-react";

interface PointsHeaderProps {
  totalPoints: number;
  weeklyTarget: number;
  weeklyProgress: number;
  level: number;
}

export function PointsHeader({ totalPoints, weeklyTarget, weeklyProgress, level }: PointsHeaderProps) {
  const progressPercentage = (weeklyProgress / weeklyTarget) * 100;
  const isOverTarget = weeklyProgress > weeklyTarget;
  const bonusPoints = isOverTarget ? weeklyProgress - weeklyTarget : 0;

  return (
    <header className="bg-gradient-hero text-white p-6 rounded-2xl shadow-glow mb-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className="bg-white/20 p-3 rounded-full">
            <Star className="w-6 h-6 text-yellow-300" />
          </div>
          <div>
            <h1 className="text-2xl font-bold">积分小达人</h1>
            <p className="text-white/80">暑期积分挑战</p>
          </div>
        </div>
        <div className="text-right">
          <Badge variant="glow" className="mb-2">
            等级 {level}
          </Badge>
          <div className="text-3xl font-bold animate-glow-pulse text-yellow-300">
            {totalPoints.toLocaleString()}
          </div>
          <div className="text-sm text-white/80">总积分</div>
        </div>
      </div>

      <div className="bg-white/10 rounded-lg p-4 backdrop-blur-sm">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-2">
            <Target className="w-4 h-4" />
            <span className="text-sm font-medium">本周目标</span>
          </div>
          <span className="text-sm">
            {weeklyProgress} / {weeklyTarget} 积分
          </span>
        </div>
        
        <div className="w-full bg-white/20 rounded-full h-3 mb-2">
          <div 
            className={`h-3 rounded-full transition-all duration-500 ${
              isOverTarget 
                ? 'bg-gradient-to-r from-yellow-300 to-orange-300 animate-glow-pulse' 
                : 'bg-gradient-to-r from-green-300 to-blue-300'
            }`}
            style={{ width: `${Math.min(progressPercentage, 100)}%` }}
          />
        </div>

        {isOverTarget && (
          <div className="flex items-center gap-2 text-yellow-300 animate-bounce-in">
            <Trophy className="w-4 h-4" />
            <span className="text-sm font-bold">
              超标完成! 获得 {bonusPoints} 奖励积分! 🎉
            </span>
          </div>
        )}
      </div>
    </header>
  );
}