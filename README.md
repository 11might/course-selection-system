# 选课系统（手敲练习项目）

一个从零手敲的**前后端分离选课系统**，用来练习并打通「前端 → 后端 → 数据库」的完整链路。
包含**用户登录鉴权（JWT）**、**课程列表**、**我的课程（多表关联查询）**三块功能。

> 说明：本项目是个人学习项目，代码为逐行手写，不是从教程复制。
> 开发过程保留了完整的 git 提交历史（从初始化到各功能逐步完成）。

---

## 一、技术栈

| 层 | 技术 | 说明 |
|---|---|---|
| 后端 | Python 3.13 + FastAPI + Uvicorn | 提供 RESTful API |
| 数据库 | MySQL / MariaDB（Wamp 集成环境） | 库名 `course_selection` |
| 数据库驱动 | PyMySQL | 用 `%s` 占位符参数化查询防注入 |
| 鉴权 | PyJWT（HS256） | 登录签发 token，接口验票 |
| 前端 | Vue 3 + Vite | `<script setup>` 组合式 API |
| 前端状态 | Pinia | 存登录用户信息 |
| 前端路由 | Vue Router | 页面跳转 + 路由守卫 |
| 前端请求 | Axios | 封装实例，拦截器自动带 token |

### 端口约定

| 服务 | 端口 |
|---|---|
| 前端开发服务器（Vite） | **5173** |
| 后端 API（Uvicorn） | **8080** |
| 数据库（MariaDB） | **3306** |

---

## 二、已实现功能

### 后端

- [x] 用户登录：查库验密 → 签发 JWT → 返回 token + 用户信息
- [x] 接口鉴权：从 `Authorization: Bearer <token>` 解析身份，失败返回 **401**
- [x] 角色校验：非 student 角色访问受限接口返回 **403**
- [x] 课程列表：查询全部课程（公开接口，不需要 token）
- [x] 我的课程：从 token 解析当前用户 → 关联查询该用户已选课程（**需要 token**）
- [x] SQL 全部使用参数化查询（`%s` + 参数列表），防 SQL 注入

### 前端

- [x] 登录页：账号密码登录，失败提示后端返回的 `msg`
- [x] token 持久化：同时写入 Pinia 与 localStorage，刷新不丢
- [x] Axios 拦截器：**所有请求自动携带** `Authorization: Bearer <token>`
- [x] 路由守卫：无 token 访问 `/home` 时拦截并跳回登录页
- [x] 课程列表页：`v-for` 渲染全部课程
- [x] 我的课程页：`onMounted` 自动加载当前登录用户的选课
- [x] 退出登录：清空 Pinia + localStorage 并跳回登录页

### 数据库

- [x] `user` 用户表
- [x] `course` 课程表
- [x] `student_course` 选课关系表（多对多中间表，含**组合唯一约束**）
- [x] 建表脚本 `sql/init.sql`、测试数据脚本 `sql/seed.sql`（可重复执行）

---

## 三、目录结构

```
I:\EE （2）\
├── sql\
│   ├── init.sql           # 建库建表（user / course / student_course）
│   └── seed.sql           # 测试数据（课程 + 选课关系），可反复执行
├── backend\
│   ├── main.py            # 全部接口（FastAPI 入口，app 变量）
│   ├── config.py          # 数据库与 JWT 配置
│   └── requirements.txt   # 后端依赖清单
├── frontend\
│   ├── package.json       # 前端依赖与脚本
│   ├── vite.config.js
│   └── src\
│       ├── main.js        # 应用入口：createApp + Pinia + Router
│       ├── App.vue        # 根组件（仅 <router-view />）
│       ├── api\
│       │   ├── request.js # axios 实例 + 拦截器（自动带 token）
│       │   ├── auth.js    # 登录接口
│       │   └── course.js  # 课程相关接口
│       ├── store\
│       │   └── user.js    # Pinia：setLogin / logout + localStorage
│       ├── router\
│       │   └── index.js   # 路由表 + 全局前置守卫
│       └── views\
│           ├── Login.vue     # 登录页
│           ├── Home.vue      # 首页（欢迎语 + 页面入口 + 退出）
│           ├── Courses.vue   # 课程列表页
│           └── MyCourses.vue # 我的课程页
└── README.md
```

---

## 四、环境要求

| 依赖 | 版本要求 |
|---|---|
| Python | 3.10+（开发环境为 3.13.12） |
| Node.js | 18+（开发环境约 22） |
| MySQL / MariaDB | 5.7+ / 10.x（开发环境用 Wamp 自带 MariaDB） |

### 后端依赖（backend/requirements.txt）

```
fastapi
uvicorn
pymysql
PyJWT
```

> 注意：若运行环境较新，PyJWT 使用 HS256 可能还需要 `cryptography`，见「已知问题」。

---

## 五、快速开始

### 第 1 步：准备数据库

1. 启动 Wamp，**确保 MariaDB 服务变绿**（端口 3306）
2. 用 MySQL Workbench（或其他客户端）连接 `127.0.0.1:3306`
3. **先执行 `sql/init.sql`** 建库建表
4. **再执行 `sql/seed.sql`** 灌入测试数据

