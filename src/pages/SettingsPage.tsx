import { useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import MainLayout from '@/components/layouts/MainLayout';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Separator } from '@/components/ui/separator';
import { useToast } from '@/hooks/use-toast';
import { User, Coins, Calendar, Award } from 'lucide-react';
import { format } from 'date-fns';
import { zhCN } from 'date-fns/locale';

export default function SettingsPage() {
  const { profile } = useAuth();
  const { toast } = useToast();
  const [loading, setLoading] = useState(false);

  const handleUpdateProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    
    toast({
      title: '功能开发中',
      description: '个人信息编辑功能即将上线',
    });
  };

  return (
    <MainLayout>
      <div className="space-y-6">
        {/* 页面标题 */}
        <div>
          <h1 className="text-3xl font-bold gradient-text mb-2">个人设置</h1>
          <p className="text-muted-foreground">管理您的账户信息和偏好设置</p>
        </div>

        <div className="grid gap-6 lg:grid-cols-3">
          {/* 左侧：个人信息 */}
          <div className="lg:col-span-2 space-y-6">
            {/* 基本信息 */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <User className="w-5 h-5" />
                  基本信息
                </CardTitle>
                <CardDescription>您的账户基本信息</CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleUpdateProfile} className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="username">用户名</Label>
                    <Input
                      id="username"
                      value={profile?.username || ''}
                      disabled
                      className="bg-muted"
                    />
                    <p className="text-xs text-muted-foreground">用户名不可修改</p>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="email">邮箱</Label>
                    <Input
                      id="email"
                      type="email"
                      value={profile?.email || `${profile?.username}@miaoda.com`}
                      disabled
                      className="bg-muted"
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="role">角色</Label>
                    <Input
                      id="role"
                      value={profile?.role === 'admin' ? '管理员' : '普通用户'}
                      disabled
                      className="bg-muted"
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="created_at">注册时间</Label>
                    <Input
                      id="created_at"
                      value={
                        profile?.created_at
                          ? format(new Date(profile.created_at), 'PPP', { locale: zhCN })
                          : ''
                      }
                      disabled
                      className="bg-muted"
                    />
                  </div>
                </form>
              </CardContent>
            </Card>

            {/* 密码修改 */}
            <Card>
              <CardHeader>
                <CardTitle>密码修改</CardTitle>
                <CardDescription>修改您的登录密码</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="current_password">当前密码</Label>
                    <Input id="current_password" type="password" disabled />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="new_password">新密码</Label>
                    <Input id="new_password" type="password" disabled />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="confirm_password">确认新密码</Label>
                    <Input id="confirm_password" type="password" disabled />
                  </div>

                  <Button disabled>
                    功能开发中
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* 右侧：统计信息 */}
          <div className="space-y-6">
            {/* 积分统计 */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Coins className="w-5 h-5" />
                  积分统计
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-center py-6">
                  <div className="text-4xl font-bold gradient-text mb-2">
                    {profile?.total_points || 0}
                  </div>
                  <p className="text-sm text-muted-foreground">总积分</p>
                </div>
                <Separator className="my-4" />
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">今日获得</span>
                    <span className="font-medium">0</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">本周获得</span>
                    <span className="font-medium">0</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">本月获得</span>
                    <span className="font-medium">0</span>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* 成就徽章 */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Award className="w-5 h-5" />
                  成就徽章
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-center py-6">
                  <div className="w-16 h-16 rounded-full bg-muted mx-auto mb-4 flex items-center justify-center">
                    <Award className="w-8 h-8 text-muted-foreground" />
                  </div>
                  <p className="text-sm text-muted-foreground">暂无成就徽章</p>
                  <p className="text-xs text-muted-foreground mt-1">完成更多任务解锁徽章</p>
                </div>
              </CardContent>
            </Card>

            {/* 活跃天数 */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Calendar className="w-5 h-5" />
                  活跃统计
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <div className="text-2xl font-bold mb-1">0 天</div>
                    <p className="text-sm text-muted-foreground">连续活跃天数</p>
                  </div>
                  <Separator />
                  <div>
                    <div className="text-2xl font-bold mb-1">
                      {profile?.created_at
                        ? Math.floor(
                            (Date.now() - new Date(profile.created_at).getTime()) /
                              (1000 * 60 * 60 * 24)
                          )
                        : 0}{' '}
                      天
                    </div>
                    <p className="text-sm text-muted-foreground">累计使用天数</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </MainLayout>
  );
}
