import DashboardPage from './pages/DashboardPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import LeaderboardPage from './pages/LeaderboardPage';
import CriteriaPage from './pages/CriteriaPage';
import SettingsPage from './pages/SettingsPage';
import NotFound from './pages/NotFound';
import type { ReactNode } from 'react';

interface RouteConfig {
  name: string;
  path: string;
  element: ReactNode;
  visible?: boolean;
}

const routes: RouteConfig[] = [
  {
    name: '仪表板',
    path: '/',
    element: <DashboardPage />,
    visible: true
  },
  {
    name: '排行榜',
    path: '/leaderboard',
    element: <LeaderboardPage />,
    visible: true
  },
  {
    name: '评分标准',
    path: '/criteria',
    element: <CriteriaPage />,
    visible: true
  },
  {
    name: '设置',
    path: '/settings',
    element: <SettingsPage />,
    visible: true
  },
  {
    name: '登录',
    path: '/login',
    element: <LoginPage />,
    visible: false
  },
  {
    name: '注册',
    path: '/register',
    element: <RegisterPage />,
    visible: false
  },
  {
    name: '404',
    path: '/404',
    element: <NotFound />,
    visible: false
  }
];

export default routes;
