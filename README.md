# 选课系统

一个前后端分离的选课系统，实现了登录鉴权、课程列表、我的课程三部分功能。
项目从零搭建，前端、后端和数据库都是自己写的，用来完整走通「页面 → 接口 → 数据库」这条链路。

## 技术栈

- 后端：Python 3.13 + FastAPI + Uvicorn
- 数据库：MySQL / MariaDB（开发环境用 Wamp 自带的 MariaDB）
- 数据库驱动：PyMySQL
- 鉴权：PyJWT（HS256），登录签发 token，受保护接口验证 token
- 前端：Vue 3 + Vite，状态管理 Pinia，路由 Vue Router，请求 Axios

开发时前端跑在 5173，后端跑在 8080，数据库在 3306。

## 功能

已完成：

- 登录：后端查库核对账号密码，成功后签发 JWT，返回 token 和用户信息
- 鉴权：受保护接口从 `Authorization: Bearer <token>` 解析身份，无票或票无效返回 401
- 角色校验：非 student 角色访问对应接口返回 403
- 课程列表：查询全部课程，公开接口，不需要登录
- 我的课程：从 token 解析当前用户，查询该用户已选的课程，需要登录
- 前端登录态：token 同时写进 Pinia 和 localStorage，刷新页面不丢
- 请求拦截器：所有请求自动带上 token，不用每个接口单独处理
- 路由守卫：没登录时访问 /home 会被拦回登录页

没做：

- 选课和退课
- 教师录入成绩
- 密码加密存储
- 单元测试

## 运行步骤

### 1. 准备数据库

启动 Wamp，确认 MariaDB 服务正常（端口 3306），然后用客户端连接 `127.0.0.1:3306`，依次执行：

- `sql/init.sql`：建库建表
- `sql/seed.sql`：插入测试数据

注意 `init.sql` 里有 `drop table user`，重复执行会清空 user 表。如果库里已经有数据，只执行新增的那部分语句。

### 2. 启动后端

```
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8080
```

看到 `Uvicorn running on http://127.0.0.1:8080` 就是起来了。

浏览器打开 http://localhost:8080/ 会返回 `{"msg":"backend ok"}`，
打开 http://localhost:8080/docs 是 FastAPI 自带的接口文档，能直接在上面调接口。

### 3. 启动前端

```
cd frontend
npm install
npm run dev
```

浏览器打开 http://localhost:5173

### 4. 登录

测试账号：`stu1` / `123456`

登录后可以从首页进入课程列表和我的课程。

## 数据库设计

一共三张表。

user 表存用户：

| 字段 | 类型 | 说明 |
|---|---|---|
| id | int | 主键，自增 |
| username | varchar(50) | 用户名，唯一 |
| password | varchar(255) | 密码，目前是明文 |
| role | varchar(25) | 角色，student / teacher / admin |
| real_name | varchar(50) | 姓名 |
| created_at | datetime | 创建时间 |

course 表存课程：

| 字段 | 类型 | 说明 |
|---|---|---|
| id | int | 主键，自增 |
| course_name | varchar(100) | 课程名 |
| teacher_id | int | 授课老师，指向 user.id |
| credit | decimal(3,1) | 学分，用 decimal 而不是 float，避免精度问题 |
| capacity | int | 容量 |

student_course 表存选课关系：

| 字段 | 类型 | 说明 |
|---|---|---|
| id | int | 主键，自增 |
| student_id | int | 学生，指向 user.id |
| course_id | int | 课程，指向 course.id |

这张表加了组合唯一约束 `unique key (student_id, course_id)`。

为什么要单独建这张表：学生和课程是多对多关系，一个学生能选多门课，一门课也能被多个学生选。
这种关系存不进 user 或 course 里。存进 user 只能把多个课程 id 拼成 `"1,2"` 这样的字符串，
数据库没法查询也没法加约束；存进 course 则会让课程信息重复，一门课被 60 个人选就要存 60 行。
所以用中间表，一行表示「某个学生选了某门课」。

组合唯一约束的作用是防止同一个学生重复选同一门课。这条规则交给数据库保证，
不依赖应用代码。重复插入时报 `Error 1062: Duplicate entry '1-1' for key 'uk_student_course'`。

## 接口

| 方法 | 路径 | 说明 | 需要 token |
|---|---|---|---|
| GET | / | 探活 | 否 |
| GET | /db-test | 测试数据库连接，列出所有表 | 否 |
| GET | /user-by-name | 按用户名查用户 | 否 |
| GET | /check-password | 校验密码 | 否 |
| POST | /login | 登录，返回 token 和用户信息 | 否 |
| GET | /me | 返回当前登录用户 | 是 |
| GET | /student-home | 需要 student 角色 | 是 |
| GET | /courses | 全部课程 | 否 |
| GET | /my-courses | 当前用户已选课程 | 是 |

登录的返回：

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

我的课程的返回：

