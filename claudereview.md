# 代码审查报告（Claude Review）

> 审查范围：Spring Boot 后端 + Vue 前端 + Flask RAG 服务
> 审查日期：2026-06-16
> 以下问题均已逐条核实，定位与行号准确。

## 概览

| 编号 | 等级 | 问题 | 位置 |
|------|------|------|------|
| #1 | P1 | 任意登录用户可禁用账号 / 自授发布权限 | `UserController.java:42,52` |
| #2 | P1 | 任意登录用户可查看任意活动报名名单 | `RegistrationController.java:39` |
| #3 | P1 | 报名容量检查存在并发超卖 | `RegistrationService.java:39` |
| #4 | P2 | 取消报名未实现"开始前 24 小时内不可取消" | `RegistrationService.java:64` |
| #5 | P2 | STUDENT_PUBLISHER 详情页不能报名 / 取消 | `ActivityDetail.vue:30` |
| #6 | P3 | 报名管理页报名时间永远显示 "—" | `PublisherRegistrations.vue:18` |

---

## P1（严重）

### #1 任意登录用户可禁用账号 / 自授发布权限

- **位置**：`backend/src/main/java/com/campus/activity/controller/UserController.java:42`（`updateStatus`）、`:52`（`updateRole`）
- **问题**：两个接口缺少 `@PreAuthorize("hasRole('ADMIN')")`，而同文件 `list:21`、`detail:33` 都有。由于 `SecurityConfig.java:45` 仅要求 `.anyRequest().authenticated()`，任何登录用户均可调用。
- **危害**：
  - `updateStatus` 在 service 层（`UserService.java:49`）**零校验**，可将任意用户（含管理员）置为 `status=0`，再经 `JwtAuthenticationFilter.java:43` 直接将对方踢下线。
  - `updateRole`（`UserService.java:53-73`）service 层禁止提升为 ADMIN / 修改 ADMIN，但允许 `USER → STUDENT_PUBLISHER / PUBLISHER`，普通用户可自授发布权限。
- **与文档冲突**：README 中"用户管理 / 角色权限由管理员管理"。
- **建议**：两个接口补加 `@PreAuthorize("hasRole('ADMIN')")`，并校验 `status ∈ {0,1}`。

### #2 任意登录用户可查看任意活动报名名单

- **位置**：`backend/src/main/java/com/campus/activity/controller/RegistrationController.java:39`
- **问题**：`byActivity` 直接返回 `findByActivityId(activityId)`，未校验当前用户是否为活动发布者或管理员，仅需登录即可访问。
- **危害**：普通学生只要知道 `activityId`，即可获取报名记录中的 `userId / status / registeredAt`（`Registration.java:9-12`），属敏感数据泄露，违反角色权限隔离要求。
- **建议**：校验调用者为该活动发布者或 ADMIN 后再返回。

### #3 报名容量检查存在并发超卖

- **位置**：`backend/src/main/java/com/campus/activity/service/RegistrationService.java:39`（判满）、`:58-59`（插入并 +1）
- **问题**：先读 `registeredCount >= maxCount` 判满，再插入报名，最后调用 `ActivityMapper.java:22` 的无条件 `registered_count = registered_count + 1`。读-判-写非原子（TOCTOU），高并发下多请求都读到未满，最终超过 `max_count`。
- **与文档冲突**：需求文档明确要求避免超卖。
- **建议**：改为数据库原子约束，例如 `UPDATE activity SET registered_count = registered_count + 1 WHERE id = ? AND registered_count < max_count`，并把"影响 0 行"视为"已满"。

---

## P2（中）

### #4 取消报名未实现"开始前 24 小时内不可取消"

- **位置**：`backend/src/main/java/com/campus/activity/service/RegistrationService.java:64`（`cancel`）
- **问题**：仅校验 `status == "registered"`，完全未读取活动开始时间，任何时刻都能取消并释放名额。
- **与文档冲突**：`docs/校园活动发布平台需求文档.md:142-143` 要求"开始时间 ≤ 24 小时时提示不可取消"。
- **建议**：取消前读取活动 `startTime`，若距开始 ≤ 24 小时则拒绝。

### #5 STUDENT_PUBLISHER 详情页不能报名 / 取消

- **位置**：`frontend/src/components/ActivityDetail.vue:30`
- **问题**：报名/取消区块条件为 `v-if="user.role==='student'"`，只匹配普通学生。`useCurrentUser.ts:14` 将 `student_publisher` 映射为 `'student_publisher'`，不等于 `'student'`，故学生发布者在详情页看不到报名/取消按钮。
- **与文档冲突**：README:155 定义 STUDENT_PUBLISHER"兼具学生和发布者权限"。
- **建议**：条件改为同时允许 `'student'` 与 `'student_publisher'`。

---

## P3（低）

### #6 报名管理页报名时间永远显示 "—"

- **位置**：`frontend/src/components/PublisherRegistrations.vue:18`
- **问题**：后端实体字段为 `registeredAt`（`Registration.java:12`），`adapters.ts` 的 `adaptRegistration`（`:14-21`）仅 `...raw` 透传，未将 `registeredAt` 映射为 `createTime`；而页面读取的是 `r.createTime`，恒为 `undefined`，永远渲染 `—`。
- **建议**：在 `adaptRegistration` 中映射 `createTime: raw.registeredAt`，或页面直接读取 `r.registeredAt`。

---

## 修复优先级建议

1. **#1**：危害最高，普通用户即可瘫痪管理员账号 / 越权提权，应最优先修复。
2. **#2、#3**：数据泄露与超卖，影响数据正确性与隐私。
3. **#4、#5**：功能与需求/文档不一致。
4. **#6**：展示缺陷，体验问题。
