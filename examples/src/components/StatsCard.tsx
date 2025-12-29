import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { TrendingUp, Calendar, Award, Target } from "lucide-react";

interface StatsCardProps {
  totalTasks: number;
  completedTasks: number;
  weeklyStreak: number;
  avgPointsPerDay: number;
}

export function StatsCard({ totalTasks, completedTasks, weeklyStreak, avgPointsPerDay }: StatsCardProps) {
  const completionRate = totalTasks > 0 ? (completedTasks / totalTasks) * 100 : 0;

  const stats = [
    {
      title: "任务完成率",
      value: `${completionRate.toFixed(1)}%`,
      icon: Target,
      color: "text-success",
      bgColor: "bg-success/10"
    },
    {
      title: "连续完成",
      value: `${weeklyStreak} 天`,
      icon: Calendar,
      color: "text-accent",
      bgColor: "bg-accent/10"
    },
    {
      title: "日均积分",
      value: avgPointsPerDay.toFixed(0),
      icon: TrendingUp,
      color: "text-secondary",
      bgColor: "bg-secondary/10"
    },
    {
      title: "总完成数",
      value: completedTasks.toString(),
      icon: Award,
      color: "text-primary",
      bgColor: "bg-primary/10"
    }
  ];

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
      {stats.map((stat, index) => (
        <Card 
          key={stat.title} 
          className="transition-all duration-300 hover:shadow-glow hover:scale-105 animate-bounce-in"
          style={{ animationDelay: `${index * 0.1}s` }}
        >
          <CardHeader className="pb-2">
            <div className="flex items-center justify-between">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                {stat.title}
              </CardTitle>
              <div className={`p-2 rounded-lg ${stat.bgColor}`}>
                <stat.icon className={`w-4 h-4 ${stat.color}`} />
              </div>
            </div>
          </CardHeader>
          <CardContent className="pt-0">
            <div className={`text-2xl font-bold ${stat.color}`}>
              {stat.value}
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}