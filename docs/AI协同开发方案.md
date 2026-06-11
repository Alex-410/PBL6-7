# 校园活动发布平台 - AI协同开发方案

## 快速启动

### 环境要求

| 工具 | 版本 |
|------|------|
| Node.js | >= 18 |
| Java | 17 |
| Maven | 3.9+ |
| MySQL | 8.0+ |

### 数据库配置

数据库连接使用环境变量参数，启动前请确保已设置以下环境变量：

| 环境变量 | 说明 | 默认值 |
|---------|------|--------|
| `DB_USERNAME` | 数据库用户名 | `root` |
| `DB_PASSWORD` | 数据库密码 | 空 |

在 PowerShell 中设置环境变量：

```powershell
# 设置数据库用户名和密码
$env:DB_USERNAME="root"
$env:DB_PASSWORD="your_password"
```

后端 `application.yml` 中已配置读取这两个环境变量：

```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/pbl6?useUnicode=true&characterEncoding=utf-8&useSSL=false&serverTimezone=Asia/Shanghai&allowPublicKeyRetrieval=true
    username: ${DB_USERNAME:root}
    password: ${DB_PASSWORD:}
```

### 启动步骤

#### 1. 初始化数据库

执行 `backend/src/main/resources/db/schema.sql` 创建数据库和表结构，或导入 `pbl6.sql` 获取完整演示数据。

#### 2. 启动后端

```powershell
cd backend
mvn spring-boot:run
```

后端默认运行在 http://localhost:8080。

#### 3. 启动前端

```powershell
cd frontend
npm install   # 首次启动需安装依赖
npm run dev
```

前端默认运行在 http://localhost:3000，已配置 API 代理将 `/api` 请求转发到后端。

---

## 1. 项目现状

### 1.1 已完成的功能

#### 前端（完整 Mock 实现）
- ✅ 项目初始化（Vue 3 + TypeScript + Vite）
- ✅ 认证页面（登录/注册，斜线分割布局，演示账号一键填入）
- ✅ **学生端**：
  - ✅ 活动广场（分类筛选、搜索、状态标签）
  - ✅ 我的活动（报名列表、签到状态、日历视图 FullCalendar）
  - ✅ 加分记录（加分列表、申诉功能）
  - ✅ 活动详情弹窗
  - ✅ 个人中心
- ✅ **管理员端**：
  - ✅ 平台概览仪表盘（统计卡片、分类占比、快捷审批）
  - ✅ 活动审批（通过/驳回）
  - ✅ 全部活动管理
  - ✅ 用户管理
  - ✅ 发布者管理
  - ✅ 数据报表
- ✅ **发布者端**：
  - ✅ 数据概览仪表盘
  - ✅ 活动管理 / 发布新活动
  - ✅ 报名数据查看
- ✅ Mock 数据系统（15+ 活动、多角色用户、报名记录、通知）
- ✅ 自定义设计系统（"集趣"品牌、莫兰迪色系、衬线/等宽字体、噪点纹理）

#### 后端
- ✅ 项目初始化（Spring Boot 3.2.4 + Java 17 + Maven）
- ✅ 注册登录接口（支持普通账号 + 学号自动登录）
- ✅ JWT 认证（jjwt 0.12.3）
- ✅ 统一异常处理（GlobalExceptionHandler）
- ✅ 统一响应封装（Result 类）
- ✅ 密码加密（BCryptPasswordEncoder）
- ✅ CORS 跨域配置
- ✅ 数据库设计：user 表、student 表、activity 表、notification 表、audit_settings 表
- ✅ 学生数据导入（3 条演示数据）

### 1.2 当前技术栈

| 分类 | 技术 | 版本 | 状态 |
|------|------|------|------|
| **前端** | Vue 3 | 3.4.x | ✅ 已配置 |
| | TypeScript | 5.x | ✅ 已配置 |
| | Vite | 5.2.x | ✅ 已配置 |
| | Vue Router | 4.x | ✅ 已配置 |
| | Pinia | 2.x | ✅ 已配置 |
| | Element Plus | 2.6.x | ✅ 已配置（未实际使用） |
| | Axios | 1.6.x | ✅ 已配置 |
| | SCSS（sass） | 1.75.x | ✅ 已配置 |
| | FullCalendar | 6.1.x | ✅ 已配置 |
| **后端** | Java | 17 | ✅ 已配置 |
| | Spring Boot | 3.2.4 | ✅ 已配置 |
| | Spring Security | 最新 | ✅ 已配置 |
| | MyBatis | 3.0.3 | ✅ 已配置 |
| | MySQL | 8.0.x | ✅ 已配置 |
| | JWT（jjwt） | 0.12.3 | ✅ 已配置 |
| | Lombok | 最新 | ✅ 已配置 |
| | Maven | 3.9.x | ✅ 已配置 |

### 1.3 待开发功能

