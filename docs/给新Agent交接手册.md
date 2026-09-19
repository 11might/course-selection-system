# 给新 Agent 的交接手册（必读）

> 用途：C 盘重装 / 对话丢失后，新对话里的 Agent **先读本文件**，再动手。  
> 权威程度：环境与禁区、教学习惯、**代码真实进度** 以本文件为准。  
> 旧进度 Word / md 可能过时，不要只信「学习进度与技术说明」里的「下一步」。  
> 本文更新日期：2026-09-14（退出登录完成；Git 已 init 未 commit；根目录 .gitignore 已备）

---

## 0. 开场 30 秒清单

1. 项目根目录：`I:\EE （2）`（手敲版选课系统；成品参考在 `I:\EE`，别混）。  
2. 用户：潘志坤；目标 Python 后端实习；一次一小步、先理解再敲。  
3. 默认只动学习环境；**禁止**乱动独立 MySQL；危险操作先确认。  
4. 进度以**代码**为准：登录 + JWT + 存 token + 守卫 + **Home 用户名 + 退出登录** 已通；选课业务未做；**Git 已 init，尚未第一次 commit**。  
5. 库在 **Wamp MariaDB 端口 3306**（不是 3308 的 MySQL 8）。  
6. 债：只认 8/12 约 **4h15min**；之后空窗先不算。  
7. **复习/开课优先用提问检验**。  
8. store 易读版：`setupUserStore` + `defineStore('user', setupUserStore)`。  
9. Git：`I:\Study\Git`；全局署名 志 / 1606472380a@gmail.com；仓库根 `I:\EE （2）`；根目录已有 `.gitignore`。  
10. cmd 进项目必须：`cd /d "I:\EE （2）"`（PowerShell 一般不用 `/d`）。

---

## 1. 用户是谁、在干什么

- 方向：Python 后端实习；先搞通前后端 + 数据库，再加深 Python。  
- 做法：在 `I:\EE （2）` **从零手敲**；可参考 `I:\EE` 成品，但本目录是练习版。  
- 原则：一步一小块；新文件/新概念要说清「在做什么 / 为什么 / 为后面什么服务」。  
- 学法约定（用户已强调）：**先理解再敲**；新名字、新函数必须说明从哪来；能自己敲的让他自己敲，Agent 指导为主，不要整段代写完除非他明确要求代做。

---

## 2. 教学与沟通习惯（必须对齐）

### 怎么教

- 一次只推一小步；讲清再出现代码。  
- 实习口述优先：主链路能讲（查库→验密→JWT→Bearer→角色），细原理可后补。  
- 安全必记：SQL 必须参数化（`%s` + 列表/元组），禁止拼接用户输入；用户要能口述防注入。  
- 前端更适合用 WebStorm；后端/总览可用 PyCharm / Cursor。

### 检验方式（本人明确喜欢 · 优先用）

- **多用提问检验**他记住多少，而不是一上来长篇重讲。  
- 题要对准他**现有薄弱点**和**本项目真实写法**（勿按成品 `I:\EE` 的哈希等超前假设，除非在对比说明）。  
- 允许答「忘了」；批改时：对的简短肯定，错的指出错在哪、和项目里谁负责。  
- 典型易混点（可持续抽问）：  
  - token **后端** `jwt.encode` 生成，**前端** `setLogin` 写入 localStorage  
  - Bearer 后面是 **token 字符串**；自动带头的是 **前端 axios 拦截器**  
  - `res.data.data`：axios 的 `res.data` + 后端包的 `data`；Home **不**再用 `res`，读 `userStore`  
  - `useUserStore` = 钥匙函数；`userStore = useUserStore()` = 仓；模板变量名须一致  
  - 仓名 `'user'` ≠ stu1；stu1 是 `userInfo` 里的货  
  - 登录页 **5173**；API **8080**（**uvicorn 在听**）；库 **3306**  
  - 验密在后端 **同一个 `login` 函数**里用 `!=` 比，不是另调一个对比函数  
  - `python -m uvicorn main:app --port 8080`：`app` 须与 `FastAPI()` 变量名一致  
  - **401** 没票/票无效；**403** 有票但角色不够  
  - 手敲版密码仍是**明文比对**  