> ⚠️ `init.sql` 中含 `drop table user`，**重复执行会清空 user 表数据**。
> 已有数据时，只执行你新增的那部分语句，不要整个文件跑。

### 第 2 步：启动后端

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8080
```

看到下面这行说明启动成功：

```
INFO:     Uvicorn running on http://127.0.0.1:8080
```

验证：浏览器打开 <http://localhost:8080/> 应返回 `{"msg":"backend ok"}`；
打开 <http://localhost:8080/docs> 是 FastAPI 自动生成的接口文档（Swagger UI）。

### 第 3 步：启动前端

```bash
cd frontend
npm install
npm run dev
```

浏览器打开 <http://localhost:5173>

### 第 4 步：登录测试

测试账号：

| 用户名 | 密码 |
|---|---|
| `stu1` | `123456` |

登录后可点击「查看课程」（全部课程）与「我的课程」（当前用户已选课程）。

---

## 六、数据库设计

### user（用户表）

| 字段 | 类型 | 说明 |
|---|---|---|
| id | int | 主键，自增 |
| username | varchar(50) | 用户名，唯一 |
| password | varchar(255) | 密码（**当前为明文，见已知问题**） |
| role | varchar(25) | 角色：student / teacher / admin |
| real_name | varchar(50) | 真实姓名 |
| created_at | datetime | 创建时间，默认当前时间 |

### course（课程表）

| 字段 | 类型 | 说明 |
|---|---|---|
| id | int | 主键，自增 |
| course_name | varchar(100) | 课程名 |
| teacher_id | int | 授课老师，指向 `user.id` |
| credit | decimal(3,1) | 学分（如 3.5，用 decimal 保证精确） |
| capacity | int | 容量，默认 50 |

### student_course（选课关系表 / 多对多中间表）

| 字段 | 类型 | 说明 |
|---|---|---|
| id | int | 主键，自增 |
| student_id | int | 学生，指向 `user.id` |
| course_id | int | 课程，指向 `course.id` |
| — | unique key | `uk_student_course (student_id, course_id)` 组合唯一 |

**为什么需要这张表**：

- 学生与课程是**多对多**关系（一个学生选多门课，一门课被多个学生选）
- 多对多**无法存进任何一张已有表**：
  - 存进 `user` 会变成 `"1,2"` 这种字符串，数据库无法查询和约束
  - 存进 `course` 会导致课程信息重复（一门课被 60 人选就存 60 行）
- 因此必须用**中间表**，一行代表「某个学生选了某门课」

**组合唯一约束的作用**：防止同一个学生重复选同一门课。违反时报
`Error 1062: Duplicate entry '1-1' for key 'uk_student_course'`。

---

## 七、接口清单

| 方法 | 路径 | 说明 | 需要 token |
|---|---|---|---|
| GET | `/` | 探活，返回 `backend ok` | 否 |
| GET | `/db-test` | 测试数据库连接，列出所有表 | 否 |
| GET | `/user-by-name?username=` | 按用户名查询用户（练习接口） | 否 |
| GET | `/check-password?username=&password=` | 校验密码（练习接口） | 否 |
| POST | `/login?username=&password=` | 登录，返回 token 与用户信息 | 否 |
| GET | `/me` | 返回当前登录用户信息 | **是** |
| GET | `/student-home` | 需 student 角色，否则 403 | **是** |
| GET | `/courses` | 课程列表（全部课程） | 否 |
| GET | `/my-courses` | 当前登录用户已选课程 | **是** |

### 登录返回结构

```json
{
  "msg": "ok",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIs...",
    "userInfo": {
      "id": 1,
      "username": "stu1",
      "role": "student",
      "realName": "王小明"
    }
  }
}
```

### 我的课程返回结构

```json
{
  "msg": "ok",
  "courses": [
    { "student_id": 1, "course_id": 1, "course_name": "数据结构", "credit": 4.0, "capacity": 60 },
    { "student_id": 1, "course_id": 2, "course_name": "计算机网络", "credit": 3.0, "capacity": 50 }
  ]
}
```

### 鉴权说明

需要 token 的接口，请求头必须携带：

```
Authorization: Bearer <token>
```

- token 由 `/login` 签发，**有效期 24 小时**
- 未携带或 token 无效/过期 → **401**
- token 有效但角色不符 → **403**

---

## 八、测试与验证记录

以下为开发过程中实际执行过的验证（含输出），用于说明各功能点的正确性。

### 1. 数据库连接验证

```
GET /db-test
→ {"msg":"db ok","tables":[["course"],["student_course"],["user"]]}
```

### 2. 组合唯一约束验证

**正常插入 4 条选课关系**：

```sql
insert into `student_course`(student_id, course_id) values (1,1),(1,2),(2,1),(2,3);
→ 4 row(s) affected
```

**故意插入重复组合**：

```sql
insert into `student_course`(student_id, course_id) values (1,1);
→ Error Code: 1062. Duplicate entry '1-1' for key 'uk_student_course'
```

**结论**：同一学生不能重复选同一门课，由**数据库层**保证，不依赖应用代码。
同时验证了「student_id 可重复、course_id 可重复，但组合不可重复」。

### 3. JOIN 连表查询验证

```sql
use course_selection;
select sc.student_id, sc.course_id, c.course_name
from `student_course` sc
join `course` c on sc.course_id = c.id
where sc.student_id = 1;
```

**结果**：

| student_id | course_id | course_name |
|---|---|---|
| 1 | 1 | 数据结构 |
| 1 | 2 | 计算机网络 |

**结论**：从关系表出发，通过 `on sc.course_id = c.id` 关联课程表，一次查询取出课程名。

### 4. 接口鉴权验证（401 vs 200）

```
① 不带 token 请求 /my-courses
   → HTTP 401  {"detail":"未登录或token无效"}