- **后端业务接口**：
  - ❌ 活动 CRUD 接口（发布、编辑、删除、列表、详情）
  - ❌ 活动审核接口（通过/驳回）
  - ❌ 报名接口（报名、取消报名、签到）
  - ❌ 加分管理接口（上传加分名单、确认、申诉）
  - ❌ 通知接口
  - ❌ JWT 拦截过滤器（JwtAuthenticationFilter）
- **前后端联调**：
  - ❌ 将前端 Mock 数据切换为真实 API 调用
  - ❌ 全链路集成测试
- **部署**：
  - ❌ Docker 化部署
  - ❌ CI/CD 配置

## 2. 开发分工建议

### 2.1 功能模块分配

| 模块 | 开发者A | 开发者B |
|------|---------|---------|
| **用户认证** | 前后端（已完成） | — |
| **活动管理** | 后端接口 | 前端联调 |
| - 活动发布/编辑/删除 | ✅ 后端 | ✅ 前端 |
| - 活动列表/详情 | ✅ 后端 | ✅ 前端 |
| - 活动搜索/筛选 | — | ✅ 前端（Mock 已实现） |
| **活动审核** | 后端接口 | 前端联调 |
| - 审核通过/驳回 | ✅ 后端 | ✅ 前端（Mock 已实现） |
| **报名管理** | 后端接口 | 前端联调 |
| - 报名/取消报名 | ✅ 后端 | ✅ 前端（Mock 已实现） |
| - 签到管理 | ✅ 后端 | ✅ 前端（Mock 已实现） |
| **加分管理** | 后端接口 | 前端联调 |
| - 加分名单上传 | ✅ 后端 | ✅ 前端（Mock 已实现） |
| - 加分确认/申诉 | ✅ 后端 | ✅ 前端（Mock 已实现） |
| **通知中心** | 后端接口 | 前端联调 |
| - 通知推送/列表 | ✅ 后端 | ✅ 前端（Mock 已实现） |
| **管理后台** | 后端接口 | 前端联调 |
| - 用户管理 | ✅ 后端 | ✅ 前端（Mock 已实现） |
| - 数据报表 | ✅ 后端 | ✅ 前端（Mock 已实现） |

### 2.2 技术职责分配

| 职责 | 开发者A | 开发者B |
|------|---------|---------|
| **前端** | ❌ | ✅ |
| - 页面开发（已完成） | ❌ | ✅ |
| - 样式优化（已完成） | ❌ | ✅ |
| - Mock 数据（已完成） | ❌ | ✅ |
| - API 联调 | ❌ | ✅ |
| **后端** | ✅ | ❌ |
| - 接口开发（待完成） | ✅ | ❌ |
| - 数据库设计 | ✅ | ❌ |
| - 安全认证 | ✅ | ❌ |
| **全栈** | ✅ | ✅ |
| - 集成测试 | ✅ | ✅ |
| - 部署配置 | ✅ | ✅ |
| - 代码审查 | ✅ | ✅ |

## 3. 技术规范

### 3.1 代码规范

#### 前端规范
- **命名规范**：
  - 组件名：PascalCase（如 `StudentDashboard.vue`）
  - 变量名：camelCase（如 `loginForm`）
  - 常量：UPPER_SNAKE_CASE（如 `API_BASE_URL`）
- **文件结构**：按功能模块组织在 `components/` 目录下
- **代码风格**：使用 Vue 3 `<script setup lang="ts">` 组合式 API
- **路由策略**：集中式路由（`router/index.ts`），通过 `DashboardView.vue` 动态切换组件
- **状态管理**：Pinia（已安装，目前使用组件本地状态 + 全局 Mock 数据）

#### 后端规范
- **命名规范**：
  - 类名：PascalCase（如 `AuthController`）
  - 方法名：camelCase（如 `register`）
  - 变量名：camelCase（如 `userService`）
- **包结构**：按分层架构组织（controller → service → mapper）
- **代码风格**：遵循阿里巴巴 Java 开发手册
- **ORM**：使用 MyBatis + 注解式 SQL（`@Select`、`@Insert` 等）

### 3.2 目录结构规范

