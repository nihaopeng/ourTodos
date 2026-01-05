# 欢迎使用你的秒哒应用代码包
秒哒应用链接
    URL:https://www.miaoda.cn/projects/app-8k6eb6g4b1fl

## 介绍

待办事项评分管理软件 - 一款智能待办事项管理应用，通过AI评分机制和积分激励系统，提升任务管理效率与完成动力。

### 核心功能

- 🎯 **智能AI评分**：基于OpenAI API的智能评分系统，自动评估待办事项的价值
- 💰 **积分激励系统**：完成待办获得积分，提前完成额外奖励，延期完成适当惩罚
- 🏆 **排行榜系统**：总榜、月榜、周榜，激励用户持续完成任务
- ⚙️ **自定义评分标准**：根据个人需求调整AI评分权重（重要性、紧急性、复杂性、影响力）
- 📊 **数据统计**：完整的任务统计和积分趋势分析
- 🎨 **现代化UI**：基于shadcn/ui的精美界面，支持深色模式，配备精美图标系统
- 📱 **响应式设计**：完美适配桌面端和移动端

### 设计亮点

- **精美图标系统**：
  - ✅⭐ **应用Logo**：勾选+星星组合，象征任务完成与价值评估
  - 🧠⭐ **AI评分图标**：大脑+星星，代表智能评分系统
  - 💰 **积分图标**：金币堆叠，展现激励机制
  - 👑🏆 **排行榜图标**：皇冠+领奖台，激发竞争动力
- **现代配色方案**：科技蓝主色 + 活力橙辅助色 + 成功绿点缀色
- **轻拟物化设计**：界面清爽美观，视觉层次分明

### 技术特点

- 用户认证系统（注册、登录、权限管理）
- 待办事项CRUD操作
- AI智能评分（可配置评分标准）
- 实时积分计算和历史记录
- 多维度排行榜展示
- 完整的RLS安全策略

## 目录结构

```
├── README.md # 说明文档
├── components.json # 组件库配置
├── index.html # 入口文件
├── package.json # 包管理
├── postcss.config.js # postcss 配置
├── public # 静态资源目录
│   ├── favicon.png # 图标
│   └── images # 图片资源
├── src # 源码目录
│   ├── App.tsx # 入口文件
│   ├── components # 组件目录
│   ├── contexts # 上下文目录
│   ├── db # 数据库配置目录
│   ├── hooks # 通用钩子函数目录
│   ├── index.css # 全局样式
│   ├── layout # 布局目录
│   ├── lib # 工具库目录
│   ├── main.tsx # 入口文件
│   ├── routes.tsx # 路由配置
│   ├── pages # 页面目录
│   ├── services  # 数据库交互目录
│   ├── types   # 类型定义目录
├── tsconfig.app.json  # ts 前端配置文件
├── tsconfig.json # ts 配置文件
├── tsconfig.node.json # ts node端配置文件
└── vite.config.ts # vite 配置文件
```

## 技术栈

- **前端框架**：React 18 + TypeScript + Vite
- **UI组件库**：shadcn/ui + Tailwind CSS
- **后端服务**：Supabase (PostgreSQL + Auth + Edge Functions)
- **AI服务**：OpenAI API (GPT-3.5-turbo)
- **状态管理**：React Context + Hooks
- **路由管理**：React Router v6
- **日期处理**：date-fns
- **表单验证**：React Hook Form (可选)

## 环境配置

### 前置要求

- Node.js >= 20.x
- npm >= 10.x
- Supabase账户（用于数据库和认证）
- OpenAI API Key（用于AI评分功能）

### 环境变量

在项目根目录创建 `.env` 文件（已自动生成）：

```env
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

在Supabase项目中配置Edge Function环境变量：

```
OPENAI_API_KEY=your_openai_api_key
```

### 数据库配置

数据库表结构已通过Supabase Migration自动创建，包括：

- `profiles` - 用户信息表
- `todos` - 待办事项表
- `groups` - 分组表
- `scoring_criteria` - 评分标准表
- `points_history` - 积分历史表
- `monthly_rankings` - 月度排行榜表

所有表都已配置RLS（Row Level Security）策略，确保数据安全。

## 本地开发

### 快速开始

```bash
# 1. 安装依赖
npm install

