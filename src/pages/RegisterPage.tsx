import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { useToast } from '@/hooks/use-toast';
import { Loader2, KeyRound, User } from 'lucide-react';

export default function RegisterPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const { signUp, signIn } = useAuth();
  const navigate = useNavigate();
  const { toast } = useToast();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!username || !password || !confirmPassword) {
      toast({
        title: '错误',
        description: '请填写所有字段',
        variant: 'destructive',
      });
      return;
    }

    // 验证用户名格式
    if (!/^[a-zA-Z0-9_]+$/.test(username)) {
      toast({
        title: '错误',
        description: '用户名只能包含字母、数字和下划线',
        variant: 'destructive',
      });
      return;
    }

    // 验证用户名长度
    if (username.length < 3 || username.length > 20) {
      toast({
        title: '错误',
        description: '用户名长度必须在3-20个字符之间',
        variant: 'destructive',
      });
      return;
    }

    // 验证密码长度
    if (password.length < 6) {
      toast({
        title: '错误',
        description: '密码长度至少为6个字符',
        variant: 'destructive',
      });
      return;
    }

    if (password !== confirmPassword) {
      toast({
        title: '错误',
        description: '两次输入的密码不一致',
        variant: 'destructive',
      });
      return;
    }

    setLoading(true);
    const { error } = await signUp(username, password);

    if (error) {
      setLoading(false);
      toast({
        title: '注册失败',
        description: error.message || '注册过程中出现错误',
        variant: 'destructive',
      });
      return;
    }

    // 注册成功后自动登录
    const { error: signInError } = await signIn(username, password);
    setLoading(false);

    if (signInError) {
      toast({
        title: '注册成功',
        description: '请登录您的账户',
      });
      navigate('/login');
    } else {
      toast({
        title: '注册成功',
        description: '欢迎加入！',
      });
      navigate('/');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-background p-4">
      <Card className="w-full max-w-md shadow-primary">
        <CardHeader className="space-y-1">
          <div className="flex items-center justify-center mb-4">
            <div className="w-16 h-16 rounded-full gradient-primary flex items-center justify-center">
              <span className="text-4xl">✓⭐</span>
            </div>
          </div>
          <CardTitle className="text-2xl text-center gradient-text">创建新账户</CardTitle>
          <CardDescription className="text-center">
            注册以开始使用待办事项评分管理
          </CardDescription>
        </CardHeader>
        <form onSubmit={handleSubmit}>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="username" className="flex items-center gap-2">
                <User className="w-4 h-4" />
                用户名
              </Label>
              <Input
                id="username"
                type="text"
                placeholder="请输入用户名（3-20个字符）"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                disabled={loading}
                autoComplete="username"
              />
              <p className="text-xs text-muted-foreground">
                只能包含字母、数字和下划线
              </p>
            </div>
            <div className="space-y-2">
              <Label htmlFor="password" className="flex items-center gap-2">
                <KeyRound className="w-4 h-4" />
                密码
              </Label>
              <Input
                id="password"
                type="password"
                placeholder="请输入密码（至少6个字符）"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                disabled={loading}
                autoComplete="new-password"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="confirmPassword" className="flex items-center gap-2">
                <KeyRound className="w-4 h-4" />
                确认密码
              </Label>
              <Input
                id="confirmPassword"
                type="password"
                placeholder="请再次输入密码"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                disabled={loading}
                autoComplete="new-password"
              />
            </div>
          </CardContent>
          <CardFooter className="flex flex-col space-y-4">
            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  注册中...
                </>
              ) : (
                '注册'
              )}
            </Button>
            <div className="text-sm text-center text-muted-foreground">
              已有账户？{' '}
              <Link to="/login" className="text-primary hover:underline">
                立即登录
              </Link>
            </div>
          </CardFooter>
        </form>
      </Card>
    </div>
  );
}
