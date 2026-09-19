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