# 2. 启动开发服务器
npm run dev

# 3. 在浏览器中打开
# http://localhost:5173
```

### 开发命令

```bash
# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 预览生产版本
npm run preview

# 代码检查和格式化
npm run lint
```

### 首次使用

1. **注册账户**：首次访问应用时，点击"立即注册"创建账户
2. **管理员权限**：第一个注册的用户将自动获得管理员权限
3. **配置OpenAI API**：在Supabase项目设置中添加 `OPENAI_API_KEY` 环境变量
4. **创建待办**：登录后即可开始创建待办事项并获得AI评分
5. **获得积分**：完成待办事项后自动获得积分奖励

### 功能说明

#### 1. 待办事项管理

- 创建待办：填写标题、描述、截止时间、优先级和分组
- AI评分：系统自动根据评分标准进行智能评分
- 编辑待办：修改待办信息并重新评分
- 完成待办：标记完成并获得积分
- 删除待办：删除不需要的待办事项

#### 2. 积分系统

- 基础积分：完成待办获得对应评分的积分
- 提前完成：获得1.1倍积分奖励
- 延期完成：获得0.8倍积分惩罚
- 积分历史：查看所有积分变动记录

#### 3. 排行榜

- 总榜：显示所有用户的总积分排名
- 月榜：显示本月积分排名
- 周榜：显示本周积分排名
- 前三名特殊展示，突出优秀用户

#### 4. 评分标准管理

- 自定义标准：创建多个评分标准
- 权重调整：调整重要性、紧急性、复杂性、影响力的权重
- 默认标准：设置默认使用的评分标准
- 标准切换：为不同类型的待办使用不同标准

### 如何在本地编辑代码？

您可以选择 [VSCode](https://code.visualstudio.com/Download) 或者您常用的任何 IDE 编辑器，唯一的要求是安装 Node.js 和 npm.

### 环境要求

```
# Node.js ≥ 20
# npm ≥ 10
例如：
# node -v   # v20.18.3
# npm -v    # 10.8.2
```

具体安装步骤如下：

### 在 Windows 上安装 Node.js

```
# Step 1: 访问Node.js官网：https://nodejs.org/，点击下载后，会根据你的系统自动选择合适的版本（32位或64位）。
# Step 2: 运行安装程序：下载完成后，双击运行安装程序。
# Step 3: 完成安装：按照安装向导完成安装过程。
# Step 4: 验证安装：在命令提示符（cmd）或IDE终端（terminal）中输入 node -v 和 npm -v 来检查 Node.js 和 npm 是否正确安装。
```

### 在 macOS 上安装 Node.js

```
# Step 1: 使用Homebrew安装（推荐方法）：打开终端。输入命令brew install node并回车。如果尚未安装Homebrew，需要先安装Homebrew，
可以通过在终端中运行如下命令来安装：
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
或者使用官网安装程序：访问Node.js官网。下载macOS的.pkg安装包。打开下载的.pkg文件，按照提示完成安装。
# Step 2: 验证安装：在命令提示符（cmd）或IDE终端（terminal）中输入 node -v 和 npm -v 来检查 Node.js 和 npm 是否正确安装。
```

### 安装完后按照如下步骤操作：

```
# Step 1: 下载代码包
# Step 2: 解压代码包
# Step 3: 用IDE打开代码包，进入代码目录
# Step 4: IDE终端输入命令行，安装依赖：npm i
# Step 5: IDE终端输入命令行，启动开发服务器：npm run dev -- --host 127.0.0.1
```

### 如何开发后端服务？

配置环境变量，安装相关依赖
如需使用数据库，请使用 supabase 官方版本或自行部署开源版本的 Supabase

### 如何配置应用中的三方 API？

#### OpenAI API 配置

AI评分功能需要配置OpenAI API Key：

1. 访问 [OpenAI Platform](https://platform.openai.com/) 并注册账户
2. 在API Keys页面创建新的API Key
3. 在Supabase项目中配置环境变量：
   - 进入Supabase项目控制台
   - 导航到 Settings > Edge Functions
   - 添加环境变量：`OPENAI_API_KEY=your_api_key`
4. 重新部署Edge Function（如果已部署）

**注意**：如果未配置OpenAI API Key，系统将使用默认评分（50分），不会影响其他功能的正常使用。

#### Supabase 配置

1. 访问 [Supabase](https://supabase.com/) 并创建项目
2. 获取项目的 URL 和 anon key
3. 在项目根目录的 `.env` 文件中配置：
   ```env
   VITE_SUPABASE_URL=your_project_url
   VITE_SUPABASE_ANON_KEY=your_anon_key
   ```
4. 数据库表结构已自动创建，无需手动配置

## 部署

### Vercel 部署

```bash
# 1. 安装 Vercel CLI
npm i -g vercel

