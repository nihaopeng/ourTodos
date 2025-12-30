import { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import MainLayout from '@/components/layouts/MainLayout';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { Trophy, Medal, TrendingUp, TrendingDown, Minus } from 'lucide-react';
import { getLeaderboard } from '@/db/api';
import type { LeaderboardEntry } from '@/types/types';
import { cn } from '@/lib/utils';

export default function LeaderboardPage() {
  const { user } = useAuth();
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'all' | 'week' | 'month'>('all');

  useEffect(() => {
    loadLeaderboard();
  }, [activeTab]);

  const loadLeaderboard = async () => {
    try {
      setLoading(true);
      const data = await getLeaderboard(activeTab, 50);
      setLeaderboard(data);
    } catch (error) {
      console.error('加载排行榜失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const getRankIcon = (rank: number) => {
    if (rank === 1) return <Trophy className="w-6 h-6 text-yellow-500" />;
    if (rank === 2) return <Medal className="w-6 h-6 text-gray-400" />;
    if (rank === 3) return <Medal className="w-6 h-6 text-amber-600" />;
    return null;
  };

  const getRankBadge = (rank: number) => {
    if (rank === 1) return 'bg-yellow-500/10 text-yellow-500 border-yellow-500/20';
    if (rank === 2) return 'bg-gray-400/10 text-gray-400 border-gray-400/20';
    if (rank === 3) return 'bg-amber-600/10 text-amber-600 border-amber-600/20';
    return 'bg-muted text-muted-foreground';
  };

  return (
    <MainLayout>
      <div className="space-y-6">
        {/* 页面标题 */}
        <div>
          <div className="flex items-center gap-3 mb-2">
            <img src="/images/rank.png" alt="排行榜" className="w-12 h-12" />
            <h1 className="text-3xl font-bold gradient-text">排行榜</h1>
          </div>
          <p className="text-muted-foreground">查看积分排名，激励自己不断进步</p>
        </div>

        {/* 排行榜卡片 */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Trophy className="w-5 h-5" />
              积分排行榜
            </CardTitle>
            <CardDescription>根据用户积分进行排名</CardDescription>
          </CardHeader>
          <CardContent>
            <Tabs value={activeTab} onValueChange={(v) => setActiveTab(v as typeof activeTab)}>
              <TabsList className="grid w-full grid-cols-3 mb-6">
                <TabsTrigger value="all">总榜</TabsTrigger>
                <TabsTrigger value="month">月榜</TabsTrigger>
                <TabsTrigger value="week">周榜</TabsTrigger>
              </TabsList>

              <TabsContent value={activeTab} className="space-y-4">
                {loading ? (
                  <>
                    {[...Array(10)].map((_, i) => (
                      <div key={i} className="flex items-center gap-4 p-4 border border-border rounded-lg">
                        <Skeleton className="w-12 h-12 rounded-full bg-muted" />
                        <div className="flex-1">
                          <Skeleton className="h-5 w-32 mb-2 bg-muted" />
                          <Skeleton className="h-4 w-20 bg-muted" />
                        </div>
                        <Skeleton className="h-8 w-16 bg-muted" />
                      </div>
                    ))}
                  </>
                ) : leaderboard.length === 0 ? (
                  <div className="text-center py-12">
                    <Trophy className="w-16 h-16 text-muted-foreground mx-auto mb-4" />
                    <h3 className="text-lg font-medium mb-2">暂无排名数据</h3>
                    <p className="text-muted-foreground">完成待办事项以获得积分并上榜</p>
                  </div>
                ) : (
                  <>
                    {/* 前三名特殊展示 */}
                    {leaderboard.slice(0, 3).length > 0 && (
                      <div className="grid gap-4 md:grid-cols-3 mb-6">
                        {leaderboard.slice(0, 3).map((entry) => (
                          <Card
                            key={entry.user_id}
                            className={cn(
                              'relative overflow-hidden',
                              entry.user_id === user?.id && 'ring-2 ring-primary'
                            )}
                          >
                            <div className="absolute top-0 right-0 w-32 h-32 -mr-16 -mt-16 rounded-full opacity-10 gradient-primary" />
                            <CardHeader className="pb-3">
                              <div className="flex items-center justify-between">
                                <Badge className={getRankBadge(entry.rank)}>
                                  第 {entry.rank} 名
                                </Badge>
                                {getRankIcon(entry.rank)}
                              </div>
                            </CardHeader>
                            <CardContent>
                              <div className="flex items-center gap-3 mb-3">
                                <div className="w-12 h-12 rounded-full bg-primary flex items-center justify-center text-primary-foreground font-bold text-lg">
                                  {entry.username.charAt(0).toUpperCase()}
                                </div>
                                <div className="flex-1 min-w-0">
                                  <p className="font-semibold truncate">{entry.username}</p>
                                  {entry.user_id === user?.id && (
                                    <Badge variant="outline" className="text-xs">
                                      我
                                    </Badge>
                                  )}
                                </div>
                              </div>
                              <div className="text-center pt-3 border-t border-border">
                                <div className="text-2xl font-bold gradient-text">
                                  {entry.total_points}
                                </div>
                                <p className="text-xs text-muted-foreground">积分</p>
                              </div>
                            </CardContent>
                          </Card>
                        ))}
                      </div>
                    )}

                    {/* 完整排名列表 */}
                    <div className="space-y-2">
                      {leaderboard.map((entry) => (
                        <div
                          key={entry.user_id}
                          className={cn(
                            'flex items-center gap-4 p-4 border border-border rounded-lg hover:bg-muted/50 transition-colors',
                            entry.user_id === user?.id && 'bg-primary/5 border-primary'
                          )}
                        >
                          {/* 排名 */}
                          <div className="w-12 flex items-center justify-center">
                            {getRankIcon(entry.rank) || (
                              <span className="text-lg font-bold text-muted-foreground">
                                {entry.rank}
                              </span>
                            )}
                          </div>

                          {/* 用户信息 */}
                          <div className="w-12 h-12 rounded-full bg-primary flex items-center justify-center text-primary-foreground font-bold shrink-0">
                            {entry.username.charAt(0).toUpperCase()}
                          </div>
                          <div className="flex-1 min-w-0">
                            <div className="flex items-center gap-2">
                              <p className="font-medium truncate">{entry.username}</p>
                              {entry.user_id === user?.id && (
                                <Badge variant="outline" className="text-xs">
                                  我
                                </Badge>
                              )}
                            </div>
                            <p className="text-sm text-muted-foreground">
                              {entry.total_points} 积分
                            </p>
                          </div>

                          {/* 趋势 */}
                          {entry.trend && (
                            <div className="shrink-0">
                              {entry.trend === 'up' && (
                                <TrendingUp className="w-5 h-5 text-success" />
                              )}
                              {entry.trend === 'down' && (
                                <TrendingDown className="w-5 h-5 text-destructive" />
                              )}
                              {entry.trend === 'same' && (
                                <Minus className="w-5 h-5 text-muted-foreground" />
                              )}
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  </>
                )}
              </TabsContent>
            </Tabs>
          </CardContent>
        </Card>
      </div>
    </MainLayout>
  );
}