② 携带过期 token 请求
   → HTTP 401  （token 有效期 24 小时，过期后验签失败）

③ 重新登录获取新 token 后请求
   → HTTP 200  返回 2 门课程
```

**结论**：受保护接口在无票/废票时正确拒绝，有效票时正常返回。

### 5. SQL 执行顺序验证

SQL 的子句执行顺序为
`from → join → on → where → group by → having → select → order by → limit`。

**验证方式**：`select` 中定义的列别名，在 `where` 中使用会报错，在 `order by` 中可以使用。

```sql
-- 报错：where 先于 select 执行，此时别名尚不存在
select course_name as name from `course` where name = '数据结构';
→ Error Code: 1054. Unknown column 'name' in 'where clause'

-- 正常：order by 后于 select 执行
select course_name as name from `course` order by name;
→ 正常返回
```

### 6. SQL 注入防护验证

所有查询均使用参数化写法，用户输入作为**数据**而非 **SQL 语法**参与执行：

```python
cur.execute('select ... from `user` where username=%s', [username])
```

即使用户输入 `stu1' OR '1'='1` 这类内容，也只会被当作一个普通字符串去比对用户名，
无法改变 SQL 结构（不会退化为 `where 1=1` 恒真条件）。

---

## 九、开发过程中的踩坑记录

| 问题 | 现象 | 原因与解决 |
|---|---|---|
| 未选择数据库 | `Error 1046: No database selected` | 新开查询窗口没有默认库；SQL 开头加 `use course_selection;` |
| SQL 语法错误 | `Error 1064` | 表名误用单引号、漏写逗号等；反引号用于表名/列名，单引号用于字符串值 |
| 参数传递遗漏 | 查询条件写成 `from username=%s` | 漏写 `where` 与表名，值被当成了表名 |
| 接口返回空列表 | `/courses` 返回 `[]` 但无报错 | 表存在但无数据——排查顺序：先查库里数据条数 → 再确认连接的库/端口 → 再看 SQL 条件 → 最后才怀疑代码 |
| 插入未生效 | 程序中 insert 后数据不在库里 | PyMySQL 默认不自动提交，需显式 `conn.commit()` |
| 热重载未生效 | 改完代码接口行为没变 | `--reload` 偶尔卡住，手动重启后端确认 |
| 前端文件移动报错 | 重命名文件后 Vite 报编译错误 | Vite 对文件重命名可能有缓存问题，重启 dev server |
| 路由不匹配 | 新页面访问不到 | 路由路径漏写开头的 `/`；或忘记 `import` 对应组件 |

---

## 十、已知问题与后续计划

### 已知问题

1. **密码明文存储与比对**：`user` 表密码为明文，登录时直接字符串比较。
   学习阶段简化，**正确做法应使用加盐哈希（如 bcrypt / argon2）**。
2. **接口未做统一错误处理**：数据库异常时直接抛出，返回 500。
3. **前端未处理 token 过期**：token 过期后接口返回 401，前端目前不会自动跳回登录页。
4. **`requirements.txt` 可能缺 `cryptography`**：PyJWT 在部分环境使用 HS256 需要该依赖。
5. **连库代码重复**：每个接口都重复了一遍连接/关闭代码，后续可抽取为公共函数或依赖注入。
6. **`config.py` 为开发配置**：数据库空密码、JWT 密钥为示例值，生产环境应改为环境变量。
7. **未加外键约束**：`course.teacher_id`、`student_course.student_id/course_id`
   目前只有注释说明，没有数据库级 `foreign key` 约束。

### 后续计划

- [ ] 选课 / 退课接口（含容量校验、重复选课校验）
- [ ] 教师角色：录入成绩
- [ ] 密码哈希改造
- [ ] 统一异常处理与返回格式
- [ ] 前端 token 过期自动跳转登录
- [ ] 补充单元测试（pytest）

---

## 十一、开发过程说明

本项目采用「一次一小步、先理解再动手」的方式开发：

- 每个功能先明确设计，再手写代码，再实际运行验证
- 数据库结构变更、接口联调、异常排查过程均有记录
- 使用 git 分步提交（`feat` / `docs` 前缀），保留完整开发轨迹
