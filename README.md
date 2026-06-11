# 集趣 - 校园活动发布平台

一站式校园活动管理平台，支持活动发布、报名、AI 智能推荐，并内置基于 RAG 的校规知识库问答系统。

## 功能特性

### 学生端
- **活动广场** - 浏览、搜索、筛选校园活动，支持按类别/标签/院系过滤
- **活动报名** - 一键报名/取消，实时查看报名状态和名额
- **日历视图** - 按日期查看活动安排
- **AI 智能推荐** - 基于豆包大模型，根据活动信息智能推荐
- **AI 聊天助手** - 支持豆包/DeepSeek/GLM 等多种大模型对话
- **加分记录** - 查看志愿时长、实践学分等加分统计
- **个人中心** - 管理个人信息和兴趣标签

### 发布者端
- **数据概览** - 查看活动统计、报名趋势
- **发布活动** - 创建活动（支持加分类型、报名限制等配置）
- **活动管理** - 管理已发布活动
- **报名管理** - 查看各活动的报名情况

### 管理员端
- **平台概览** - 全站数据统计
- **活动审批** - 审核发布者提交的活动
- **全部活动** - 查看和管理所有活动
- **用户管理** - 管理用户角色和权限
- **发布者管理** - 管理发布者账号
- **数据报表** - 活动分布、报名排行、关键指标

### 校规知识库 (RAG)
- **智能问答** - 基于 98 条校规的 RAG 检索增强生成
- **对话管理** - 新建/删除对话，删除单条消息
- **知识库管理** - 上传文档、查看切片、删除文档
- **多策略分片** - 支持固定长度/递归分割/结构化分割

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue 3 + TypeScript + Vite + Element Plus + SCSS |
| 后端 | Java 17 + Spring Boot 3.2 + Spring Security + MyBatis-Plus + JWT |
| 数据库 | MySQL 8.0 |
| RAG 系统 | Python Flask + FAISS + Ollama (Embedding) + DeepSeek API (LLM) |
| AI 推荐 | 豆包大模型 API |

## 项目结构

```
校园活动发布平台/
├── frontend/           # 前端 (Vue 3)
│   ├── src/
│   │   ├── views/      # 页面组件
│   │   ├── components/ # 功能组件
│   │   ├── router/     # 路由配置
│   │   ├── services/   # API 服务
│   │   └── styles/     # 全局样式
│   └── package.json
├── backend/            # 后端 (Spring Boot)
│   ├── src/main/java/com/campus/activity/
│   │   ├── controller/ # REST 控制器
│   │   ├── service/    # 业务逻辑
│   │   ├── entity/     # 数据实体
│   │   ├── mapper/     # MyBatis 映射
│   │   ├── config/     # 安全/JWT 配置
│   │   └── dto/        # 数据传输对象
│   └── pom.xml
├── campus-rag/         # RAG 知识库系统
│   ├── main.py         # Flask 服务端
│   ├── rag_data/       # 校规原始文档
│   └── vector_db/      # 预置向量数据库
├── test/               # 自动化测试
└── docs/               # 设计文档
```

## 快速启动

### 1. 后端服务

```bash
# 创建数据库
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS pbl6"

# 导入表结构
mysql -u root -p pbl6 < backend/src/main/resources/db/schema.sql

# 启动后端
cd backend
mvn spring-boot:run
```

后端运行在 http://localhost:8080

### 2. 前端服务

```bash
cd frontend
npm install
npm run dev
```

前端运行在 http://localhost:5173

### 3. RAG 知识库（可选）

```bash
# 安装 Ollama 并拉取模型
ollama pull qwen3-embedding:0.6b

# 启动 RAG 服务
cd campus-rag
pip install -r requirements.txt
python main.py
```

RAG 服务运行在 http://localhost:9001

访问校规知识库：http://localhost:5173/school-rules

## 用户角色

| 角色 | 说明 | 默认账号 |
|------|------|----------|
| 学生 (USER) | 浏览活动、报名、查看加分 | 注册即获得 |
| 发布者 (PUBLISHER) | 发布和管理活动 | 管理员授予 |
| 学生发布者 (STUDENT_PUBLISHER) | 兼具学生和发布者权限 | 管理员授予 |
| 管理员 (ADMIN) | 完整管理权限 | 需手动创建 |

## 主要 API

### 认证
| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/auth/register` | POST | 用户注册 |
| `/api/auth/login` | POST | 用户登录 |

### 活动
| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/activities` | GET | 获取活动列表 |
| `/api/activities` | POST | 创建活动 |
| `/api/activities/{id}` | GET | 获取活动详情 |
| `/api/activities/{id}/audit` | PUT | 审核活动 |
| `/api/activities/{id}` | DELETE | 删除活动 |

### 报名
| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/registrations` | POST | 报名活动 |
| `/api/registrations/{id}` | DELETE | 取消报名 |
| `/api/registrations/me` | GET | 我的报名列表 |

### 用户管理
| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/users` | GET | 用户列表 (管理员) |
| `/api/users/{id}/status` | PUT | 启用/禁用用户 |
| `/api/users/{id}/role` | PUT | 修改用户角色 |

### RAG 知识库
| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/rag/chat/` | POST | 发送问题 |
| `/api/rag/status/` | GET | 知识库状态 |
| `/api/rag/upload/` | POST | 上传文档 |
| `/api/rag/conversations/` | GET/POST | 对话管理 |

## 安全特性

- JWT 令牌认证
- 基于角色的访问控制 (RBAC)
- 登录失败频率限制（5次/15分钟）
- XSS 输入转义
- SQL 注入防护（MyBatis 参数化查询）
- 禁用用户 Token 立即失效

## 开发

### Git 提交规范

```
feat: 新功能
fix: 修复 bug
docs: 文档更新
style: 代码格式调整
refactor: 重构
test: 测试相关
chore: 构建/工具相关
```

### 运行测试

```bash
cd test
python run_full_test.py
```

测试脚本会自动创建临时用户并生成 Excel 报告。

## 相关链接

- [项目仓库](https://github.com/Alex-410/PBL6-7)
- [DeepSeek API](https://platform.deepseek.com)
- [Ollama](https://ollama.ai)
