# 校园活动发布平台

## 项目简介

校园活动发布平台是一个为高校师生提供活动信息发布、浏览、管理的综合性平台，包含校规知识库 RAG 问答系统。

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

### RAG 知识库系统
- Python 3.10+
- Flask
- FAISS (向量检索)
- Ollama (本地 Embedding)
- DeepSeek API (LLM)

## 项目结构

```
校园活动发布平台/
├── frontend/              # 前端项目 (Vue 3)
├── backend/               # 后端项目 (Spring Boot)
├── campus-rag/            # RAG 知识库系统
│   ├── main.py            # Flask 服务端
│   ├── rag_data/          # 校规原始文档
│   │   └── demo_rules.txt # 预置校规内容 (98条)
│   └── vector_db/         # 预置向量数据库
│       ├── faiss_index.index
│       └── documents.json
└── docs/                  # 文档目录
```

## 快速开始

### 1. 前端启动

```bash
cd frontend
npm install
npm run dev
```

前端运行在 http://localhost:5173

### 2. 后端启动 (Spring Boot)

1. 创建数据库并执行 `backend/src/main/resources/db/schema.sql`
2. 修改 `application.yml` 中的数据库配置
3. 运行 `Application.java`

后端运行在 http://localhost:8080

### 3. RAG 知识库系统启动

#### 前置条件

1. **安装 Ollama** (用于文本向量化)
   ```bash
   # Windows: 从 https://ollama.ai 下载安装
   # 或使用 winget
   winget install Ollama.Ollama
   ```

2. **拉取 Embedding 模型**
   ```bash
   ollama pull qwen3-embedding:0.6b
   ```

3. **配置 LLM API** (可选)
   
   创建 `campus-rag/.env` 文件：
   ```env
   # DeepSeek API (用于生成回答)
   LLM_API_KEY=your_api_key_here
   LLM_MODEL=deepseek-chat
   LLM_BASE_URL=https://api.deepseek.com
   
   # Ollama 配置 (默认本地)
   OLLAMA_BASE_URL=http://localhost:11434
   EMBEDDING_MODEL=qwen3-embedding:0.6b
   ```

#### 启动服务

```bash
cd campus-rag
pip install flask flask-cors requests faiss-cpu numpy python-dotenv
python main.py
```

RAG 服务运行在 http://localhost:9001

#### 访问校规知识库

前端启动后访问：http://localhost:5173/school-rules

## RAG 系统功能

### 智能问答

- **校规相关问题**：使用 RAG 检索校规文档 + LLM 生成回答
- **普通问题**：直接调用 LLM 回答（不加载向量数据库）

### 支持的问题类型

| 类型 | 示例问题 |
|------|----------|
| 处分规定 | 考试作弊会有什么处分？ |
| 宿舍管理 | 宿舍几点关门？晚归几次会处分？ |
| 奖学金 | 一等奖学金多少钱？获奖比例是多少？ |
| 图书馆 | 本科生最多能借几本书？借期多久？ |
| 学籍管理 | 转专业需要什么条件？ |
| 资助政策 | 助学贷款最多能贷多少？ |

### 对话管理

- 新建对话
- 删除对话
- 删除单条消息
- 查看检索结果

## API 接口

### RAG 服务 API (端口 9001)

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/rag/status/` | GET | 获取知识库状态 |
| `/api/rag/chat/` | POST | 发送问题 |
| `/api/rag/upload/` | POST | 上传文档 |
| `/api/rag/save/` | POST | 保存切片到知识库 |
| `/api/rag/delete/` | POST | 删除文档 |
| `/api/rag/conversations/` | GET/POST | 获取/创建对话 |
| `/api/rag/conversations/delete/` | POST | 删除对话 |
| `/api/rag/conversations/delete_message/` | POST | 删除消息 |

### 请求示例

```bash
# 发送问题
curl -X POST http://localhost:9001/api/rag/chat/ \
  -H "Content-Type: application/json" \
  -d '{"question": "考试作弊会有什么处分？", "conversation_id": "test"}'

# 获取状态
curl http://localhost:9001/api/rag/status/
```

## 部署说明

### 向量数据库

- 预置向量数据库位于 `campus-rag/vector_db/`
- 包含 111 个文档切片，覆盖 98 条校规
- 如需更新校规，修改 `rag_data/demo_rules.txt` 后重启服务

### 共享向量数据库

将 `campus-rag/vector_db/` 目录打包分享，对方放到同样位置即可使用。

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
- RAG：遵循 PEP 8 Python 编码规范

## 分支说明

- `main`: 主分支，稳定版本
- `feature/rag-system`: RAG 知识库系统分支
- `dev`: 开发分支

## 相关链接

- [项目仓库](https://github.com/Alex-410/PBL6-7)
- [DeepSeek API](https://platform.deepseek.com)
- [Ollama 官网](https://ollama.ai)
- [FAISS 文档](https://faiss.ai/)