- 单参数占位：`[username]`（与 `(username,)` 等价）。

### 怎么说话

- 直接、简洁；长文先给结论。  
- 少用大段加粗；少废话、少「下面分几部分」。  
- 用户规则里：危险/非法操作不给步骤；本项目场景下主要是 **别乱动库与系统**。

### 督学（压力驱动，用户曾授权）

- 可查岗、可严厉，但 **9 月排班需用户重新确认**（文档里 8 月休息日已过期）。  
- **债口径（2026-09-04 本人确认）：** 只保留 8/12 时欠下的约 **4h15min**；8/12 之后因重装等空窗 **先不算**；何时摊还以后再说。  
- 打卡模板（若用户还要用）：日期 / 上班或休息 / 是否空窗 / 实际时长 / 还债分钟 / 完成任务 / 未完成。

### 项目依赖

- venv、`node_modules`、pip/npm 包：**默认用户自己装**，除非明确说「你代做」。  
- Agent 不要擅自大范围重装依赖。

---

## 3. 硬性禁区与原则

| 规则 | 说明 |
|------|------|
| 独立 MySQL 勿动 | `I:\Study\MySQL` 有问题，**先别管**；不要修、不要启、不要改数据。 |
| 只用 Wamp 这一套库 | 项目连 Wamp；历史曾有 `I:\EE\mysql-run` 等，已弃用。 |
| 不要把 Wamp PHP 写进 PATH | 会报警/冲突。 |
| 能原路径跑就不重装软件 | 软件本体多在数据盘。 |
| 危险操作先确认 | 删库、改服务、改系统配置、force 类 git 等。 |
| 默认只动学习环境 | Python / Node / PyCharm / WebStorm / Wamp；QQ/微信/G HUB/Java 等除非另说。 |

---

## 4. 环境（C 盘重装 + 工作盘改盘符后）

### 盘符

- 手册旧路径曾写 `D:\Study`、`D:\environment`；**现为 `I:`**：`I:\Study`、`I:\environment`。  
- 日常其它软件仍多在 `E:\01_Software`。  
- 系统恢复手册：`I:\电脑\C盘重装后快速恢复手册.docx`（桌面/E 盘也可能有副本）。

### 学习软件现状（2026-08-30 核对后）

| 用途 | 路径 / 说明 | 状态 |
|------|-------------|------|
| Python | `I:\Study\Python idle`（3.13）；PATH 已加；桌面「Python IDLE」 | 可用 |
| PyCharm | `I:\Study\PyCharm\...\bin\pycharm64.exe` | 可用 |
| WebStorm | `I:\Study\WebStorm\...\bin\webstorm64.exe` | 可用 |
| Node / npm | `I:\environment`（Node ~22 / npm ~10.9） | 可用 |
| Wamp | `I:\Study\Wampmanager`；主要当数据库用 | 可用 |
| Wamp Apache | `wampapache64`；`http://127.0.0.1:8030/` | 服务可跑 |
| Wamp MariaDB | `wampmariadb64`，**端口 3306** ← **项目数据在这里** | 要用 |
| Wamp MySQL 8 | `wampmysqld64`，端口 **3308**；**没有** `course_selection` | 别连错 |
| 独立 MySQL | `I:\Study\MySQL` | **勿动** |
| Java / Maven / IDEA | 文件在 I 盘，PATH/快捷方式本轮未配 | 本项目暂不用 |

### 用户 PATH（应包含）

```
I:\Study\Python idle
I:\Study\Python idle\Scripts
I:\environment
```

（后面可有 WindowsApps。）

### Cursor 终端注意

- Cursor 可能把自带 `helpers\node.exe` 插到 PATH 最前。  
- 用户设置里应有（若丢失请补回）：

```json
"terminal.integrated.env.windows": {
  "Path": "I:\\Study\\Python idle;I:\\Study\\Python idle\\Scripts;I:\\environment;${env:Path}"
}
```

