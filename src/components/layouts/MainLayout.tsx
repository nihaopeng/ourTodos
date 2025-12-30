import { useState, useEffect, ReactNode } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Separator } from '@/components/ui/separator';
import {
  LayoutDashboard,
  Trophy,
  Scale,
  Settings,
  LogOut,
  User,
  Menu,
  Coins,
  Folder,
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { getGroups } from '@/db/api';
import type { Group } from '@/types/types';

interface MainLayoutProps {
  children: ReactNode;
  onGroupSelect?: (groupId: string) => void;
  selectedGroupId?: string | null;
}

const navigation = [
  { name: '仪表板', href: '/', icon: LayoutDashboard },
  { name: '排行榜', href: '/leaderboard', icon: Trophy },
  { name: '评分标准', href: '/criteria', icon: Scale },
  { name: '设置', href: '/settings', icon: Settings },
];

export default function MainLayout({ children, onGroupSelect, selectedGroupId }: MainLayoutProps) {
  const { profile, signOut } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  const [groups, setGroups] = useState<Group[]>([]);

  useEffect(() => {
    if (profile?.id) {
      loadGroups();
    }
  }, [profile]);

  const loadGroups = async () => {
    if (!profile?.id) return;
    try {
      const data = await getGroups(profile.id);
      setGroups(data);
    } catch (error) {
      console.error('加载分组失败:', error);
    }
  };

  const handleSignOut = async () => {
    await signOut();
    navigate('/login');
  };

  const Sidebar = () => (
    <div className="flex flex-col h-full">
      <div className="p-6">
        <Link to="/" className="flex items-center gap-2">
          <div className="w-10 h-10 rounded-lg flex items-center justify-center">
            <img src="/images/score.png" alt="Logo" className="w-10 h-10" />
          </div>
          <div className="flex flex-col">
            <span className="font-bold text-lg gradient-text">待办评分</span>
            <span className="text-xs text-muted-foreground">智能任务管理</span>
          </div>
        </Link>
      </div>

      <Separator />

      <ScrollArea className="flex-1 px-3 py-4">
        <nav className="space-y-1">
          {navigation.map((item) => {
            const isActive = location.pathname === item.href;
            return (
              <Link
                key={item.name}
                to={item.href}
                className={cn(
                  'flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors',
                  isActive
                    ? 'bg-primary text-primary-foreground shadow-primary'
                    : 'text-muted-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground'
                )}
              >
                <item.icon className="w-5 h-5" />
                {item.name}
              </Link>
            );
          })}
        </nav>

        {/* 分组列表 - 仅在仪表板页面显示 */}
        {location.pathname === '/' && groups.length > 0 && (
          <>
            <Separator className="my-4" />
            <div className="px-3 py-2">
              <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2 flex items-center gap-2">
                <Folder className="w-4 h-4" />
                我的分组
              </h3>
              <div className="space-y-1">
                {groups.map((group) => (
                  <button
                    key={group.id}
                    onClick={() => onGroupSelect?.(group.id)}
                    className={cn(
                      'w-full flex items-center gap-2 px-3 py-2 rounded-lg text-sm transition-colors',
                      selectedGroupId === group.id
                        ? 'bg-primary/10 text-primary font-medium'
                        : 'text-muted-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground'
                    )}
                  >
                    <span
                      className="w-2 h-2 rounded-full shrink-0"
                      style={{ backgroundColor: group.color }}
                    />
                    <span className="flex-1 text-left truncate">{group.name}</span>
                  </button>
                ))}
              </div>
            </div>
          </>
        )}
      </ScrollArea>

      <Separator />

      <div className="p-4">
        <div className="flex items-center gap-3 p-3 rounded-lg bg-sidebar-accent">
          <div className="w-10 h-10 rounded-full bg-primary flex items-center justify-center text-primary-foreground font-bold">
            {profile?.username?.charAt(0).toUpperCase() || 'U'}
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium truncate">{profile?.username || '用户'}</p>
            <div className="flex items-center gap-1 text-xs text-muted-foreground">
              <img src="/images/coins.png" alt="积分" className="w-3 h-3" />
              <span>{profile?.total_points || 0} 积分</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="flex min-h-screen w-full">
      {/* 桌面端侧边栏 */}
      <aside className="hidden lg:block w-64 border-r border-sidebar-border bg-sidebar shrink-0">
        <Sidebar />
      </aside>

      {/* 主内容区 */}
      <div className="flex-1 flex flex-col">
        {/* 顶部导航栏 */}
        <header className="sticky top-0 z-40 border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
          <div className="flex h-16 items-center gap-4 px-4 lg:px-6">
            {/* 移动端菜单按钮 */}
            <Sheet>
              <SheetTrigger asChild>
                <Button variant="ghost" size="icon" className="lg:hidden">
                  <Menu className="h-5 w-5" />
                </Button>
              </SheetTrigger>
              <SheetContent side="left" className="w-64 p-0">
                <Sidebar />
              </SheetContent>
            </Sheet>

            {/* 标题 */}
            <div className="flex-1">
              <h1 className="text-lg font-semibold">
                {navigation.find((item) => item.href === location.pathname)?.name || '待办事项'}
              </h1>
            </div>

            {/* 积分显示 */}
            <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-full bg-primary/10 text-primary">
              <img src="/images/coins.png" alt="积分" className="w-5 h-5" />
              <span className="text-sm font-medium">{profile?.total_points || 0}</span>
            </div>

            {/* 用户菜单 */}
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="icon" className="rounded-full">
                  <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center text-primary-foreground font-bold text-sm">
                    {profile?.username?.charAt(0).toUpperCase() || 'U'}
                  </div>
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-56">
                <DropdownMenuLabel>
                  <div className="flex flex-col space-y-1">
                    <p className="text-sm font-medium">{profile?.username || '用户'}</p>
                    <p className="text-xs text-muted-foreground">
                      {profile?.email || `${profile?.username}@miaoda.com`}
                    </p>
                  </div>
                </DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuItem asChild>
                  <Link to="/settings" className="cursor-pointer">
                    <User className="mr-2 h-4 w-4" />
                    个人设置
                  </Link>
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={handleSignOut} className="cursor-pointer text-destructive">
                  <LogOut className="mr-2 h-4 w-4" />
                  退出登录
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </header>

        {/* 页面内容 */}
        <main className="flex-1 p-4 lg:p-6">
          {children}
        </main>
      </div>
    </div>
  );
}