```
trae/
├── frontend/                    # 前端项目
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── src/
│   │   ├── main.ts              # 入口文件
│   │   ├── App.vue              # 根组件
│   │   ├── styles/
│   │   │   └── global.scss      # 全局样式（设计系统）
│   │   ├── router/
│   │   │   └── index.ts         # 路由配置
│   │   ├── services/
│   │   │   └── api.ts           # API 服务 + 请求拦截器
│   │   ├── mock/
│   │   │   └── data.ts          # Mock 数据（用户/活动/报名/通知）
│   │   ├── views/
│   │   │   ├── AuthView.vue     # 登录/注册页面
│   │   │   └── DashboardView.vue# 主布局（侧边栏 + 动态组件）
│   │   └── components/
│   │       ├── StudentDashboard.vue    # 学生 - 活动广场
│   │       ├── StudentActivities.vue   # 学生 - 我的活动
│   │       ├── StudentCalendar.vue     # 学生 - 日历视图
│   │       ├── StudentBonus.vue        # 学生 - 加分记录
│   │       ├── ActivityDetail.vue      # 活动详情弹窗
│   │       ├── ProfileView.vue         # 个人中心
│   │       ├── AdminDashboard.vue      # 管理员 - 平台概览
│   │       ├── AdminApprovals.vue      # 管理员 - 活动审批
│   │       ├── AdminAllActivities.vue  # 管理员 - 全部活动
│   │       ├── AdminUserManage.vue     # 管理员 - 用户管理
│   │       ├── AdminPublishers.vue     # 管理员 - 发布者管理
│   │       ├── AdminReports.vue        # 管理员 - 数据报表
│   │       └── PublisherDashboard.vue  # 发布者 - 控制台
│   └── public/
├── backend/                     # 后端项目
│   ├── pom.xml
│   ├── src/main/java/com/campus/activity/
│   │   ├── Application.java           # 启动类
│   │   ├── common/
│   │   │   └── Result.java            # 统一响应封装
│   │   ├── config/
│   │   │   └── SecurityConfig.java    # Spring Security 配置
│   │   ├── controller/
│   │   │   └── AuthController.java    # 认证控制器
│   │   ├── dto/
│   │   │   ├── LoginDTO.java          # 登录请求
│   │   │   └── RegisterDTO.java       # 注册请求
│   │   ├── entity/
│   │   │   ├── User.java              # 用户实体
│   │   │   └── Student.java           # 学生实体
│   │   ├── exception/
│   │   │   └── GlobalExceptionHandler.java  # 统一异常处理
│   │   ├── mapper/
│   │   │   ├── UserMapper.java        # 用户数据访问
│   │   │   └── StudentMapper.java     # 学生数据访问
│   │   ├── service/
│   │   │   └── AuthService.java       # 认证服务
│   │   ├── utils/
│   │   │   └── JwtUtil.java           # JWT 工具类
│   │   └── vo/
│   │       └── UserVO.java            # 用户视图对象
│   └── src/main/resources/
│       ├── application.yml             # 应用配置
│       └── db/
│           └── schema.sql              # 数据库建表脚本
└── docs/                        # 文档目录
    ├── README.md
    ├── 需求分析文档.md
    ├── 前端架构设计.md
    ├── 后端架构设计.md
    ├── 项目目录结构.md
    ├── 校园活动发布平台需求文档.md
    └── AI协同开发方案.md
```

### 3.3 API 规范

- **接口路径**：`/api/{模块}/{功能}`
- **HTTP方法**：
  - GET：查询
  - POST：创建
  - PUT：更新
  - DELETE：删除
- **响应格式**：
  ```json
  {
    "code": 200,
    "message": "success",
    "data": {}
  }
  ```
- **错误处理**：统一异常处理，返回错误码和错误信息
- **认证方式**：JWT Bearer Token（请求头 `Authorization: Bearer <token>`）

### 3.4 数据库设计（现有表结构）

| 表名 | 说明 | 状态 |
|------|------|------|
| `user` | 用户表（含角色、状态） | ✅ 已建 |
| `student` | 学生信息表（关联 user） | ✅ 已建 |
| `activity` | 活动表（含审核信息、AI审核标记） | ✅ 已建 |
| `notification` | 通知表 | ✅ 已建 |
| `audit_settings` | 审核设置表 | ✅ 已建 |

## 4. 开发流程

### 4.1 分支管理

- **main**：主分支，用于发布
- **develop**：开发分支，集成所有功能
- **feature/{模块}**：功能分支，如 `feature/activity-api`
- **bugfix/{问题}**：bug修复分支

### 4.2 下一阶段开发步骤（优先级排序）

1. **后端 JWT 拦截过滤器** — 实现 `JwtAuthenticationFilter`，保护需要认证的接口
2. **活动 CRUD 接口** — 活动的发布、编辑、删除、列表、详情
3. **活动审核接口** — 管理员的通过/驳回操作
4. **报名接口** — 报名、取消报名、签到、我的报名列表
5. **加分管理接口** — 加分名单上传、确认、申诉、记录查询
6. **通知接口** — 通知列表、标记已读
7. **前后端联调** — 将前端 Mock 数据切换为真实 API 调用
8. **集成测试** — 全链路测试
9. **部署** — Docker + CI/CD

### 4.3 协同工具

- **代码仓库**：GitHub
- **任务管理**：GitHub Issues
- **代码审查**：GitHub Pull Requests
- **沟通工具**：根据团队偏好选择

## 5. 代码管理

### 5.1 Git 提交规范

使用 Conventional Commits 规范：

- **feat**：新功能
- **fix**：修复bug
- **docs**：文档更新
- **style**：代码格式调整
- **refactor**：重构
- **test**：测试相关
- **chore**：构建/工具相关

### 5.2 代码审查

- **Pull Request**：每个功能分支必须通过代码审查
- **审查要点**：
  - 代码质量
  - 安全性
  - 性能
  - 可读性
  - 测试覆盖
