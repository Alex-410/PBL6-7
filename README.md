# 校园活动发布平台

## 项目简介

校园活动发布平台是一个为高校师生提供活动信息发布、浏览、管理的综合性平台。

## 技术栈

### 前端
- Vue 3 + TypeScript
- Vite
- Vue Router
- Pinia
- Element Plus
- Axios
- SCSS

### 后端
- Java 17
- Spring Boot 3.2.4
- Spring Security
- MyBatis-Plus
- MySQL 8.0
- JWT
- Maven

## 项目结构

```
校园活动发布平台/
├── frontend/          # 前端项目
├── backend/        # 后端项目
└── docs/           # 文档目录
```

## 快速开始

### 前端启动

```bash
cd frontend
npm install
npm run dev
```

### 后端启动

1. 创建数据库并执行 `backend/src/main/resources/db/schema.sql`
2. 修改 `application.yml` 中的数据库配置
3. 运行 `Application.java`

## 开发规范

### Git 提交规范

- feat: 新功能
- fix: 修复 bug
- docs: 文档更新
- style: 代码格式调整
- refactor: 重构
- test: 测试相关
- chore: 构建/工具相关

### 代码规范

- 前端：遵循 Vue 3 官方风格指南
- 后端：遵循阿里巴巴 Java 开发手册