```json
{
  "msg": "ok",
  "courses": [
    { "student_id": 1, "course_id": 1, "course_name": "数据结构", "credit": 4.0, "capacity": 60 },
    { "student_id": 1, "course_id": 2, "course_name": "计算机网络", "credit": 3.0, "capacity": 50 }
  ]
}
```

需要 token 的接口，请求头里要带 `Authorization: Bearer <token>`。
token 由登录接口签发，有效期 24 小时。没带或已失效返回 401，token 有效但角色不符返回 403。

## 测试记录

下面这些是开发过程中实际跑过的验证，连输出一起记下来。

### 数据库连接

```
GET /db-test
返回 {"msg":"db ok","tables":[["course"],["student_course"],["user"]]}
```

### 组合唯一约束

先插四条选课关系，正常：

```sql
insert into `student_course`(student_id, course_id) values (1,1),(1,2),(2,1),(2,3);
-- 4 row(s) affected
```

再故意插一条重复的组合：

```sql
insert into `student_course`(student_id, course_id) values (1,1);
-- Error Code: 1062. Duplicate entry '1-1' for key 'uk_student_course'
```

学生 1 选了课程 1 和 2，学生 2 选了课程 1 和 3，所以 student_id 有重复、course_id 也有重复，
但组合没有重复。重复的组合被数据库挡下来了。

### 连表查询

```sql
use course_selection;
select sc.student_id, sc.course_id, c.course_name
from `student_course` sc
join `course` c on sc.course_id = c.id
where sc.student_id = 1;
```

结果：

```
student_id | course_id | course_name
1          | 1         | 数据结构
1          | 2         | 计算机网络
```

从关系表出发，通过 `on sc.course_id = c.id` 关联到课程表，一次查出课程名，
不用先查关系表拿到 id 再查一次课程表。

### 接口鉴权

```
不带 token 请求 /my-courses        -> HTTP 401  {"detail":"未登录或token无效"}
带过期 token 请求 /my-courses      -> HTTP 401
重新登录拿新 token 后再请求        -> HTTP 200，返回 2 门课程
```

### SQL 子句执行顺序

SQL 的执行顺序是 from → join → on → where → group by → having → select → order by → limit，
select 排在 where 后面。用一个列别名可以验证这一点：

```sql
-- 报错，因为 where 先于 select 执行，别名那时还不存在
select course_name as name from `course` where name = '数据结构';
-- Error Code: 1054. Unknown column 'name' in 'where clause'

-- 正常，order by 后于 select 执行
select course_name as name from `course` order by name;
```

### SQL 注入防护

所有查询都用参数化写法：

```python
cur.execute('select ... from `user` where username=%s', [username])
```

SQL 模板和参数值是分开传给数据库的，用户输入只作为数据参与执行，不会变成 SQL 语法。
比如用户名传 `stu1' OR '1'='1`，这串东西整体只会被当成一个普通字符串去比对，查不到人。

## 开发中遇到的问题

| 问题 | 现象 | 原因和处理 |
|---|---|---|
| 没选数据库 | Error 1046 No database selected | 新开查询窗口没有默认库，SQL 开头加 `use course_selection;` |
| SQL 语法错误 | Error 1064 | 表名误用单引号、漏写逗号等。反引号用于表名列名，单引号用于字符串值 |
| 查询条件写错 | 条件写成 `from username=%s` | 漏了 where 和表名，值被当成表名 |
| 接口返回空列表 | /courses 返回 `[]` 但不报错 | 表在但没数据，排查顺序是先查库里有没有数据，再确认连的哪个库和端口，再看 SQL 条件，最后才怀疑代码 |
| 插入不生效 | 程序里 insert 完库里没有 | PyMySQL 默认不自动提交，需要显式 `conn.commit()` |
| 热重载失效 | 改完代码接口行为没变 | `--reload` 偶尔卡住，手动重启后端 |
| 前端报编译错误 | 重命名文件后 Vite 报错 | Vite 对文件重命名有缓存问题，重启 dev server |
| 页面访问不到 | 新加的路由打不开 | 路由路径漏了开头的 `/`，或者忘了 import 组件 |

## 已知问题和改进计划

目前的问题：

1. 密码是明文存储和比对的，正确做法应该用加盐哈希，比如 bcrypt 或 argon2
2. 没有做统一的异常处理，数据库出错时直接返回 500
3. 前端没处理 token 过期，过期后接口返回 401，前端不会自动跳回登录页
4. requirements.txt 里可能缺 cryptography，PyJWT 在部分环境用 HS256 需要它
5. 每个接口都重复了一遍连接和关闭数据库的代码，可以抽成公共函数
6. config.py 里是开发配置，数据库空密码、JWT 密钥是示例值，生产环境应该走环境变量
7. teacher_id、student_id、course_id 目前没有加数据库级外键约束

接下来打算做：

- 选课和退课接口，包含容量校验和重复选课校验
- 教师录入成绩
- 密码改成哈希存储
- 统一异常处理和返回格式
- 前端处理 token 过期
- 补一些单元测试