- 校验口令：`where python` / `where node` / `where npm` 应指向 I 盘上述路径。  
- 若 `python` 变成微软商店空壳：删掉 `%LOCALAPPDATA%\Microsoft\WindowsApps\python.exe` 与 `python3.exe` 占位，并确认 User PATH。

### 数据库连接（项目）

- `backend\config.py`：`127.0.0.1:3306`，`root`，密码 `""`，库 `course_selection`。  
- 测试用户：`stu1` / `123456`（明文，学习阶段）。  
- Workbench：连 **3306 / MariaDB**，不要连 3308 还以为库丢了。

---

## 5. 项目结构（真实文件）

```
I:\EE （2）\
  sql\
    init.sql                 # 建库建表（user）
  backend\
    requirements.txt         # fastapi / uvicorn / pymysql / PyJWT
    config.py                # DB + JWT 配置
    main.py                  # 全部后端接口
    （无 start.bat；文档若写有，以本条为准）
  frontend\
    package.json             # vue / pinia / vue-router / axios / vite
    src\
      main.js                # createApp + Pinia + router
      App.vue                # 仅 <router-view />
      api\request.js         # baseURL http://localhost:8080；自动 Bearer
      api\auth.js            # POST /login（query 传 username/password）
      store\user.js          # setLogin / logout + localStorage
      router\index.js        # /login /home；无 token 拦 /home
      views\Login.vue        # 登录页（已通）
      views\Home.vue         # 欢迎 + userStore.userInfo.username（已通）
  docs\
    本交接手册 + 日记/进度/时间表 md 与 docx
```

无 `.git`。

### 依赖实况（2026-09-04 本机核对）

用户主观感觉「什么都没装」，但当场检查结果是：

| 项 | 结果 |
|----|------|
| Python / pip | 可用（`I:\Study\Python idle`，3.13.12） |
| `fastapi` / `uvicorn` / `pymysql` / `PyJWT` | **已装且可 import**（在 Python idle 的 site-packages） |
| Node / npm | 可用（`I:\environment`）；注意 Cursor 终端 `where node` 可能先看到 Cursor 自带 node，但 I 盘 node/npm 也在 PATH |
| 前端 `node_modules`（vue/pinia/router/axios/vite） | **已在** |
| Wamp MariaDB 3306 / `course_selection.user` | 服务可跑；测试用户在 |

结论：跑简单 Python、起本项目前后端，**按现状不必先重装依赖**。若某台机器或缺包，再 `pip install -r backend\requirements.txt` / 在 `frontend` 下 `npm install`。缺包时默认让用户自己装，除非他明确说代做。

---

## 6. 代码真实进度（比旧文档准）

### 后端已有接口

| 接口 | 作用 |
|------|------|
| `GET /` | `backend ok` |
| `GET /db-test` | 连库，列表示表 |
| `GET /user-by-name` | 按用户名查人（练习） |
| `GET /check-password` | 验密练习 |
| `POST /login` | 验密 + JWT；返回 `data.token` + `data.userInfo` |
| `GET /me` | Bearer 鉴权，当前用户 |
| `GET /student-home` | 需 student 角色，否则 403 |

要点：查库用 `%s` 参数化；CORS 允许 `http://localhost:5173`；后端端口约定 **8080**（Apache 在 8030）。

### 前端已完成（约等于原 T1～T5）

- Vite 壳、Pinia `setLogin`/`logout`、axios 拦截器带 token、Login 联调、失败看 `msg`、路由守卫、**Home 显示用户名 + 退出按钮**。  
- store 易读写法：`setupUserStore` + `export const useUserStore = defineStore('user', setupUserStore)`。  
- 登录成功：`setLogin(res.data.data)`（注意 **双 data**）。

### 未做 / 下一步建议（开干时再与用户确认）

1. 退出登录按钮 — **已完成（9/13）**  
2. Git：已 init；下次 **第一次 add/commit**（再可选 push）。  
3. 课程列表 / 选课（原 T7/T8）。  
4. 教师录成绩等。  
5. 密码改密文、整理重复连库代码——非当前最高优先级。

### 旧文档漂移（别踩坑）