# 2. 登录 Vercel
vercel login

# 3. 部署项目
vercel

# 4. 配置环境变量
# 在 Vercel 项目设置中添加环境变量
```

### Netlify 部署

```bash
# 1. 安装 Netlify CLI
npm i -g netlify-cli

# 2. 登录 Netlify
netlify login

# 3. 部署项目
netlify deploy --prod

# 4. 配置环境变量
# 在 Netlify 项目设置中添加环境变量
```

## 常见问题

### Q: AI评分不工作怎么办？

A: 请检查以下几点：
1. 确认已在Supabase中配置 `OPENAI_API_KEY` 环境变量
2. 确认OpenAI API Key有效且有足够的额度
3. 查看浏览器控制台和Supabase Edge Function日志
4. 如果API不可用，系统会自动使用默认评分（50分）

### Q: 第一个用户如何成为管理员？

A: 第一个注册的用户会自动获得管理员权限，这是通过数据库触发器实现的。后续注册的用户默认为普通用户。

### Q: 管理员和普通用户有什么区别？

A: 
- **管理员**：可以创建、编辑、删除评分标准，管理系统配置
- **普通用户**：只能查看评分标准（只读），无法修改
- 所有用户都可以创建和管理自己的待办事项

### Q: 如何修改评分标准？

A: 只有管理员可以修改评分标准。登录后访问"评分标准"页面，可以创建新的评分标准或编辑现有标准。调整重要性、紧急性、复杂性、影响力的权重，确保总和为100%。普通用户只能查看评分标准。

### Q: 积分如何计算？

A: 
- 基础积分 = 待办事项的AI评分
- 提前完成 = 基础积分 × 1.1
- 延期完成 = 基础积分 × 0.8
- 删除未完成的待办不会获得积分

## 项目结构说明

```
src/
├── components/          # 组件目录
│   ├── layouts/        # 布局组件
│   ├── ui/             # UI基础组件（shadcn/ui）
│   ├── TodoCard.tsx    # 待办卡片组件
│   ├── AddTodoDialog.tsx    # 添加待办对话框
│   ├── EditTodoDialog.tsx   # 编辑待办对话框
│   └── ...
├── contexts/           # React Context
│   └── AuthContext.tsx # 认证上下文
├── db/                 # 数据库相关
│   ├── supabase.ts    # Supabase客户端
│   └── api.ts         # API封装
├── hooks/              # 自定义Hooks
├── pages/              # 页面组件
│   ├── DashboardPage.tsx    # 仪表板
│   ├── LeaderboardPage.tsx  # 排行榜
│   ├── CriteriaPage.tsx     # 评分标准
│   ├── SettingsPage.tsx     # 设置
│   ├── LoginPage.tsx        # 登录
│   └── RegisterPage.tsx     # 注册
├── types/              # TypeScript类型定义
│   └── types.ts
├── App.tsx             # 应用入口
├── routes.tsx          # 路由配置
└── index.css           # 全局样式

supabase/
└── functions/          # Edge Functions
    └── score-todo/     # AI评分函数
        └── index.ts
```

## 贡献指南

欢迎提交Issue和Pull Request！

## 许可证

MIT License

## 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 Issue
- 发送邮件
- 访问帮助文档

具体三方 API 调用方法，请参考帮助文档：[源码导出](https://cloud.baidu.com/doc/MIAODA/s/Xmewgmsq7)，了解更多详细内容。

## 了解更多

您也可以查看帮助文档：[源码导出](https://cloud.baidu.com/doc/MIAODA/s/Xmewgmsq7)，了解更多详细内容。
