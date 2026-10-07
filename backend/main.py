from fastapi import FastAPI, Request, HTTPException
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware
import pymysql
import config
import jwt

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
@app.get("/")
def home():
        return {"msg":"backend ok"}
@app.get('/db-test')
def db_test():
    conn=pymysql.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME,
        charset='utf8mb4'
    )
    try:
        with conn.cursor() as cur:
            cur.execute('show tables')
            tables=cur.fetchall()
        return {'msg':'db ok','tables':tables}
    finally:
        conn.close()
@app.get('/user-by-name')
def user_by_name(username:str):
    conn=pymysql.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
    )
    try:
        with conn.cursor() as cur:
            cur.execute(
                'select id,username,password,role,real_name from `user` where username=%s',
                [username],
            )
            row =cur.fetchone()
        if row is None:
            return {'msg':'not found'}
        return {'msg':'ok','user':row}
    finally:
        conn.close()
@app.get('/check-password')
def check_password(username:str,password:str):
    conn=pymysql.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
    )
    try:
        with conn.cursor() as cur:
            cur.execute(
                'select id,username,password,role,real_name from `user` where username=%s',
                [username],
            )
            row=cur.fetchone()
        if row is None:
            return {'msg':'用户名或密码错误'}
        if row['password']!=password:
            return {'msg':'用户名或密码错误'}
        return {
            'msg':'ok',
            'user':{
                'id':row['id'],
                'username':row['username'],
                'role':row['role'],
                'realName':row['real_name'],
            },
        }
    finally:
        conn.close()
@app.post('/login')
def login(username:str,password:str):
    conn=pymysql.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
    )
    try:
        with conn.cursor() as cur:
            cur.execute(
                'select id,username,password,role,real_name from `user` where username=%s',
                [username],
            )
            row=cur.fetchone()
        if row is None or row['password']!=password:
            return {'msg':'用户名或密码错误'}
        payload={
            'user_id':row["id"],
            'username':row['username'],
            'role':row['role'],
            'exp':datetime.utcnow()+timedelta(hours=config.JWT_EXPIRE_HOURS),
        }
        token=jwt.encode(payload,config.JWT_SECRET,algorithm='HS256')
        return {
            'msg':'ok',
           'data':{
               'token':token,
               'userInfo':{
               'id':row['id'],
               'username':row['username'],
               'role':row['role'],
               'realName':row['real_name'],
                }
           },
        }
    finally:
        conn.close()
def get_user_from_token(request:Request):
    """从请求头取出 token，解开后返回 payload；失败就 401"""
    auth=request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer"):
        raise HTTPException(status_code=401,detail='未登录或token无效')
    token=auth[7:]
    try:
        payload=jwt.decode(token,config.JWT_SECRET,algorithms=["HS256"])
        return payload
    except Exception:
        raise HTTPException(status_code=401,detail='未登录或token无效')
@app.get('/me')
def me(request:Request):
    payload=get_user_from_token(request)
    return {
        'msg':'ok',
        'user':{
            'user_id':payload.get("user_id"),
            'username':payload.get('username'),
            'role':payload.get('role'),
        },
    }
@app.get('/student-home')
def student_home(request:Request):
    payload=get_user_from_token(request)
    if payload.get('role')!='student':
        raise HTTPException(status_code=403,detail='需要学生角色')
    return {
        'msg':'ok',
        'tip':'only student can see',
        'username':payload.get('username'),
    }

@app.get('/courses')
def courses():
    conn=pymysql.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
    )
    try:
        with conn.cursor()as cur:
            cur.execute('select id,course_name,teacher_id,credit,capacity from `course`')
            rows=cur.fetchall()
        return {'msg':'ok','courses':rows}
    finally:
        conn.close()
@app.get('/my-courses')
def my_courses(request:Request):
    payload=get_user_from_token(request)
    student_id=payload.get('user_id')
    conn=pymysql.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
    )
    try:
        with conn.cursor()as cur:
            cur.execute('''select sc.student_id,sc.course_id,c.course_name,c.credit,c.capacity
            from `student_course` sc
             join `course` c on sc.course_id=c.id
             where sc.student_id=%s''',
                [student_id],)
            rows=cur.fetchall()
        return {'msg':'ok','courses':rows}
    finally:
        conn.close()
    