- `学习进度与技术说明` / `学习总结完整版.docx` 仍可能写「前端登录没做」「角色校验可选未做」——**已过时**。  
- 日记 `今日总结-2026-07-25.md` 续写到 **2026-08-12**，更接近代码。  
- 文档写 `backend\start.bat`：**文件不存在**。启动用：

```text
cd /d I:\EE （2）\backend
python -m uvicorn main:app --reload --port 8080
```

```text
cd /d I:\EE （2）\frontend
npm run dev
```

---

## 7. 日常怎么开（方案：用时再开）

```text
1. Wamp → 等服务绿（至少 MariaDB；Apache 8030 可选）
2. 后端 :8080 → http://localhost:8080/ 与 /docs
3. 前端 :5173 → 登录 stu1 / 123456 → 看 Local Storage 有 token、userInfo
4. 用完：终端 Ctrl+C；Wamp 可关
```

口令复习：

```text
WAMP(MariaDB 3306) → uvicorn 8080 → npm run dev → stu1 登录 → /home 守卫
```

面试口述（已练过的版本）：

> 登录查库验密，成功签发 JWT；受保护接口从 Authorization: Bearer 取 token 校验，失败 401；角色不对 403。查库不拼接用户输入，用占位符防 SQL 注入。前端 setLogin 把 token 存 Pinia + localStorage，axios 拦截器自动带 Bearer。

---

## 8. docs 里还有什么

| 文件 | 用途 |
|------|------|
| **本手册** `给新Agent交接手册.md` / `.docx` | 新 Agent 第一优先 |
| `今日总结-2026-07-25.md` | 按天日记（已续写到 2026-09-05） |
| `学习进度与技术说明.md` | 长期说明（进度表可能旧） |
| `每日学习时间表与督学约定.md` | 8 月督学；Word 为旧权威，9 月需重确认 |
| `学习总结完整版.docx` | 通勤合并本（可能旧） |
| `Word文档说明.txt` | 各 Word 职责 |
| `_md_to_docx.py` | md 导出 docx |

更新习惯：先改 md，再跑导出脚本或让 Agent 导出。

---

## 9. 任务队列快照（原 T 表，状态已校正）

| 编号 | 任务 | 真实状态（2026-09-04） |
|------|------|------------------------|
| T1 | Vite 壳 | 已完成 |
| T2 | Pinia setLogin | 已完成 |
| T3 | request 自动 Bearer | 已完成 |
| T4 | Login + localStorage | 已完成 |
| T5 | 路由守卫 + Home 用户名 + 退出 | **已完成** |
| T6 | Git | **进行中**：已安装/署名/init/.gitignore；**缺第一次 commit**（push 未做） |
| T7 | 课程列表 | **未做** |
| T8 | 选课 | **未做** |
| T9 | 教师/管理一小块 | **未做** |
| T10 | 面试口述 + 简历 Demo | 穿插；主链路口述已有基础 |

---

## 10. 新对话建议开场策略

1. 读本手册；必要时扫 `backend\main.py` 与 `frontend\src` 确认无意外改动。  
2. 问用户：今天是同步 / 复习 / 推进哪一小步；**不要默认开选课大功能**。  
3. 若复习：先出几道对准易混点的题（见「检验方式」），再补讲；Bearer / 双 data 若仍糊可专拆一节。  
4. 若推进：Git 第一次 commit（或 push）/ 选课业务 / 用户指定。  
5. 债：按 8/12 的 4h15min 口径；之后空窗先不算。  
6. 涉及 Wamp 端口、删数据、改 PATH、动独立 MySQL：**先确认**。  
7. 用户 PATH 若再次丢失：应含 `Python idle`、`Scripts`、`I:\environment`、`I:\Study\Git\cmd`；Cursor `terminal.integrated.env.windows` 同步前置这些路径。

---

## 11. 一句话给新 Agent

这是一个 **登录鉴权前后端已打通、业务选课未开始** 的手敲练习项目；库在 **MariaDB 3306**；教的时候 **小步 + 提问检验 + 让他自己敲**；独立 MySQL 与乱改系统环境是红线；旧进度文档会骗人，以代码和本手册为准。
