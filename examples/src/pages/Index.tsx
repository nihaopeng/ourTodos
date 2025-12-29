import { useState } from "react";
import { PointsHeader } from "@/components/PointsHeader";
import { TaskCard, Task } from "@/components/TaskCard";
import { RewardStore, Reward } from "@/components/RewardStore";
import { StatsCard } from "@/components/StatsCard";
import { AddTaskDialog } from "@/components/AddTaskDialog";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useToast } from "@/hooks/use-toast";

const Index = () => {
  const { toast } = useToast();
  
  // Mock data - 可以替换为实际的状态管理
  const [userPoints, setUserPoints] = useState(1250);
  const [tasks, setTasks] = useState<Task[]>([
    {
      id: "1",
      title: "整理书桌",
      description: "把书桌上的书本和文具分类整理好",
      points: 50,
      bonusPoints: 20,
      category: "家务",
      completed: false,
      difficulty: "简单",
      deadline: new Date(Date.now() + 2 * 24 * 60 * 60 * 1000)
    },
    {
      id: "2", 
      title: "完成数学作业",
      description: "完成暑假数学练习册第10-15页",
      points: 100,
      bonusPoints: 50,
      category: "学习",
      completed: false,
      difficulty: "中等",
      progress: 3,
      maxProgress: 6
    },
    {
      id: "3",
      title: "洗碗刷锅",
      description: "饭后主动洗碗并整理厨房",
      points: 80,
      category: "家务", 
      completed: true,
      difficulty: "中等"
    },
    {
      id: "4",
      title: "阅读30分钟",
      description: "阅读课外书籍，培养阅读习惯",
      points: 60,
      bonusPoints: 30,
      category: "学习",
      completed: false,
      difficulty: "简单",
      progress: 1,
      maxProgress: 5
    },
    {
      id: "5",
      title: "整理房间",
      description: "把衣服整理好，房间保持干净整洁",
      points: 120,
      bonusPoints: 40,
      category: "家务",
      completed: false,
      difficulty: "困难"
    }
  ]);

  const rewards: Reward[] = [
    {
      id: "r1",
      name: "乐高积木套装",
      description: "小型建筑系列，培养动手能力",
      cost: 2000,
      category: "玩具",
      available: true,
      icon: "🧱",
      popularity: 1
    },
    {
      id: "r2",
      name: "美味冰淇淋",
      description: "哈根达斯两球装，任选口味",
      cost: 300,
      category: "零食",
      available: true,
      icon: "🍨",
      popularity: 2
    },
    {
      id: "r3",
      name: "电影院观影",
      description: "和家人一起看最新上映的电影",
      cost: 800,
      category: "活动",
      available: true,
      icon: "🎬"
    },
    {
      id: "r4",
      name: "晚睡特权",
      description: "周末可以晚睡1小时",
      cost: 500,
      category: "特权",
      available: true,
      icon: "🌙",
      popularity: 3
    },
    {
      id: "r5",
      name: "游乐园门票",
      description: "迪士尼乐园一日游门票",
      cost: 3000,
      category: "活动",
      available: true,
      icon: "🎠"
    },
    {
      id: "r6",
      name: "精美文具套装",
      description: "包含彩色笔、便签本等学习用品",
      cost: 600,
      category: "玩具",
      available: true,
      icon: "✏️"
    }
  ];

  const weeklyTarget = 500;
  const [weeklyProgress, setWeeklyProgress] = useState(380);
  const currentLevel = Math.floor(userPoints / 500) + 1; // 每500积分升一级

  const completedTasksCount = tasks.filter(task => task.completed).length;
  const totalTasksCount = tasks.length;
  const weeklyStreak = 5; // 模拟数据
  const avgPointsPerDay = userPoints / 30; // 假设30天

  const handleCompleteTask = (taskId: string) => {
    setTasks(prevTasks => 
      prevTasks.map(task => {
        if (task.id === taskId && !task.completed) {
          const pointsEarned = task.points + (task.bonusPoints || 0);
          
          // 使用 setTimeout 来避免渲染期间状态更新的警告
          setTimeout(() => {
            setUserPoints(prev => prev + pointsEarned);
            setWeeklyProgress(prev => prev + pointsEarned);
            toast({
              title: "任务完成! 🎉",
              description: `获得 ${pointsEarned} 积分! 总积分: ${userPoints + pointsEarned}`,
            });
          }, 0);

          return { ...task, completed: true };
        }
        return task;
      })
    );
  };

  const handleTaskProgress = (taskId: string, progress: number) => {
    setTasks(prevTasks =>
      prevTasks.map(task =>
        task.id === taskId ? { ...task, progress } : task
      )
    );
    
    toast({
      title: "进度更新!",
      description: "任务进度已更新，继续努力!",
    });
  };

  const handlePurchaseReward = (rewardId: string) => {
    const reward = rewards.find(r => r.id === rewardId);
    if (reward && userPoints >= reward.cost) {
      setUserPoints(prev => prev - reward.cost);
      toast({
        title: "兑换成功! 🎁",
        description: `成功兑换 ${reward.name}! 积分余额: ${userPoints - reward.cost}`,
      });
    } else {
      toast({
        title: "兑换失败",
        description: "积分不足，继续完成任务赚取积分吧!",
        variant: "destructive"
      });
    }
  };

  const handleAddTask = (newTaskData: Omit<Task, 'id' | 'completed'>) => {
    const newTask: Task = {
      ...newTaskData,
      id: Date.now().toString(),
      completed: false
    };
    
    setTasks(prev => [...prev, newTask]);
    
    toast({
      title: "任务添加成功! ✨",
      description: `新任务"${newTask.title}"已添加到任务列表!`,
    });
  };

  const pendingTasks = tasks.filter(task => !task.completed);
  const completedTasks = tasks.filter(task => task.completed);

  return (
    <div className="min-h-screen bg-background p-4 md:p-6">
      <div className="max-w-6xl mx-auto space-y-6">
        <PointsHeader 
          totalPoints={userPoints}
          weeklyTarget={weeklyTarget}
          weeklyProgress={weeklyProgress}
          level={currentLevel}
        />

        <StatsCard
          totalTasks={totalTasksCount}
          completedTasks={completedTasksCount}
          weeklyStreak={weeklyStreak}
          avgPointsPerDay={avgPointsPerDay}
        />

        <Tabs defaultValue="tasks" className="space-y-6">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="tasks">任务中心</TabsTrigger>
            <TabsTrigger value="rewards">积分商城</TabsTrigger>
          </TabsList>

          <TabsContent value="tasks" className="space-y-6">
            <div>
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-2xl font-bold">待完成任务</h2>
                <AddTaskDialog onAddTask={handleAddTask} />
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {pendingTasks.map(task => (
                  <TaskCard
                    key={task.id}
                    task={task}
                    onComplete={handleCompleteTask}
                    onProgress={handleTaskProgress}
                  />
                ))}
              </div>
            </div>

            {completedTasks.length > 0 && (
              <div>
                <h3 className="text-xl font-bold mb-4 text-success">已完成任务</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {completedTasks.map(task => (
                    <TaskCard
                      key={task.id}
                      task={task}
                      onComplete={handleCompleteTask}
                    />
                  ))}
                </div>
              </div>
            )}
          </TabsContent>

          <TabsContent value="rewards">
            <RewardStore
              rewards={rewards}
              userPoints={userPoints}
              onPurchase={handlePurchaseReward}
            />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default Index;
