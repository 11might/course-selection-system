create database if not exists course_selection
default character set utf8mb4;
use course_selection;
drop table if exists `user`;
create table `user`(
 id int primary key auto_increment,
 username varchar(50) not null unique,
 password varchar(255) not null,
 role varchar(25) not null,
 real_name varchar(50) not null,
 created_at datetime default current_timestamp
 );

-- ===== T7 课程列表：course 表（2026-09-21 追加）=====
-- 注意：这里【故意不写 drop table】。
-- 因为执行整个 init.sql 时 drop 是真删，会清空数据；
-- 以后要重建这张表，手动敲一句 drop table `course`; 即可。
-- ↓ 下面这段由本人自己敲（2026-09-21），敲完再写回本文件

create table  `course`(
 id   int primary key auto_increment,
 course_name varchar(100) not null,
 teacher_id int not null,
 credit decimal(3,1) not null,
 capacity int not null default 50
);

-- ===== T8 选课：student_course 关系表（2026-09-25 追加，本人自己敲）=====
-- 多对多中间表：一行 = 某个学生选了某门课
-- unique key：保证同一个学生不会把同一门课选两遍（组合唯一）
create table `student_course`(
 id         int primary key auto_increment,
 student_id int not null,
 course_id  int not null,
 unique key uk_student_course (student_id, course_id)
);