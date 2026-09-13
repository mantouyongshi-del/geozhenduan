# AGENTS.md - GEO 诊断与监控雷达系统开发规则与协作规范

> 本文件是本仓库 (`01-radar-monitor`) 的 AI Agent 与工程师开发总纲。  
> 所有进入本仓库进行代码编写、架构设计、重构或调试的 Agent / 开发者必须严格遵守以下规则。

---

## 一、 通用智能体行为准则 (Core Engineering Principles)

### 1. 谋定而后动 (Think Before Coding)
* **严禁盲目假设**：在改动或实现功能前，必须明确理解输入输出数据契约；
* **暴露技术权衡**：如果存在更简化的实现方式，务必主动提出，拒绝过度设计；
* **遇到模糊立即停顿**：若算法公式或数据模型有疑义，先厘清业务逻辑，不擅自修改核心定性。

### 2. 极简主义原则 (Simplicity First)
* **最小可用代码**：用最少、最清晰的代码解决实际问题，不写投机性的超前抽象；
* **拒绝无用封装**：仅使用一次的逻辑直接平铺，不要建立冗余的多层继承或空壳设计模式；
* **50 行原则**：如果一段能用 50 行写清楚的高内聚逻辑写了 200 行，必须重构精简。

### 3. 外科手术式修改 (Surgical Changes)
* **专注当下变更**：只修改与当前需求直接相关的代码与文件，不随意格式化或重命名无关文件；
* **随手清理自身产生的孤儿代码**：若新增逻辑导致某些 import、变量废弃，主动清理自己的残留；
* **精准代码可追溯性**：代码的每一次 diff 都必须能直接映射到具体的功能或 Bugfix。

### 4. 目标驱动与闭环验证 (Goal-Driven Execution)
* 每次修改诊断算法、提示词或报表渲染，必须通过真实数据流或真机调用进行端到端验证；
* 验证目标明确：算分逻辑准确、报告页面正常渲染、移动端自适应无错位。

---

## 二、 仓库 1 专属业务定位与核心边界 (Domain Boundaries)

### 1. 仓库角色定位
* **系统名称**：蜉蝣小宝 GEO 商业诊断与监控雷达 (Radar & Prescription Engine)
* **核心职责**：作为整个蜉蝣小宝 GEO 商业矩阵的 **“体检中心与处方发起者 (Radar & Prescriber)”**。
* **主要功能**：
  1. 六大主流基座大模型（DeepSeek、豆包、Kimi、元宝、文心一言、通义千问）真机并发评测；
  2. AIVS 六维健康得分测算、同行竞品截流榜统计与商业损失量化测算；
  3. 真实决策现场红黑/攻防对比展区还原、高管专属高清数据战报图直出；
  4. 产出结构化的靶向落地任务工单 (`GeoActionTask`)，作为下游执行舰队的任务源。

### 2. 核心架构与端口约定
* **运行端口**：后端固定为 **`8001`**，前端控制台固定为 **`5173`**；
* **技术栈**：Python 3.9+、FastAPI 异步架构、SQLite/SQLAlchemy、Vue 3 (`<script setup>`)、Vite。

---

## 三、 技术栈与依赖治理规范 (Tech Stack & Dependencies)

| 领域 | 官方核准技术选型 | 核心规范与编码范式 | 🚫 明令禁止引入项 |
| :--- | :--- | :--- | :--- |
| **后端运行时** | Python 3.9+ | 严格使用全异步 `async` / `await` 模式 | 严禁阻塞型长耗时同步调用 |
| **Web 框架** | **FastAPI** | 规范使用 APIRouter、Pydantic v2 模型校验 | 严禁引入 Flask、Django 等异构框架 |
| **持久层** | **SQLite + SQLAlchemy 2.0** | 规范使用 ORM 与 JSON 类型存储复杂分析结果 | 严禁直接手写拼装无防护原生 SQL |
| **跨服务通信** | **HTTPX** (异步模式) | 统一使用异步 Client，用于真机模型调用与跨仓通信 | **严禁引入 requests 造成线程阻塞** |
| **大模型集成** | 官方原生 SDK 或 HTTP Client | 统一通过 `arbiter_service` 集中治理 Prompt 与超时重试 | 严禁引入 LangChain 等重型黑盒 Wrapper |
| **前端框架** | **Vue 3** (Composition API) | 强制使用 `<script setup>` 组合式语法与 Pinia/Ref 状态 | **严禁混用 Vue 2 Options API 或 React** |
| **前端构建** | **Vite** | 极速热重载开发，产物轻量纯净 | 严禁引入 Webpack 等重型构建工具 |
| **报表渲染** | HTML5 Canvas (海报生成) + ECharts | 支持 2.5x Retina 矢量超采样高清直出 | 严禁客户端页面依赖沉重不可控的三方截屏插件 |

---

