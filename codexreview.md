# Codex Code Review

本次 review 仅总结已核验的非 RAG 相关问题；`/api/rag/**`、`campus-rag/**`、RAG 控制器和知识库服务问题均已按要求排除。

## Critical

### 1. 任意登录用户可禁用账号或修改角色

- 位置：
  - `backend/src/main/java/com/campus/activity/controller/UserController.java:42`
  - `backend/src/main/java/com/campus/activity/controller/UserController.java:52`
  - `backend/src/main/java/com/campus/activity/service/UserService.java:49`
- 现象：
  - `updateStatus` 和 `updateRole` 没有 `@PreAuthorize("hasRole('ADMIN')")`。
  - 全局安全配置对未单独标注的接口只要求 `authenticated()`，因此普通登录用户也能调用。
  - `UserService.updateStatus` 没有角色校验，也没有限制 `status` 只能是 `0/1`。
- 影响：
  - 普通用户可以禁用任意账号，包括管理员。
  - 普通用户可以把自己或他人改为 `PUBLISHER` / `STUDENT_PUBLISHER`。
- 建议：
  - 给两个接口补充管理员权限校验。
  - 对 `status` 做白名单校验。
  - 需要考虑禁止禁用最后一个管理员或当前管理员误禁用自己。

## High

### 2. JWT 签名密钥硬编码

- 位置：
  - `backend/src/main/resources/application.yml:27`
  - `backend/src/main/java/com/campus/activity/utils/JwtUtil.java:17`
- 现象：
  - `jwt.secret` 明文提交在配置文件中。
  - `JwtUtil` 直接使用该配置进行 token 签发和验签。
- 影响：
  - 任何能看到仓库的人都可以伪造合法 JWT，并构造管理员角色绕过鉴权。
- 建议：
  - 改为环境变量，例如 `${JWT_SECRET}`。
  - 生产环境使用足够随机且长度满足 HMAC 要求的密钥。

### 3. 报名人数存在并发超额风险

- 位置：
  - `backend/src/main/java/com/campus/activity/service/RegistrationService.java:39`
  - `backend/src/main/java/com/campus/activity/service/RegistrationService.java:58`
  - `backend/src/main/java/com/campus/activity/mapper/ActivityMapper.java:22`
- 现象：
  - 当前逻辑先读取 `registeredCount` 判断是否满员，再插入报名记录，最后无条件自增 `registered_count`。
- 影响：
  - 并发报名时多个请求可能同时通过满员检查，导致实际报名人数超过 `max_count`。
- 建议：
  - 在数据库层做条件更新：`registered_count < max_count` 时才自增。
  - 如果影响行数为 0，则返回“报名人数已满”。
  - 报名插入和名额扣减需要保持同一事务内的一致性。

## Medium

### 4. CORS 配置过宽且允许凭证

- 位置：
  - `backend/src/main/java/com/campus/activity/config/SecurityConfig.java:54`
  - `backend/src/main/java/com/campus/activity/config/SecurityConfig.java:57`
  - `backend/src/main/java/com/campus/activity/controller/AuthController.java:15`
- 现象：
  - `setAllowedOriginPatterns("*")` 与 `setAllowCredentials(true)` 同时存在。
  - `AuthController` 上还有 `@CrossOrigin(origins = "*")`。
- 影响：
  - 任意来源都可以发起跨域请求，配置面过宽。
- 建议：
  - 限制为明确的前端来源，例如本地开发地址和生产域名。
  - 避免在全局 CORS 配置和 Controller 注解里重复配置。

### 5. 学生默认密码可预测

- 位置：
  - `backend/src/main/java/com/campus/activity/service/AuthService.java:70`
- 现象：
  - 学生登录时使用学号后 6 位作为默认密码。
  - 若用户不存在，首次登录会自动创建账号。
- 影响：
  - 学号通常容易获得或猜测，账号容易被撞库或冒用。
- 建议：
  - 改为一次性初始密码、短信/邮箱验证、统一认证或首次登录强制改密。
  - 对学生账号登录增加更强的身份校验。

### 6. 登录锁定策略容易被滥用且窗口计算不合理

- 位置：
  - `backend/src/main/java/com/campus/activity/service/AuthService.java:134`
  - `backend/src/main/java/com/campus/activity/service/AuthService.java:148`
- 现象：
  - 失败记录只按 username 存储。
  - 后续失败只增加次数，不刷新时间戳。
  - 记录保存在单进程内存中。
- 影响：
  - 攻击者可以持续尝试某个用户名，造成该账号被锁。
  - 多实例部署时锁定策略不一致。
  - 15 分钟窗口从首次失败计算，而不是最近一次失败。
- 建议：
  - 结合账号、IP、设备指纹等维度限流。
  - 将计数放入 Redis 等共享存储。
  - 明确采用滑动窗口或固定窗口策略。

## Low

### 7. `status` 拆箱存在潜在 NPE 风险

- 位置：
  - `backend/src/main/java/com/campus/activity/service/AuthService.java:87`
  - `backend/src/main/java/com/campus/activity/service/AuthService.java:111`
- 现象：
  - `user.getStatus() == 0` 会对 `Integer` 自动拆箱。
- 影响：
  - 当前 SQL 中 `status` 是 `NOT NULL DEFAULT 1`，正常数据库约束下风险较低。
  - 如果历史数据、手工导入或迁移绕过约束导致 `status = null`，登录会抛 NPE。
- 建议：
  - 参考 `JwtAuthenticationFilter` 的写法，显式处理 `null`。

### 8. AI 推荐组件存在调试日志和状态/字段问题

- 位置：
  - `frontend/src/components/StudentAIRecommend.vue:125`
  - `frontend/src/components/StudentAIRecommend.vue:127`
  - `frontend/src/components/StudentAIRecommend.vue:131`
  - `frontend/src/components/StudentAIRecommend.vue:135`
  - `frontend/src/components/StudentAIRecommend.vue:161`
  - `frontend/src/components/StudentAIRecommend.vue:182`
  - `frontend/src/components/StudentAIRecommend.vue:186`
  - `frontend/src/components/StudentAIRecommend.vue:190`
- 现象：
  - 组件中残留多处 `console.log`。
  - `registered` 被硬编码为 `false`，不会反映用户真实报名状态。
  - 构造推荐上下文时把 `description.substring(0, 50)` 放进 `category` 字段，字段语义不准确。
- 影响：
  - 已报名活动仍可能显示“立即报名”。
  - 调试日志污染控制台。
  - AI 推荐提示词中的活动分类信息不准确。
- 建议：
  - 移除调试日志或使用受环境控制的日志工具。
  - 拉取当前用户报名记录并合并到推荐活动状态中。
  - 使用真实 `category` 字段，描述单独传递。

### 9. 前端缺少全局 401 处理

- 位置：
  - `frontend/src/services/api.ts:24`
- 现象：
  - Axios 响应拦截器只返回 `response.data` 或直接 `Promise.reject(error)`。
  - 没有统一处理 token 过期、401、清理登录态或跳转登录页。
- 影响：
  - token 过期或被禁用后，页面请求失败但用户体验不明确。
- 建议：
  - 在响应拦截器中统一处理 HTTP 401 或业务 `code === 401`。
  - 清理 `localStorage` 中的 token/user，并跳转登录页。

## 已排除

以下条目未按本次要求检查或汇总：

- `/api/rag/start` 未鉴权。
- RAG 服务无鉴权、不区分用户。
- RAG 分块参数死循环 / DoS。
- RAG `call_llm` 未检查 HTTP 状态码。
- `RagController` 上的 CORS 配置。