## 四、 本仓库特有开发规则与架构红线 (Specific Rules)

### 🔴 红线 1：AIVS 算分客观性铁律，严禁虚假自嗨
* 评测结果必须完全基于大模型的真实真机返回内容，严禁人为硬编码虚假“推荐率 0%”或“排位 100 分”；
* 任何维度的得分调整必须在 `diagnostic_service.py` 的算法公式中留有严谨的数学推导与权重释义。

### 🔴 红线 2：任务工单协议标准（下游契约保证）
* 生成的 `GeoActionTask` 工单必须保持向下兼容，必须完整包含以下核心字段：
  * `id`: 工单编号（如 `GEO-001`）；
  * `priority`: 优先级（`P0` / `P1` / `P2`）；
  * `title`: 明确具体的任务标题；
  * `recommended_platforms`: 具体平台阵地清单（如 `["微信公众号", "知乎", "今日头条"]`）；
  * `suggested_title`: 现成可用的建议宣发标题；
  * `core_keywords`: 3~5 个核心实体词与长尾话题标签；
  * `format_guide`: 明确的大模型 RAG 采信结构规范；
  * `action`: 详细实操动作指引；
  * `expected_impact`: 商业收益预期。

### 🔴 红线 3：报告页面与控制台沙箱安全
* 确保客户分享链接（携带 `share=true` 或 `public=true` 时）进入免登只读沙箱模式；
* 内部销售专属工具（如 30 秒促单提词器、工作台返回按钮）在销售视角下必须永久常驻。

---

## 五、 跨系统协同与契约规范 (Cross-Repo Contracts & Governance)

作为 GEO 矩阵的总指挥官，本仓库与下游系统的协同严格遵循以下四大跨仓协议：

### 1. 全局实体主键规范 (Global Entity Identity)
* 跨系统交互必须统一遵循全局实体识别标准：
  * **优先级别**：以企业的 **统一社会信用代码 (18位 USCC)** 作为跨系统通信与知识库索引的唯一物理主键 `brand_id`；
  * **降级备用**：若暂无税号，统一采用 `{企业全称}::{城市}` 作为联合主键。

### 2. 宽容解析原则 (Tolerant Reader Pattern)
* 仓库 1 在升级工单结构新增字段时，必须保证旧有字段的语义向下兼容；
* 新增字段尽量赋予合理的默认值，确保下游分发系统即使运行老版本也不会被解析异常中断。

### 3. 优雅降级与兜底机制 (Graceful Degradation)
* 在生成工单时，即便外部大模型 API 调用超时，必须由本地的高质量多行业兜底规则平滑降级，保证报告 100% 成功生成。

### 4. 内部服务通信鉴权 (Internal Service Token)
* 未来向下游分发系统推送工单或提供查询时，统一在 HTTP 请求头中附加预共享密钥：
  * Header: `X-Internal-Token: ${INTERNAL_SERVICE_SECRET}`
  * 本地开发环境下未配置该环境变量时默认信任放行。

### 5. 工单向内容工厂的自动下发 (Downstream Dispatch)
体检报告生成后，`GeoActionTask` 工单会自动推送到下游 `03-seo-distribution`（内容工厂）：

* **触发时机**：`/api/v1/diagnostic/run` 体检成功后**自动**下发；走后台任务，绝不阻塞体检报告实时返回，失败静默降级（不反噬主流程）。
* **手动补推**：`POST /api/v1/distribution/dispatch`，入参 `{"report_code": "...", "brand_id": null, "task_ids": null}`；
* **连通性自检**：`GET /api/v1/distribution/status`；
* **相关环境变量**：

| 变量 | 默认值 | 说明 |
| :--- | :--- | :--- |
| `DISTRIBUTION_API_URL` | `http://127.0.0.1:8003` | 下游内容分发系统地址 |
| `DISTRIBUTION_ENABLED` | `true` | 下发总开关（关闭则零网络请求） |
| `DISTRIBUTION_AUTO_DISPATCH` | `true` | 体检成功后是否自动下发 |
| `DISTRIBUTION_TIMEOUT_S` | `5` | 单次请求超时（秒） |
| `DISTRIBUTION_MAX_RETRIES` | `3` | 失败重试次数（指数退避） |
| `INTERNAL_SERVICE_SECRET` | 空 | 跨仓预共享令牌，非空时附带 `X-Internal-Token` |

* **主键约定（重要）**：01 当前无 USCC 档案字段，`brand_id` 会降级为 `{企业全称}::{城市}` 联合主键（见五.1）；
  调用方可在 `dispatch` 请求中显式传 `brand_id` 覆盖。**生产环境务必传 18 位 USCC**，
  否则下游按该降级主键检索不到知识库事实，事实注入会退化为兜底语料。
* 下游不可达时返回 `200` 且 `degraded > 0`（优雅降级），**绝不返回 5xx**。
